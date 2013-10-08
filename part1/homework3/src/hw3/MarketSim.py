'''
Created on Sep 28, 2013

@author: mfullen
'''
import csv
import math

from Order import Order
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import numpy as np
import pandas as pd


class MarketSim(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def orders_from_file(self,filename):
        reader = csv.reader(open(filename, 'rU'), delimiter = ',')
        orders = []
        for row in reader:
            year = int(row[0])
            month = int(row[1])
            day = int(row[2])
            symbol = row[3]
            action = row[4]
            quant = int(row[5])
            order = Order(dt.datetime(year,month,day),symbol, action, quant)
            orders.append(order)
        return orders
    
    def cash_to_csv(self,filename, cash_matrix):
        writer = csv.writer(open(filename, 'wb'),delimiter=',')
        print "CSV======================="
        print cash_matrix
        row = cash_matrix
        for i in range(0,len(row)):
            row_index = row.index[i]
            csv_row = [row_index.strftime("%Y"), row_index.strftime("%m"), row_index.strftime("%d"), math.ceil(row[i])]
            print csv_row
            writer.writerow(csv_row)       
            
    def get_adjustedclose_matrix(self, orders):
        timestamps = list(set([o.get_order_date() for o in orders]))
        timestamps.sort()
        symbols = list(set([o.get_symbol() for o in orders]))
        timeofday = dt.timedelta(hours=16)
        c_dataobj = da.DataAccess('Yahoo')
        ls_keys = ['close']
        
        ldt_timestamps = du.getNYSEdays(timestamps[0], timestamps[-1] + dt.timedelta(days=1), timeofday)
        ldf_data = c_dataobj.get_data(ldt_timestamps, symbols, ls_keys)
        d_data = dict(zip(ls_keys, ldf_data))
        
        adjusted_closing_price = d_data['close']

        return adjusted_closing_price
    
    def calculate_cash(self,price_matrix, start_money, filename):
        orders = pd.read_csv(filename, names=['year', 'month', 'day', 'symbol', 'sell_or_buy', 'quantity', 'empty'], parse_dates={'datetime':['year', 'month', 'day']})
        orders['symbol'].drop_duplicates().reset_index(drop=True)
        orders['sell_or_buy'] = 2*(orders['sell_or_buy'] == 'Buy')-1
        
        dates = list(set(orders['datetime'].tolist()))
        all_dates = du.getNYSEdays(min(dates), max(dates)+ dt.timedelta(days=1), dt.timedelta(hours=16))
        symbols = list(set(orders['symbol']))
         
        trade = price_matrix.copy()
        trade *= 0

        i = 0
        for col in orders.index:
            sym = orders.ix[col]['symbol']
            date = orders.ix[col]['datetime'].strftime("%Y-%m-%d")
            sell_or_buy = orders.ix[col]['sell_or_buy']
            shares = orders.ix[col]['quantity']
            trade_exists = trade.ix[date][sym][0] != 0
            
            if(trade_exists):
                trade.ix[date][sym][0] = (sell_or_buy * shares) + trade.ix[date][sym][0]
            else:
                trade.ix[date][sym][0] = sell_or_buy * shares
            i= i + 1
       
        value = trade * price_matrix
       
        np_zeroc = np.zeros(len(all_dates) )
        ts_values = pd.Series(np_zeroc, index=all_dates)
        value['_TOTAL'] = ts_values
        value = value.cumsum(axis=1)
        
        np_zeroc = np.zeros(len(all_dates) )
        ts_cash = pd.Series(np_zeroc, index=all_dates)
        
        yesterdays_cash = start_money
       
        for i in all_dates:
            d = i.strftime("%Y-%m-%d")
            #print "Start Day: " + d
            todays_cash = 0.0
            for sym in symbols:
                todays_cash -=  trade.ix[d][sym][0] * price_matrix[d][sym][0]   
            ts_cash[i] = todays_cash + yesterdays_cash
            yesterdays_cash = ts_cash[i]
        
        price_matrix['_CASH'] = 1.0
        trade['_CASH'] = ts_cash
        holdingMatrix = trade.cumsum()
       
        np_zeroc = np.zeros(len(all_dates) )
        ts_final = pd.Series(np_zeroc, index=all_dates)

        for i in all_dates:
            d = i.strftime("%Y-%m-%d")
            todays_cash = 0.0
            for sym in symbols:
                todays_cash +=  holdingMatrix.ix[d][sym][0] * price_matrix[d][sym][0]   
            ts_final[i] = todays_cash + (ts_cash.ix[d][0])
        return ts_final

  
if __name__ == "__main__":
    sim = MarketSim()
    filename = "quiz-orders2.csv"
    orders = sim.orders_from_file(filename)
    matrix = sim.get_adjustedclose_matrix(orders)
    x = sim.calculate_cash(matrix, 1000000, filename)
    sim.cash_to_csv("values.csv",x)


