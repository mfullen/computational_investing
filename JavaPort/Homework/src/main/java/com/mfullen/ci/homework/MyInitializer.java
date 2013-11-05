package com.mfullen.ci.homework;

import com.google.inject.Inject;
import com.google.inject.persist.PersistService;

/**
 *
 * @author mfullen
 */
public class MyInitializer
{
    @Inject
    MyInitializer(PersistService service)
    {
        service.start();

        // At this point JPA is started and ready.
    }
}
