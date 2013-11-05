package com.mfullen.ci.homework;

import com.google.inject.AbstractModule;
import com.mfullen.ci.JpaPriceRepository;
import com.mfullen.ci.PriceRepository;
import com.mfullen.ci.homework.service.MetricsService;
import com.mfullen.ci.homework.service.impl.FundMetricService;

/**
 *
 * @author mfullen
 */
public class DesktopModule extends AbstractModule
{
    @Override
    protected void configure()
    {
        bind(PriceRepository.class).to(JpaPriceRepository.class);
        bind(MetricsService.class).to(FundMetricService.class);
    }
}
