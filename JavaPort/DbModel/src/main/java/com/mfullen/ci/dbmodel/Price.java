package com.mfullen.ci.dbmodel;

import com.mfullen.model.AbstractModel;

import java.util.Date;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Table;
import javax.persistence.Temporal;
import javax.persistence.TemporalType;
import javax.persistence.UniqueConstraint;

/**
 *
 * @author mfullen
 */
@Entity
@Table(uniqueConstraints =
        @UniqueConstraint(columnNames =
{
    "eventDate", "symbol"
}))
public class Price extends AbstractModel
{
    @Column(name = "symbol", nullable = false)
    private String symbol;
    @Column(name = "eventDate", nullable = false)
    @Temporal(TemporalType.DATE)
    private Date eventDate;
    private Double openPrice;
    private Double high;
    private Double low;
    private Double closePrice;
    private Double adjustedClose;
    private Integer volume;

    public String getSymbol()
    {
        return symbol;
    }

    public void setSymbol(String symbol)
    {
        this.symbol = symbol;
    }

    public Date getDate()
    {
        return eventDate;
    }

    public void setDate(Date date)
    {
        this.eventDate = date;
    }

    public Double getOpen()
    {
        return openPrice;
    }

    public void setOpen(Double open)
    {
        this.openPrice = open;
    }

    public Double getHigh()
    {
        return high;
    }

    public void setHigh(Double high)
    {
        this.high = high;
    }

    public Double getLow()
    {
        return low;
    }

    public void setLow(Double low)
    {
        this.low = low;
    }

    public Double getClose()
    {
        return closePrice;
    }

    public void setClose(Double close)
    {
        this.closePrice = close;
    }

    public Double getAdjustedClose()
    {
        return adjustedClose;
    }

    public void setAdjustedClose(Double adjustedClose)
    {
        this.adjustedClose = adjustedClose;
    }

    public Integer getVolume()
    {
        return volume;
    }

    public void setVolume(Integer volume)
    {
        this.volume = volume;
    }

    @Override
    public String toString()
    {
        return "Price{" + "symbol=" + symbol + ", date=" + eventDate + ", open=" + openPrice + ", high=" + high + ", low=" + low + ", close=" + closePrice + ", adjustedClose=" + adjustedClose + ", volume=" + volume + '}';
    }
}
