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

    def read_values(self,valuesfile):
        """Read values to a Panda DataFrame"""
    
        li_cols = [0, 1, 2, 3]
        ls_names = ['YEAR', 'MONTH', 'DAY', 'TOTAL']
        d_date_columns = { 'DATE': ['YEAR', 'MONTH', 'DAY']}
        s_index_column = 'DATE'
        df_values = pd.read_csv(valuesfile, \
                                dtype={'TOTAL': np.float64}, \
                                sep=',', \
                                comment='#', \
                                skipinitialspace=True, \
                                header=None, \
                                usecols=li_cols, \
                                names=ls_names, \
                                parse_dates=d_date_columns, \
                                index_col=s_index_column)
        if not df_values.index.is_monotonic:
            df_values.sort_index(inplace=True)
    
        return df_values
    
    def __init__(self):
        '''
        Constructor
        '''
        
    def simulate(self,ports):
        # Extract just the data (as floating point values)
        na_values = ports.values * 1.0
    
        # Normalize
        na_norm_values = na_values / na_values[0, :]
    
        # Returnize the values
        na_returns = na_norm_values.copy()
        tsu.returnize0(na_returns)
    
        # Calculate statistical values
        daily_return = np.mean(na_returns)
        cumulative_return = np.prod(na_returns + 1.0)
        volatility = np.std(na_returns)
        sharpe_ratio = math.sqrt(252.0) * daily_return / volatility
        
        return volatility, daily_return, sharpe_ratio, cumulative_return
        
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
    filename = "values1.csv"
    ports = analyzer.portfolio_from_file(filename)
    timestamps = list([i for i in ports.index])
    timestamps.sort()
    #print timestamps
    #volatility, daily_return, sharpe_ratio, cumulative_return = analyzer.benchmark(["$SPX"], timestamps)
    
    p2 = analyzer.read_values(filename)
    volatility, daily_return, sharpe_ratio, cumulative_return = analyzer.simulate(p2)
    print volatility
    print daily_return
    print sharpe_ratio
    print cumulative_return