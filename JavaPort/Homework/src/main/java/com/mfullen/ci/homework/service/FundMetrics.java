package com.mfullen.ci.homework.service;

/**
 *
 * @author mfullen
 */
public class FundMetrics
{
    private double dailyReturn;
    private double sharpeRatio;
    private double cumulativeReturn;
    private double volatility;
    private double calculationTime;

    public double getDailyReturn()
    {
        return dailyReturn;
    }

    public void setDailyReturn(double dailyReturn)
    {
        this.dailyReturn = dailyReturn;
    }

    public double getSharpeRatio()
    {
        return sharpeRatio;
    }

    public void setSharpeRatio(double sharpeRatio)
    {
        this.sharpeRatio = sharpeRatio;
    }

    public double getCumulativeReturn()
    {
        return cumulativeReturn;
    }

    public void setCumulativeReturn(double cumulativeReturn)
    {
        this.cumulativeReturn = cumulativeReturn;
    }

    public double getVolatility()
    {
        return volatility;
    }

    public void setVolatility(double volatility)
    {
        this.volatility = volatility;
    }

    public void setCalculationTime(double calculationTime)
    {
        this.calculationTime = calculationTime;
    }

    public double getCalculationTime()
    {
        return calculationTime;
    }

    @Override
    public String toString()
    {
        return "FundMetrics{" + "dailyReturn=" + dailyReturn + ", sharpeRatio=" + sharpeRatio + ", cumulativeReturn=" + cumulativeReturn + ", volatility=" + volatility + ", calculationTime=" + calculationTime + '}';
    }
}
