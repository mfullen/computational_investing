package com.mfullen.ci.homework.service.impl;

import com.google.inject.Inject;
import com.mfullen.ci.PriceRepository;
import com.mfullen.ci.dbmodel.Price;
import com.mfullen.ci.homework.service.FundMetrics;
import com.mfullen.ci.homework.service.MetricsService;
import java.util.Collection;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import org.apache.commons.math3.linear.MatrixUtils;
import org.apache.commons.math3.linear.RealMatrix;
import org.apache.commons.math3.stat.descriptive.SummaryStatistics;
import org.apache.commons.math3.stat.descriptive.summary.Sum;

/**
 *
 * @author mfullen
 */
public class FundMetricService implements MetricsService
{
    private PriceRepository priceRepository;

    @Inject
    public FundMetricService(PriceRepository priceRepository)
    {
        this.priceRepository = priceRepository;
    }

    public double calculateFundSharpeRatio(String symbol, Date start, Date end)
    {
        Collection<Price> bySymbol = this.priceRepository.getBySymbolDateRange(symbol, start, end);

//        for (Price price : bySymbol)
//        {
//            System.out.println("Symbol: " + price.getSymbol());
//            System.out.println("Date: " + price.getDate());
//            System.out.println("Adjusted close: " + price.getAdjustedClose());
//        }

        double[] adjustedClose = new double[bySymbol.size()];

        int i = 0;
        for (Price price : bySymbol)
        {
            adjustedClose[i++] = price.getAdjustedClose();
        }

        double[] normalize = new double[adjustedClose.length];

        for (int j = 0; j < normalize.length; j++)
        {
            normalize[j] = adjustedClose[j] / adjustedClose[0];
        }


        double[] dailyReturnArray = new double[normalize.length];

        for (int j = 1; j < dailyReturnArray.length; j++)
        {
            dailyReturnArray[j - 1] = (normalize[j] / normalize[j - 1]) - 1.0;
        }


        SummaryStatistics stats = new SummaryStatistics();
        for (double d : dailyReturnArray)
        {
            stats.addValue(d);
        }

        double volatility = stats.getStandardDeviation();
        double dailyReturn = stats.getMean();
        double sharpeRatio = Math.sqrt(252.0) * dailyReturn / volatility;
        double cumulativeReturn = normalize[normalize.length - 1];

        System.out.println("Vol: " + volatility);
        System.out.println("Daily Return: " + dailyReturn);
        System.out.println("Sharpe: " + sharpeRatio);
        System.out.println("Cum Return: " + cumulativeReturn);


        return sharpeRatio;
    }

    public FundMetrics calculateMetrics(String[] symbols, Date start, Date end)
    {
        Map<String, Collection<Price>> bySymbolsDateRange = this.priceRepository.getBySymbolsDateRange(symbols, start, end);

        long startTime = System.nanoTime();
        
        Map<String, double[]> adjustedClose = new HashMap<String, double[]>();

        for (Map.Entry<String, Collection<Price>> entry : bySymbolsDateRange.entrySet())
        {
            double[] ac = new double[entry.getValue().size()];

            int i = 0;
            for (Price price : entry.getValue())
            {
                ac[i++] = price.getAdjustedClose();
            }
            adjustedClose.put(entry.getKey(), ac);
        }

        Map<String, double[]> normalizeMap = new HashMap<String, double[]>();

        for (Map.Entry<String, double[]> entry : adjustedClose.entrySet())
        {
            double[] ac = new double[entry.getValue().length];

            for (int j = 0; j < ac.length; j++)
            {
                ac[j] = entry.getValue()[j] / entry.getValue()[0];
            }

            normalizeMap.put(entry.getKey(), ac);
        }

        double[][] normalizedMatrix = new double[normalizeMap.keySet().size()][];

        int i = 0;
        for (Map.Entry<String, double[]> entry : normalizeMap.entrySet())
        {
            normalizedMatrix[i++] = entry.getValue();
        }

        RealMatrix matrix = MatrixUtils.createRealMatrix(normalizedMatrix);
        Sum sum = new Sum();
        int rowDimension = matrix.getRowDimension();
        int colDimension = matrix.getColumnDimension();

        double[] cumulativeArray = new double[colDimension];

        for (int j = 0; j < colDimension; j++)
        {
            cumulativeArray[j] = sum.evaluate(matrix.getColumn(j));
        }

        double[] dailyReturnMatrix = new double[cumulativeArray.length];

        for (int j = 1; j < dailyReturnMatrix.length; j++)
        {
            dailyReturnMatrix[j - 1] = (cumulativeArray[j] / cumulativeArray[j - 1]) - 1.0;
        }

        SummaryStatistics stats = new SummaryStatistics();
        for (double d : dailyReturnMatrix)
        {
            stats.addValue(d);
        }

        double volatility = stats.getStandardDeviation();
        double dailyReturn = stats.getMean();
        double sharpeRatio = Math.sqrt(252.0) * dailyReturn / volatility;
        double cumulativeReturn = cumulativeArray[cumulativeArray.length - 1];

        long endTime = System.nanoTime();

        FundMetrics metrics = new FundMetrics();
        metrics.setVolatility(volatility);
        metrics.setDailyReturn(dailyReturn);
        metrics.setSharpeRatio(sharpeRatio);
        metrics.setCumulativeReturn(cumulativeReturn);
        metrics.setCalculationTime(endTime - startTime);


        return metrics;
    }

    public static void main(String[] args)
    {
        double[][] matrixData =
        {
            {
                1d, 2d, 3d
            },
            {
                2d, 5d, 3d
            },
            {
                3d, 5d, 3d
            }
        };

        RealMatrix matrix = MatrixUtils.createRealMatrix(matrixData);
        Sum sum = new Sum();
        double evaluate = sum.evaluate(matrix.getColumn(0));
        System.out.println("Eval: " + evaluate);
    }
}
