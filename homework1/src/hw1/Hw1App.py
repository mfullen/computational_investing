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
import itertools 

class Hw1App(object):
    def __init__(self):
        self.timeofday = dt.timedelta(hours=16)
        self.c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)
        self.ldf_data = None
        self.d_data = None
        
    def find_sum_in_list(self,numbers, target, length):
        results = []
        for x in range(len(numbers)):
            results.extend(
                [   
                    #combo for combo in itertools.permutations(numbers , x)  
                    combo for combo in itertools.product(numbers, repeat=4)  
                        if (sum(combo) == target and len(combo) == length)
                ]   
            )   
    
        return results
   
              
    def optimize(self, startDate, endDate, symbols):
        
        allocations = self.find_sum_in_list(range(0,10), 10, len(symbols))
        allocations = np.array(allocations)
        allocations = allocations / 10.0
        sharpe_ratios = []
        
        for i in range(0, len(allocations)):
            vol, daily_ret, sharpe, cum_ret = self.simulate(startDate,endDate, symbols, allocations[i])
            sharpe_ratios.append(sharpe)
            print(str(allocations[i]) + "sharpe: " + str(sharpe))
        
        #print(max(sharpe_ratios))
        return max(sharpe_ratios)
    
    
    def simulate(self, startDate, endDate, symbols, allocations):
        
        ldt_timestamps = du.getNYSEdays(startDate, endDate, self.timeofday)
        
        ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
        if(self.ldf_data == None):
            self.ldf_data = self.c_dataobj.get_data(ldt_timestamps, symbols, ls_keys)
            
        if(self.d_data == None):    
            d_data = dict(zip(ls_keys, self.ldf_data))
        
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
    
    



