'''
Created on Oct 22, 2013

@author: mfullen
'''

import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import csv
import QSTK.qstkstudy.EventProfiler as ep
from hw5.Main import Hw5App



class Hw6App(object):
    
    def __init__(self):
        '''
        Constructor
        '''
        
    def find_events(self,ls_symbols, price_data):
        ''' Finding the event dataframe '''
        df_close = price_data
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
                f_marketprice_today = ts_market.ix[ldt_timestamps[i]]
                f_marketprice_yest = ts_market.ix[ldt_timestamps[i - 1]]
                f_cutoff = -2.0
                market_cutoff = 1.1
                if f_symprice_today < f_cutoff and f_symprice_yest >= f_cutoff and f_marketprice_today >= market_cutoff:
                    df_events[s_sym].ix[ldt_timestamps[i]] = 1
    
        return df_events
if __name__ == '__main__':
    dataobj = da.DataAccess('Yahoo')
    ls_symbols = dataobj.get_symbols_from_list('sp5002012')
    ls_symbols.append('SPY')
    print "got symbols"
    dt_start = dt.datetime(2008,1,1 )
    dt_end = dt.datetime(2009, 12, 31)
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    app5 = Hw5App()
    print "getting close data"
    prices = app5.get_close_data(ls_symbols, ldt_timestamps)
    print "Got close data"
    close_price = prices['close']
    bollinger_val = app5.create_bollinger_matrix(close_price, 20)
    print bollinger_val.values
    
    app6 = Hw6App()
    df_events = app6.find_events(ls_symbols, bollinger_val)
        
    print "Creating Study"
    ep.eventprofiler(df_events, prices, i_lookback=20, i_lookforward=20, s_filename='Hw6Quiz1EventStudy.pdf', b_market_neutral=True, b_errorbars=True, s_market_sym='SPY')
    ''' expectedEvents = 278  '''
    