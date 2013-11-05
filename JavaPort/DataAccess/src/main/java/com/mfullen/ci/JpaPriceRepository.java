package com.mfullen.ci;

import com.mfullen.ci.dbmodel.Price;
import com.mfullen.ci.dbmodel.Price_;
import com.mfullen.repositories.jpa.AbstractJpaRepository;
import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.persistence.TypedQuery;
import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Predicate;
import javax.persistence.criteria.Root;

/**
 *
 * @author mfullen
 */
public class JpaPriceRepository extends AbstractJpaRepository<Price> implements
        PriceRepository
{
    public Collection<Price> getBySymbol(String symbol)
    {
        List<Price> findByField = this.findByField(Price_.symbol, symbol);
        return findByField;
    }

    public Collection<Price> getByDate(Date date)
    {
        List<Price> findByField = this.findByField(Price_.eventDate, new Timestamp(date.getTime()));
        return findByField;
    }

    public Collection<Price> getByDateRange(Date start, Date end)
    {
        CriteriaBuilder builder = getEntityManager().getCriteriaBuilder();
        CriteriaQuery<Price> query = builder.createQuery(Price.class);

        Root<Price> root = query.from(Price.class);

        Predicate condition = builder.greaterThanOrEqualTo(root.get(Price_.eventDate), start);
        Predicate condition2 = builder.lessThanOrEqualTo(root.get(Price_.eventDate), end);

        query.where(condition, condition2);

        TypedQuery<Price> q = this.getEntityManager().createQuery(query);

        return q.getResultList();
    }

    public Collection<Price> getBySymbolDateRange(String symbol, Date start, Date end)
    {
        CriteriaBuilder builder = getEntityManager().getCriteriaBuilder();
        CriteriaQuery<Price> query = builder.createQuery(Price.class);

        Root<Price> root = query.from(Price.class);

        Predicate datePredicate = builder.between(root.get(Price_.eventDate), start, end);
        Predicate symbolPredicate = builder.equal(root.get(Price_.symbol), symbol);
        Predicate andPredicate = builder.and(datePredicate, symbolPredicate);


        query.where(andPredicate).orderBy(builder.asc(root.get(Price_.eventDate)));


        TypedQuery<Price> typedQuery = this.getEntityManager().createQuery(query);
        return typedQuery.getResultList();
    }

    public Map<String, Collection<Price>> getBySymbolsDateRange(String[] symbols, Date start, Date end)
    {
        Map<String, Collection<Price>> map = new HashMap<String, Collection<Price>>();

        CriteriaBuilder builder = getEntityManager().getCriteriaBuilder();
        CriteriaQuery<Price> query = builder.createQuery(Price.class);

        Root<Price> root = query.from(Price.class);

        Predicate datePredicate = builder.between(root.get(Price_.eventDate), start, end);
        Predicate symbolPredicate = builder.equal(root.get(Price_.symbol), symbols[0]);

        for (int i = 1; i < symbols.length; i++)
        {
            symbolPredicate = builder.or(symbolPredicate, builder.equal(root.get(Price_.symbol), symbols[i]));
        }

        Predicate andPredicate = builder.and(datePredicate, symbolPredicate);

        query.where(andPredicate).orderBy(builder.asc(root.get(Price_.eventDate)));

        TypedQuery<Price> typedQuery = this.getEntityManager().createQuery(query);
        List<Price> resultList = typedQuery.getResultList();

        for (Price price : resultList)
        {
            if (!map.containsKey(price.getSymbol()))
            {
                map.put(price.getSymbol(), new ArrayList<Price>());
            }
            map.get(price.getSymbol()).add(price);
        }

        return map;
    }
}
