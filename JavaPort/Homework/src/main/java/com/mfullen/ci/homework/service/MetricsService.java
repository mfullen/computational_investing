package com.mfullen.ci.homework.service;

import java.util.Date;

/**
 *
 * @author mfullen
 */
public interface MetricsService
{
    double calculateFundSharpeRatio(String symbol, Date start, Date end);

    FundMetrics calculateMetrics(String[] symbols, Date start, Date end);
}
