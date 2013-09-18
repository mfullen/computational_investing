'''
Created on Sep 15, 2013

Computational Investing Part 1 HW 2: Event Studies

@author: mfullen
'''
import unittest
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import copy
import numpy as np
import QSTK.qstkstudy.EventProfiler as ep

class Hw2Test(unittest.TestCase):

    def find_events(self,ls_symbols, d_data, eventPrice):
        ''' Finding the event dataframe '''
        df_close = d_data['actual_close']
        ts_market = df_close['SPY']
    
        print "Finding Events"
    
        # Creating an empty dataframe
        df_events = copy.deepcopy(df_close)
        df_events = df_events * np.NAN
    
        # Time stamps for the event range
        ldt_timestamps = df_close.index
    
        for s_sym in ls_symbols:
            for i in range(1, len(ldt_timestamps)):
                # Calculating the returns for this timestamp
                f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
                f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
                #f_marketprice_today = ts_market.ix[ldt_timestamps[i]]
                #f_marketprice_yest = ts_market.ix[ldt_timestamps[i - 1]]
                #f_symreturn_today = (f_symprice_today / f_symprice_yest) - 1
                #f_marketreturn_today = (f_marketprice_today / f_marketprice_yest) - 1
    
                # Event is found if the symbol is down more then 3% while the
                # market is up more then 2%
                if f_symprice_today < eventPrice and f_symprice_yest >= eventPrice: 
                    df_events[s_sym].ix[ldt_timestamps[i]] = 1
    
        return df_events
    
    def testExample1(self):
        print("======================testExample1===============")
        dt_start = dt.datetime(2008,1,1)
        dt_end = dt.datetime(2009,12,31)
        ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
        dataobj = da.DataAccess('Yahoo')
        ls_symbols = dataobj.get_symbols_from_list('sp5002012')
        ls_symbols.append('SPY')
        ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
        ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
        d_data = dict(zip(ls_keys, ldf_data))
        
        for s_key in ls_keys:
            d_data[s_key] = d_data[s_key].fillna(method='ffill')
            d_data[s_key] = d_data[s_key].fillna(method='bfill')
            d_data[s_key] = d_data[s_key].fillna(1.0)
        
        print d_data
        
        eventPrice = 5.0
        expectedEvents = 176
        resultEventNumber = 0
        
        df_events = self.find_events(ls_symbols, d_data, eventPrice)
        
        print "Creating Study"
        ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                    s_filename='testExample1EventStudy.pdf', b_market_neutral=True, b_errorbars=True,
                    s_market_sym='SPY')
      
        #self.assertEqual(expectedEvents, resultEventNumber, "Events are not equal")
        pass
        
    def testExample2(self):
        print("======================testExample2===============")
        dt_start = dt.datetime(2008,1,1)
        dt_end = dt.datetime(2009,12,31)
        ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
        dataobj = da.DataAccess('Yahoo')
        ls_symbols = dataobj.get_symbols_from_list('sp5002008')
        ls_symbols.append('SPY')
        ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
        ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
        d_data = dict(zip(ls_keys, ldf_data))
        
        for s_key in ls_keys:
            d_data[s_key] = d_data[s_key].fillna(method='ffill')
            d_data[s_key] = d_data[s_key].fillna(method='bfill')
            d_data[s_key] = d_data[s_key].fillna(1.0)
        
        print d_data
        
        eventPrice = 5.0
        expectedEvents = 326
        resultEventNumber = 0
        
        df_events = self.find_events(ls_symbols, d_data, eventPrice)
        
        print "Creating Study"
        ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                    s_filename='testExample2EventStudy.pdf', b_market_neutral=True, b_errorbars=True,
                    s_market_sym='SPY')
        pass
        #self.assertEqual(expectedEvents, resultEventNumber, "Events are not equal")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Hw2Test.testName']
    unittest.main()