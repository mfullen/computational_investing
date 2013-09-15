'''
Created on Sep 9, 2013

Description: Homework Assignment 1 from Computational Investing Part 1 on Coursera.com

@author: mfullen
'''
import unittest

import datetime as dt
from hw1.Hw1App import Hw1App


class TestHw1(unittest.TestCase):


    def testExampleOutput1(self):
        print("===============testExampleOutput1===============")
        app = Hw1App()
        vol, daily_ret, sharpe, cum_ret = app.simulate(startDate= dt.datetime(2011,1,1),
                     endDate= dt.datetime(2011,12,31),
                     symbols=['AAPL', 'GLD', 'GOOG', 'XOM'],
                     allocations=[0.4, 0.4, 0.0, 0.2])
        self.assertAlmostEqual(1.02828403099, sharpe, 7,"Result Sharpe Ratio: " + str(sharpe) +" is incorrect", delta=None)
        self.assertAlmostEqual(vol, 0.0101467067654, 7, "Volatility (stdev of daily returns) " + str(vol) +" is incorrect", delta=None)
        self.assertAlmostEqual(daily_ret, 0.000657261102001, 7, "Average Daily Return " + str(daily_ret) +" is incorrect", delta=None)
        self.assertAlmostEqual(cum_ret, 1.16487261965,7, "Result: " + str(cum_ret) +" doesn't match expected Cumulative Return", delta=None)
       
        
    def testExampleOutput2(self):
        print("===============testExampleOutput2===============")
        app = Hw1App()
        vol, daily_ret, sharpe, cum_ret = app.simulate(startDate= dt.datetime(2010,1,1),
                     endDate= dt.datetime(2010,12,31),
                     symbols=['AXP', 'HPQ', 'IBM', 'HNZ'],
                     allocations=[0.0, 0.0, 0.0, 1.0])
        self.assertAlmostEqual(1.29889334008, sharpe, 7,"Result Sharpe Ratio: " + str(sharpe) +" is incorrect", delta=None)
        self.assertAlmostEqual(vol, 0.00924299255937, 7, "Volatility (stdev of daily returns) " + str(vol) +" is incorrect", delta=None)
        self.assertAlmostEqual(daily_ret, 0.000756285585593, 7, "Average Daily Return " + str(daily_ret) +" is incorrect", delta=None)
        self.assertAlmostEqual(cum_ret, 1.1960583568, 7, "Cumulative Return " + str(cum_ret) +" is incorrect", delta=None)
    
    def testOptimizeQuizQuestion1(self):
        print("===============testOptimizeQuizQuestion1===============")
        app = Hw1App()
        sharpe, allocation = app.optimize(startDate= dt.datetime(2011,1,1), endDate= dt.datetime(2011,12,31),
                     symbols=['AAPL', 'GOOG', 'IBM', 'MSFT'])
        print(sharpe)
        print(allocation)
        self.assertAlmostEqual(1.19360525401, sharpe, 7,"Result Sharpe Ratio: " + str(sharpe) +" is incorrect", delta=None)
         
    def testOptimizeQuizQuestion2(self):
        print("===============testOptimizeQuizQuestion2===============")
        app = Hw1App()
        sharpe, allocation = app.optimize(startDate= dt.datetime(2010,1,1), endDate= dt.datetime(2010,12,31),
                     symbols= ['BRCM', 'TXN', 'IBM', 'HNZ'] )
        print(sharpe)
        print(allocation)
        self.assertAlmostEqual(1.38514235431, sharpe, 7,"Result Sharpe Ratio: " + str(sharpe) +" is incorrect", delta=None)
        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'TestHw1.testName']
    unittest.main()
