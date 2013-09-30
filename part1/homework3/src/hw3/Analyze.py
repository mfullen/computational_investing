'''
Created on Sep 28, 2013

@author: mfullen
'''
import csv
import math

import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
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
        
        # clean up unused columns
        del(trades['year'])
        del(trades['month'])
        del(trades['day'])
        
        trades = trades.set_index(trades['date'])
        del(trades['date'])
        return trades

    def __init__(self):
        '''
        Constructor
        '''
        
    def simulate(self,ports):
        #adjusted = ports['cum_port'].values.reshape((len(ports['cum_port']), 1))
        #print ports
        #ports = ports.fillna(method='ffill')
        #ports = ports.fillna(method='bfill')
        adjusted = ports['cum_port'].values.reshape((len(ports['cum_port']), 1))
        adjusted = [a[0] for a in adjusted if(a != 0)]
        adjusted= np.array(adjusted).reshape((len(adjusted),1))
        print adjusted
        normalized = adjusted / adjusted[0,:]
        #print normalized
        #calculate daily return, [252,1]
        daily_ret_matrix = np.zeros((len(normalized) , 1)) 
        
        df_rets = adjusted.copy()
        # Filling the data.
        #df_rets = df_rets.fillna(method='ffill')
        #df_rets = df_rets.fillna(method='bfill')
        
        # Numpy matrix of filled data values
        na_rets = df_rets
        na_rets = na_rets / na_rets[0, :]
        
        #print na_rets
        
        na_portrets = np.sum(na_rets, axis=1)
        
        #print na_portrets
        cum_ret = na_portrets[-1]
        tsu.returnize0(na_portrets)
    
        print na_portrets
        # Statistics to calculate
        stddev = np.std(na_portrets)
        daily_ret = np.mean(na_portrets)
        sharpe = (np.sqrt(252) * daily_ret) / stddev
    
        # Return all the variables
        return stddev, daily_ret, sharpe, cum_ret
        
        '''for i in range(1, len(na_rets)): 
            if(na_rets[i] != 0 and na_rets[i-1] != 0):
                daily_ret_matrix[i-1] = (na_rets[i] / na_rets[i-1]) - 1 
        
        #print daily_ret_matrix
            
        #calculate cumulative daily return, [252,1]
        volatility = daily_ret_matrix.std()
        daily_return = np.mean(daily_ret_matrix)
        sharpe_ratio = math.sqrt(252) * daily_return / volatility
        cumulative_return = na_rets[len(na_rets)-1][0]
        
        return volatility, daily_return, sharpe_ratio, cumulative_return
        '''
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
    ports = analyzer.portfolio_from_file("values2.csv")
    timestamps = list([i for i in ports.index])
    timestamps.sort()
    #print timestamps
    volatility, daily_return, sharpe_ratio, cumulative_return = analyzer.benchmark(["$SPX"], timestamps)
    volatility, daily_return, sharpe_ratio, cumulative_return = analyzer.simulate(ports)
    print volatility
    print daily_return
    print sharpe_ratio
    print cumulative_return