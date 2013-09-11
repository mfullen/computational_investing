import QSTK
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import math
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from compiler import symbols

class Hw1App(object):
    
    
    def simulate(self, startDate, endDate, symbols, allocations):
        
        timeofday = dt.timedelta(hours=16)
        ldt_timestamps = du.getNYSEdays(startDate, endDate, timeofday)
        
        c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)
        ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
        ldf_data = c_dataobj.get_data(ldt_timestamps, symbols, ls_keys)
        d_data = dict(zip(ls_keys, ldf_data))
        
        adjusted_closing_price = d_data['close'].values
        normalized_closing_price = adjusted_closing_price / adjusted_closing_price[0,:]
        
        #allocated matrix [252, 4]
        allocated_matrix = normalized_closing_price.copy()
        for col in range(0, len(allocations)):
            for row in range(0, len(allocated_matrix)):
                allocated_matrix[row][col] = allocated_matrix[row][col] * allocations[col]
        

        #sum up the rows of allocated matrix to get cumulative return matrix. [252,1]
        cumulative_return_matrix = np.zeros((len(allocated_matrix), 1))
        for row in range(0, len(allocated_matrix)):
            for col in range(0, len(allocations)):
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
    
    



