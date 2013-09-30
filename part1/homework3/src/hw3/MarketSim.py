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

        #print df_cash
        return df_cash
  
    def process_money(self, account, action, num):
        if(action == 'Buy'):
                return account.withdraw(num)
        elif (action== 'Sell'):
                return account.deposit(num)
            
    def do_It(self,matrix,orders,account,df_cash):
        orders.sort(key=lambda x: x.order_date)
        #copy matrix shape
        own = matrix.copy()
        #set all owned shares to 0
        own = own.ix[0:] * 0
        
        for order in orders:
            symbol = order.get_symbol()
            date = order.get_order_date()
            shares = order.get_number_of_shares()
            action = order.get_action()
            
            if(action == 'Buy'):
                own.ix[date.strftime("%Y-%m-%d")][symbol] += shares*1.0
                
            elif (action== 'Sell'):
                own.ix[date.strftime("%Y-%m-%d")][symbol] += shares*-1.0
                
            value = own.ix[date.strftime("%Y-%m-%d")][symbol][0]
            #print value
            own.ix[date.strftime("%Y-%m-%d"):][symbol] = value

        '''
        print "===================="
        print own.ix[0:]
        print "===================="
        print "===================="
        print own.ix[0:]['AAPL']
        print "===================="
        print "================="
        print own.ix[0:]['GOOG'][0]
        '''
        '''
        print own.ix[0:]['AAPL']
        print "==================================================================="
        print own.ix[0:]['IBM']
        print "==================================================================="
        print own.ix[0:]['GOOG']
        print "==================================================================="
        print own.ix[0:]['XOM']
        print "==================================================================="
        '''

        print "==============Prices========================" 
        print matrix.ix[0:20]
        print matrix.ix[220:240]
        print "==============Shares========================" 
        print own.ix[0:20]
        print own.ix[220:240]
        print "==============Values========================" 
        values = own * matrix
        print values.ix[0:20]
        print values.ix[220:240]
       
        print "FOR LOOP" 

        cums = []
        ts = []
        for i in values.index:
            #row = cash_matrix['cash']
            #print row.index[i]
            cum = 0
            for sy in values:
                cum += values[i.strftime("%Y-%m-%d")].ix[0][sy]
            #print cum
            ts.append(i)
            cums.append(cum)

        #print cums
        cums = np.array(cums).reshape((len(values),1))
        #ts = list(np.array(ts).reshape((len(values),1)))
        print cums
        index = pd.DatetimeIndex(ts)
        df_cums = pd.DataFrame(cums, index=index, columns=['cums'])
        print df_cums.ix[0:20]
        
        
        
        lols = np.zeros((len(values),1))
        
        #lols = np.array(lols).reshape((len(row),1))
        print lols
        df_real_cash = pd.DataFrame(lols,index=index, columns=['cash'])
        print df_real_cash
        
        row =  df_cash['cash']
        for i in range(0,len(row)):
            row_index = row.index[i]
            #print row_index
            df_real_cash.ix[row_index.strftime("%Y-%m-%d")]= row.ix[row_index.strftime("%Y-%m-%d")]
        
        print df_real_cash.ix[0:20]
        
        print "Cums + cash"
        total_cash = (df_cums['cums'] + df_real_cash['cash'])
        print total_cash.ix[230:250]
        
        return total_cash
       
        
        '''
        print values1.ix[0:]['AAPL'][0]
        print values1.ix[0:]['GOOG'][0]
        print values1.ix[0:]['IBM'][0]
        print values1.ix[0:]['XOM'][0]
        print values1.cumsum(axis=0).ix[-1]
        '''
        
        
        '''
        cash = matrix.copy()
        cash = cash.ix[0:] * 0
        cash.ix[0:]['AAPL'][0] = account.get_balance()
        #print cash.ix[0:]['AAPL']
        print "ORDERS-----------------------"
        for order in orders:
            symbol = order.get_symbol()
            date = order.get_order_date()
            shares = order.get_number_of_shares()
            action = order.get_action()
            shares_owned = own.ix[date.strftime("%Y-%m-%d")][symbol][0]
            price = matrix.ix[date.strftime("%Y-%m-%d")][symbol][0] 

            print "Date: " + date.strftime("%Y-%m-%d")
            
            myCash = cash.ix[date.strftime("%Y-%m-%d")]['AAPL'][0]
            print "My Cash: " + str(myCash)
            myCash -= (shares_owned * price)
            cash.ix[date.strftime("%Y-%m-%d"):]['AAPL'] = myCash
            
            print "Symbol: " + str(symbol)
            print "Action: " + str(action)
            print "PRICE: " + str(price)
            print "Shares Owned: " + str(shares_owned)
            print "Value: " + str(shares_owned*price)
            print "After Trade Cash: " + str(myCash)
            print "=============================="
        print " ------------------------------------------------------------"
        print cash.ix[0:]['AAPL']
        
       
        #print np.cumsum(own,axis=1)
        '''
        
  
if __name__ == "__main__":
    sim = MarketSim()
    orders = sim.orders_from_file("orders.csv")
    matrix = sim.get_adjustedclose_matrix(orders)

    account = BankAccount()
    account.deposit(1000000)
    print account.get_balance()
    
    
    cash_matrix = sim.proccess_market_transaction(account,orders, matrix)
    cash_matrix = sim.do_It(matrix,orders,account,cash_matrix)
    sim.cash_to_csv("values.csv",cash_matrix)
    print "Account Balance"
    print account.get_balance()

