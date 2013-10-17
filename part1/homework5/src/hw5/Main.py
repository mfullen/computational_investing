'''
Created on Oct 16, 2013

@author: mfullen
'''
import datetime as dt
import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep



if __name__ == '__main__':
    print "Hello World"
    ls_symbols = ['AAPL','GOOG','IBM','MSFT']
    dt_start = dt.datetime(2010,1,1 )
    dt_end = dt.datetime(2010, 12, 31)
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    c_dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)
    prices = d_data['close']
   
    rolling_mean = pd.rolling_mean(prices,20)
    rolling_std = pd.rolling_std(prices,20)
    bollinger_val = (prices - rolling_mean)/rolling_std
    
    print bollinger_val.values