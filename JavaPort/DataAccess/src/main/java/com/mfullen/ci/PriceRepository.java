package com.mfullen.ci;

import com.mfullen.ci.dbmodel.Price;
import com.mfullen.infrastructure.Repository;
import java.util.Collection;
import java.util.Date;
import java.util.Map;

/**
 *
 * @author mfullen
 */
public interface PriceRepository extends Repository<Price>
{
    Collection<Price> getBySymbol(String symbol);

    Collection<Price> getByDate(Date date);

    Collection<Price> getByDateRange(Date start, Date end);

    Collection<Price> getBySymbolDateRange(String symbol, Date start, Date end);

    Map<String, Collection<Price>> getBySymbolsDateRange(String[] symbols, Date start, Date end);
}
