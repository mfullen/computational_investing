package com.mfullen.ci;

import com.mfullen.ci.dbmodel.Price;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Date;
import java.util.List;
import java.util.Map;

/**
 *
 * @author mfullen
 */
public class InMemoryPriceRepository implements PriceRepository
{
    private List<Price> quotes = new ArrayList<Price>();

    public Collection<Price> getBySymbol(String symbol)
    {
        Collection<Price> p = new ArrayList<Price>();

        for (Price price : quotes)
        {
            if (price.getSymbol().equalsIgnoreCase(symbol))
            {
                p.add(price);
            }
        }

        return p;
    }

    public Collection<Price> getByDate(Date date)
    {
        Collection<Price> p = new ArrayList<Price>();

        for (Price price : quotes)
        {
            if (price.getDate().equals(date))
            {
                p.add(price);
            }
        }

        return p;
    }

    public Collection<Price> getByDateRange(Date start, Date end)
    {
        Collection<Price> p = new ArrayList<Price>();

        for (Price price : quotes)
        {
            if (price.getDate().after(start) && price.getDate().before(end))
            {
                p.add(price);
            }
        }

        return p;
    }

    public Price save(Price entity)
    {
        this.quotes.add(entity);
        return entity;
    }

    public Price delete(Price entity)
    {
        this.quotes.remove(entity);
        return entity;
    }

    public Price getById(long id)
    {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }

    public Collection<Price> getAll()
    {
        return this.quotes;
    }

    public Collection<Price> getBySymbolDateRange(String symbol, Date start, Date end)
    {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }

    public Map<String, Collection<Price>> getBySymbolsDateRange(String[] symbols, Date start, Date end)
    {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }
}
