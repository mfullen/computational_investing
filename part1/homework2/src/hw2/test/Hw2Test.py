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
import pandas as pd

class Hw2Test(unittest.TestCase):

    def find_events(self,ls_symbols, d_data, eventPrice):
        df_close = d_data['actual_close']
        print df_close
        print "Finding Events"
        #np.set_printoptions(threshold='nan')
        #pd.set_printoptions(max_rows=510, max_columns=510)
        my_test = (df_close < eventPrice) & (df_close.shift(1) >= eventPrice)
        df_close[my_test] = 1
        #print my_test.values
        #print df_close[my_test].values
        #print df_close[my_test].sum().sum()
       
        return df_close[my_test]
    
    def find_events_rose_above(self,ls_symbols, d_data, eventPrice):
        df_close = d_data['actual_close']
        my_test = (df_close > eventPrice) & (df_close.shift(1) <= eventPrice)
        df_close[my_test] = 1

        return df_close[my_test]
    
    def fetch_data(self, dt_start, dt_end, symbolsFile):
        ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
        dataobj = da.DataAccess('Yahoo')
        ls_symbols = dataobj.get_symbols_from_list(symbolsFile)
        ls_symbols.append('SPY')
        ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
        ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
        d_data = dict(zip(ls_keys, ldf_data))
        
        for s_key in ls_keys:
            d_data[s_key] = d_data[s_key].fillna(method='ffill')
            d_data[s_key] = d_data[s_key].fillna(method='bfill')
            d_data[s_key] = d_data[s_key].fillna(1.0)
            
        return d_data, ls_symbols
    
    def testExample1(self):
        print("======================testExample1===============")
        dt_start = dt.datetime(2008,1,1)
        dt_end = dt.datetime(2009,12,31)
        eventPrice = 5.0
       
        d_data, ls_symbols = self.fetch_data(dt_start, dt_end ,'sp5002012')
        df_events = self.find_events(ls_symbols, d_data, eventPrice)
        
        print "Creating Study"
        ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                    s_filename='testExample1EventStudy.pdf', b_market_neutral=True, b_errorbars=True,
                    s_market_sym='SPY')
        ''' expectedEvents = 176 '''
        pass
        
    def testExample2(self):
        print("======================testExample2===============")
        dt_start = dt.datetime(2008,1,1)
        dt_end = dt.datetime(2009,12,31)
        eventPrice = 5.0
       
        d_data, ls_symbols = self.fetch_data(dt_start, dt_end ,'sp5002008')
        df_events = self.find_events(ls_symbols, d_data, eventPrice)
        
        print "Creating Study"
        ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                    s_filename='testExample2EventStudy.pdf', b_market_neutral=True, b_errorbars=True,
                    s_market_sym='SPY')
        ''' expectedEvents = 326 '''
        pass
    
    def testHwQuestion2(self):
        print("======================testHwQuestion2===============")
        dt_start = dt.datetime(2008,1,1)
        dt_end = dt.datetime(2009,12,31)
        eventPrice = 6.0
       
        d_data, ls_symbols = self.fetch_data(dt_start, dt_end ,'sp5002008')
        df_events = self.find_events(ls_symbols, d_data, eventPrice)
        
        print "Creating Study"
        ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                    s_filename='testHwQuestion2EventStudy.pdf', b_market_neutral=True, b_errorbars=True,
                    s_market_sym='SPY')
        ''' expectedEvents = 326 '''
        pass
    
    def testHwQuestion3(self):
        print("======================testHwQuestion3===============")
        dt_start = dt.datetime(2008,1,1)
        dt_end = dt.datetime(2009,12,31)
        eventPrice = 7.0
       
        d_data, ls_symbols = self.fetch_data(dt_start, dt_end ,'sp5002012')
        df_events = self.find_events(ls_symbols, d_data, eventPrice)
        
        print "Creating Study"
        ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                    s_filename='testHwQuestion3EventStudy.pdf', b_market_neutral=True, b_errorbars=True,
                    s_market_sym='SPY')
        ''' expectedEvents = 326 '''
        pass
    
    def testCustomEvent_roseAbove5_2008(self):
        print("======================testCustomEvent_roseAbove5_2008===============")
        dt_start = dt.datetime(2008,1,1)
        dt_end = dt.datetime(2009,12,31)
        eventPrice = 5.0
       
        d_data, ls_symbols = self.fetch_data(dt_start, dt_end ,'sp5002008')
        df_events = self.find_events_rose_above(ls_symbols, d_data, eventPrice)
        
        print "Creating Study"
        ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                    s_filename='RoseAbove5Dollars2008EventStudy.pdf', b_market_neutral=True, b_errorbars=True,
                    s_market_sym='SPY')
        pass
    
    def testCustomEvent_roseAbove10_2008(self):
        print("======================testCustomEvent_roseAbove10_2008===============")
        dt_start = dt.datetime(2008,1,1)
        dt_end = dt.datetime(2009,12,31)
        eventPrice = 10.0
       
        d_data, ls_symbols = self.fetch_data(dt_start, dt_end ,'sp5002008')
        df_events = self.find_events_rose_above(ls_symbols, d_data, eventPrice)
        
        print "Creating Study"
        ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                    s_filename='RoseAbove10Dollars2008EventStudy.pdf', b_market_neutral=True, b_errorbars=True,
                    s_market_sym='SPY')
        pass
    
    def testCustomEvent_roseAbove5_2012(self):
        print("======================testCustomEvent_roseAbove5_2012===============")
        dt_start = dt.datetime(2008,1,1)
        dt_end = dt.datetime(2009,12,31)
        eventPrice = 5.0
       
        d_data, ls_symbols = self.fetch_data(dt_start, dt_end ,'sp5002012')
        df_events = self.find_events_rose_above(ls_symbols, d_data, eventPrice)
        
        print "Creating Study"
        ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                    s_filename='RoseAbove5Dollars2012EventStudy.pdf', b_market_neutral=True, b_errorbars=True,
                    s_market_sym='SPY')
        pass
    
    def testCustomEvent_roseAbove10_2012(self):
        print("======================testCustomEvent_roseAbove10_2012===============")
        dt_start = dt.datetime(2008,1,1)
        dt_end = dt.datetime(2009,12,31)
        eventPrice = 10.0
       
        d_data, ls_symbols = self.fetch_data(dt_start, dt_end ,'sp5002012')
        df_events = self.find_events_rose_above(ls_symbols, d_data, eventPrice)
        
        print "Creating Study"
        ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                    s_filename='RoseAbove10Dollars2012EventStudy.pdf', b_market_neutral=True, b_errorbars=True,
                    s_market_sym='SPY')
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Hw2Test.testName']
    unittest.main()