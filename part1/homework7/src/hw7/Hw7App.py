'''
Created on Oct 22, 2013

@author: mfullen
'''
import csv
import copy

import QSTK.qstkstudy.EventProfiler as ep
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import datetime as dt
from hw5.Main import Hw5App
from hw3.MarketSim import MarketSim
from hw3.Analyze import Analyze
import numpy as np

class Hw7App(object):
    
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
        filename = "event_orders.csv"
        with open(filename, 'wb') as w:
            for s_sym in ls_symbols:
                for i in range(1, len(ldt_timestamps)):
                    # Calculating the returns for this timestamp
                    f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
                    f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
                    f_marketprice_today = ts_market.ix[ldt_timestamps[i]]
                    f_marketprice_yest = ts_market.ix[ldt_timestamps[i - 1]]
                    f_cutoff = -2.0
                    market_cutoff = 1.0
                    if f_symprice_today <= f_cutoff and f_symprice_yest >= f_cutoff and f_marketprice_today >= market_cutoff:
                        df_events[s_sym].ix[ldt_timestamps[i]] = 1
                        buy_date = ldt_timestamps[i]
                        event_sym = s_sym
                        sell_date = ldt_timestamps[i]
                        if((i+ 5) >= len(ldt_timestamps)):
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

    app7 = Hw7App()
    #df_events = app7.find_events(ls_symbols, bollinger_val)

    orders_file = "event_orders.csv"
    sim = MarketSim()
    orders = sim.orders_from_file(orders_file)
    matrix = sim.get_adjustedclose_matrix(orders)
    cash_matrix = sim.calculate_cash(matrix, 100000, orders_file)
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