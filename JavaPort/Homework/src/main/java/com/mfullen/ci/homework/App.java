package com.mfullen.ci.homework;

import com.google.inject.Guice;
import com.google.inject.Injector;
import com.google.inject.persist.jpa.JpaPersistModule;
import com.mfullen.ci.homework.service.FundMetrics;
import com.mfullen.ci.homework.service.MetricsService;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;

/**
 *
 * @author mfullen
 */
public class App
{
    public static void main(String[] args)
    {
        Injector injector = Guice.createInjector(new JpaPersistModule("production"), new DesktopModule());
        MyInitializer instance = injector.getInstance(MyInitializer.class);

        MetricsService metricsService = injector.getInstance(MetricsService.class);

        GregorianCalendar gregorianCalendar = new GregorianCalendar();
        gregorianCalendar.set(2008, Calendar.JANUARY, 1);
        Date start = gregorianCalendar.getTime();

        gregorianCalendar.set(2009, Calendar.DECEMBER, 30);
        Date end = gregorianCalendar.getTime();

        double calculateFundSharpeRatio = metricsService.calculateFundSharpeRatio("GOOG", start, end);
        System.out.println("Fund Sharpe: " + calculateFundSharpeRatio);

        FundMetrics calculateMetrics = metricsService.calculateMetrics(new String[]
        {
            "GOOG"
        }, start, end);
        System.out.println("calculateMetrics: " + calculateMetrics);
    }
}
