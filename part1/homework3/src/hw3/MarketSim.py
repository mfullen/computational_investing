'''
Created on Sep 28, 2013

@author: mfullen
'''
import csv
import math

from BankAccount import BankAccount
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
        row = cash_matrix['cash']
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
    
    def proccess_market_transaction(self,account,orders, matrix):
        orders.sort(key=lambda x: x.order_date)
        timestamps = list([o.get_order_date() for o in orders])
        timestamps.sort()
        columns = ['cash']
        df_cash = pd.DataFrame(index = timestamps, columns=columns)
        df_cash = df_cash.fillna(0)
        cash = [self.process_money(account,order.get_action(),order.get_number_of_shares() * matrix.ix[order.get_order_date().strftime("%Y-%m-%d")][order.get_symbol()][0]) for order in orders]

        '''
        for i in range(0,len(orders)):
            print str(i) + ": ==========================================="
            
            print orders[i].get_symbol()
            print matrix.ix[orders[i].get_order_date().strftime("%Y-%m-%d")]
            print matrix.ix[orders[i].get_order_date().strftime("%Y-%m-%d")][orders[i].get_symbol()][0]
            print orders[i].get_number_of_shares()
            print order.get_number_of_shares() * matrix.ix[orders[i].get_order_date().strftime("%Y-%m-%d")][orders[i].get_symbol()][0]
            print "==========================================="
        '''
        i= 0
        for c in cash:
            df_cash.ix[i,0] = c
            i +=1
        
        #remove duplicate date indexes
        df_cash["index"] = df_cash.index
        df_cash.drop_duplicates(cols='index', take_last=True, inplace=True)
        del df_cash["index"]

        return df_cash
  
    def process_money(self, account, action, num):
        if(action == 'Buy'):
                return account.withdraw(num)
        elif (action== 'Sell'):
                return account.deposit(num)
  
if __name__ == "__main__":
    sim = MarketSim()
    orders = sim.orders_from_file("orders.csv")
    matrix = sim.get_adjustedclose_matrix(orders)
    account = BankAccount()
    account.deposit(1000000)
    print account.get_balance()
    cash_matrix = sim.proccess_market_transaction(account,orders, matrix)
    sim.cash_to_csv("values.csv",cash_matrix)
    print "Account Balance"
    print account.get_balance()

