package com.mfullen.ci;

import com.mfullen.ci.dbmodel.Price;
import java.io.File;
import java.io.FileFilter;
import java.io.FileReader;
import java.sql.Timestamp;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;
import javax.persistence.criteria.CriteriaQuery;
import org.supercsv.cellprocessor.constraint.NotNull;
import org.supercsv.cellprocessor.ift.CellProcessor;
import org.supercsv.io.CsvListReader;
import org.supercsv.io.ICsvListReader;
import org.supercsv.prefs.CsvPreference;
import org.apache.commons.io.FilenameUtils;
import org.hibernate.Session;

/**
 *
 * @author mfullen
 */
public class CsvImport
{
    public static final String CSV_DIR = "C:\\Python27\\Lib\\site-packages\\QSTK\\QSData\\Yahoo";
    private static final String P_UNIT = "production";
    private static final String P_UNIT2 = "test";
    private static EntityManagerFactory factory;
    private static EntityManager entityManager;
    private static Session session;

    public static void main(String[] args) throws Exception
    {
        //URL resource = Thread.currentThread().getContextClassLoader().getResource("A.csv");
        //String filePath = resource.getFile();
        File csvDirectory = new File(CSV_DIR);
        File[] listFiles = csvDirectory.listFiles(new FileFilter()
        {
            public boolean accept(File pathname)
            {
                return pathname.isFile() && pathname.getName().endsWith(".csv");
            }
        });
        File[] listFiles2 =
        {
            listFiles[241]//GOOG
        };

        ExecutorService service = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());
        long startTime = System.nanoTime();
        final List<Price> priceList = new CopyOnWriteArrayList<Price>();


        for (final File file : listFiles)
        {
            Runnable runnable = new Runnable()
            {
                public void run()
                {
                    try
                    {
                        priceList.addAll(readWithCsvListReader(file.getAbsolutePath()));
                        System.out.println("Finished file: " + file.getAbsolutePath());
                    }
                    catch (Exception ex)
                    {
                        Logger.getLogger(CsvImport.class.getName()).log(Level.SEVERE, null, ex);
                    }
                }
            };
            service.execute(runnable);
        }

        service.shutdown();
        service.awaitTermination(5, TimeUnit.MINUTES);
        long difference = System.nanoTime() - startTime;
        long milliseconds = TimeUnit.MILLISECONDS.convert(difference, TimeUnit.NANOSECONDS);
        long seconds = TimeUnit.SECONDS.convert(difference, TimeUnit.NANOSECONDS);
        System.out.println("Completed in Seconds: " + seconds);
        System.out.println("Completed in MiliSeconds: " + milliseconds);
        System.out.println("Size: " + priceList.size());

        setupPersistence();
        entityManager.getTransaction().begin();
        int errors = 0;
        for (Price price : priceList)
        {

            try
            {
                entityManager.persist(price);
            }
            catch (Exception e)
            {
                errors++;
            }

        }
        entityManager.getTransaction().commit();

        System.out.println("Executed with this many errors: " + errors);
        //Collection<Price> bySymbol = repository.getBySymbol("GOOG");
        //System.out.println("By Symbol size: " + bySymbol.size());
        CriteriaQuery<Price> query = entityManager.getCriteriaBuilder().createQuery(Price.class);
        query.from(Price.class);
        List<Price> prices = entityManager.createQuery(query).getResultList();
        System.out.println("Prices size: " + prices.size());
        tearDownPersistence();
    }

    static void setupPersistence()
    {
        factory = Persistence.createEntityManagerFactory(P_UNIT);
        entityManager = factory.createEntityManager();
    }

    static void tearDownPersistence()
    {
        factory.close();
    }

    private static List<Price> readWithCsvListReader(String filename) throws
            Exception
    {
        List<Price> priceList = new ArrayList<Price>();
        ICsvListReader listReader = null;
        try
        {
            listReader = new CsvListReader(new FileReader(filename), CsvPreference.STANDARD_PREFERENCE);

            listReader.getHeader(true); // skip the header (can't be used with CsvListReader)

            final CellProcessor[] processors =
            {
                new NotNull(),
                new NotNull(),
                new NotNull(),
                new NotNull(),
                new NotNull(),
                new NotNull(),
                new NotNull()
            };

            DateFormat df = new SimpleDateFormat("yyyy-MM-dd", Locale.ENGLISH);

            List<Object> customerList;

            while ((customerList = listReader.read(processors)) != null)
            {
//                System.out.println(String.format("lineNo=%s, rowNo=%s, prices=%s", listReader.getLineNumber(),
//                        listReader.getRowNumber(), customerList));

                Price p = new Price();
                p.setSymbol(FilenameUtils.removeExtension(new File(filename).getName()));
                Date parse = df.parse(customerList.get(0).toString());
                p.setDate(new Timestamp(parse.getTime()));
                p.setOpen(Double.valueOf(customerList.get(1).toString()));
                p.setHigh(Double.valueOf(customerList.get(2).toString()));
                p.setLow(Double.valueOf(customerList.get(3).toString()));
                p.setClose(Double.valueOf(customerList.get(4).toString()));
                p.setVolume(Integer.valueOf(customerList.get(5).toString()));
                p.setAdjustedClose(Double.valueOf(customerList.get(6).toString()));

                priceList.add(p);
            }
        }
        finally
        {
            if (listReader != null)
            {
                listReader.close();
            }
            return priceList;
        }
    }
}
