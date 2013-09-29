'''
Created on Sep 28, 2013

@author: mfullen
'''
import csv
import math

import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import numpy as np
import pandas as pd


class Analyze(object):
    '''
    classdocs
    '''


    def portfolio_from_file(self,filename):
        # read the CSV with orders
        trades = pd.read_csv(filename, index_col=None, header=None, usecols=[0,1,2,3])
        # name the columns
        trades.columns = ['year','month','day','cum_port']
        # create a date object column for convenient comparison
        trades.insert(0, 'date', [dt.datetime(trades['year'][i],trades['month'][i],trades['day'][i],16,0,0) for i in trades.index])
        
        return trades

    def __init__(self):
        '''
        Constructor
        '''
        
    def simulate(self,ports):
        #ports.sort(key=lambda x: x.date)
        #print ports.ix[0]
        adjusted = ports['cum_port'].values.reshape((len(ports['cum_port']), 1))
        #print adjusted
        normalized = adjusted / adjusted[0,:]
        #print normalized
        #calculate daily return, [252,1]
        daily_ret_matrix = np.zeros((len(normalized) , 1)) 

        for i in range(1, len(normalized)): 
            daily_ret_matrix[i-1] = (normalized[i] / normalized[i-1]) - 1 
        
        print daily_ret_matrix
            
        #calculate cumulative daily return, [252,1]
        volatility = daily_ret_matrix.std()
        daily_return = np.mean(daily_ret_matrix)
        sharpe_ratio = math.sqrt(252) * daily_return / volatility
        cumulative_return = normalized[len(normalized)-1][0]
        
        print volatility
        print daily_return
        print sharpe_ratio
        print cumulative_return
        
    def benchmark(self, symbols,dates):
        ldt_timestamps = du.getNYSEdays(dates[0], dates[-1], dt.timedelta(hours=16))
        ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
        c_dataobj = da.DataAccess('Yahoo')
        #print symbols
        ldf_data = c_dataobj.get_data(ldt_timestamps, symbols, ls_keys)
        d_data = dict(zip(ls_keys,ldf_data))
        adjusted_closing_price = d_data['close'].values
        
        normalized_closing_price = adjusted_closing_price / adjusted_closing_price[0,:]
        
        #allocated matrix [252, 4]
        allocated_matrix = normalized_closing_price.copy()

        #sum up the rows of allocated matrix to get cumulative return matrix. [252,1]
        cumulative_return_matrix = np.zeros((len(allocated_matrix), 1))
        for row in range(0, len(allocated_matrix)):
            for col in range(0, 1):
                cumulative_return_matrix[row][0] = cumulative_return_matrix[row][0] + allocated_matrix[row][col]
        
        #calculate daily return, [252,1]
        daily_ret_matrix = np.zeros((len(cumulative_return_matrix) , 1)) 

        for i in range(1, len(cumulative_return_matrix)): 
            daily_ret_matrix[i-1] = (cumulative_return_matrix[i] / cumulative_return_matrix[i-1]) - 1 
            
        #calculate cumulative daily return, [252,1]
        volatility = daily_ret_matrix.std()
        daily_return = np.mean(daily_ret_matrix)
        sharpe_ratio = math.sqrt(252) * daily_return / volatility
        cumulative_return = cumulative_return_matrix[len(cumulative_return_matrix)-1][0]
        #cumulative_return = np.sum(cum_daily_return_matrix)
        
        return volatility, daily_return, sharpe_ratio, cumulative_return
        
        
if __name__ == "__main__":
    analyzer = Analyze()
    ports = analyzer.portfolio_from_file("values.csv")
    #analyzer.simulate(ports)
    timestamps = list([ports.ix[i]['date'] for i in ports.index])
    timestamps.sort()
    #print timestamps
    volatility, daily_return, sharpe_ratio, cumulative_return = analyzer.benchmark(["$SPX"], timestamps)
    print volatility
    print daily_return
    print sharpe_ratio
    print cumulative_return