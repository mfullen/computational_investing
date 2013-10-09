'''
Created on Oct 7, 2013

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

from hw3.MarketSim import MarketSim
from hw3.Analyze import Analyze

class Hw4App(object):
    
     def __init__(self):
        '''
        Constructor
        '''
     def find_events(self,ls_symbols, d_data, event_price):
        ''' Finding the event dataframe '''
        df_close = d_data['actual_close']
        ts_market = df_close['SPY']
    
        print "Finding Events"
    
        # Creating an empty dataframe
        df_events = copy.deepcopy(df_close)
        df_events = df_events * np.NAN
    
        # Time stamps for the event range
        ldt_timestamps = df_close.index
    
        filename = "event_orders.csv"
        with open(filename, 'wb') as w:
            for s_sym in ls_symbols:
                for i in range(1, len(ldt_timestamps)):
                    # Calculating the returns for this timestamp
                    f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
                    f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
                    f_cutoff = event_price
                    if f_symprice_today < f_cutoff and f_symprice_yest >= f_cutoff:
                        df_events[s_sym].ix[ldt_timestamps[i]] = 1
                        buy_date = ldt_timestamps[i]
                        event_sym = s_sym
                        sell_date = ldt_timestamps[i]
                        if((i+ 5) > len(ldt_timestamps)):
                            #if our sell date exceeds our timestamps, sell on the last date
                            sell_date = ldt_timestamps[-1]
                        else:
                            sell_date = ldt_timestamps[i + 5]
                        
                        
                            writer = csv.writer(w, delimiter=',')
                            shares = 100
                            buy_order = [buy_date.strftime("%Y"), buy_date.strftime("%m"), buy_date.strftime("%d"), event_sym, "Buy", shares]
                            sell_order = [sell_date.strftime("%Y"), sell_date.strftime("%m"), sell_date.strftime("%d"), event_sym, "Sell", shares]
                            writer.writerow(buy_order) 
                            writer.writerow(sell_order) 
            return df_events


     def event_study(self, dt_start, dt_end, symbols_list, event_price):
        ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

        print "Data Access"
        dataobj = da.DataAccess('Yahoo')
        ls_symbols = dataobj.get_symbols_from_list(symbols_list)
        ls_symbols.append('SPY')
        ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
        print "Looking Up data"
        ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
        print "dict Data"
        d_data = dict(zip(ls_keys, ldf_data))

        print "Backfilling NAN data"
        for s_key in ls_keys:
            d_data[s_key] = d_data[s_key].fillna(method = 'ffill')
            d_data[s_key] = d_data[s_key].fillna(method = 'bfill')
            d_data[s_key] = d_data[s_key].fillna(1.0)
            
        df_events = self.find_events(ls_symbols, d_data, event_price)
        
        print "Creating Study"
        date_str= str(dt_start.month) + "-" + str(dt_start.year) + "_" + str(dt_end.month) + "-" + str(dt_end.year)
        filename = "EventStudy-" + date_str + "Price- " + str(event_price) + ".pdf"
        ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                     s_filename=filename, b_market_neutral=True, b_errorbars=True,
                    s_market_sym='SPY')
        
if __name__ == '__main__':
    #inputs
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    #dt_end = dt.datetime(2008, 1, 5)
    symbols_list = 'sp5002012'
    event_price = 8.0
    
    app = Hw4App()
    app.event_study(dt_start, dt_end, symbols_list, event_price)
    
    orders_file = "event_orders.csv"
    sim = MarketSim()
    orders = sim.orders_from_file(orders_file)
    matrix = sim.get_adjustedclose_matrix(orders)
    cash_matrix = sim.calculate_cash(matrix, 50000, orders_file)
    values_file = "event_values.csv"
    sim.cash_to_csv(values_file,cash_matrix)
    
    analyzer = Analyze()
    values_file = "event_values.csv"
    filename = values_file
    ports = analyzer.portfolio_from_file(filename)
    timestamps = list([i for i in ports.index])
    timestamps.sort()
    vol, daily_ret, sharpe, cum_ret = analyzer.benchmark(["$SPX"], timestamps)
    p2 = analyzer.read_values(filename)
    pt_volatility, pt_daily_return, pt_sharpe_ratio, pt_cumulative_return = analyzer.simulate(p2)
    
    print "Market Sharpe Ratio", sharpe
    print "Market vol", vol
    print "Market daily_ret", daily_ret
    print "Market cum_ret", cum_ret
    
    print ""
    
    print "Fund Sharpe Ratio", pt_sharpe_ratio
    print "Fund pt_volatility", pt_volatility
    print "Fund pt_daily_return", pt_daily_return
    print "Fund pt_cumulative_return", pt_cumulative_return
    
    
    
    
    