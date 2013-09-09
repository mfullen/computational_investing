'''
Created on Sep 9, 2013

Description: Homework Assignment 1 from Computational Investing Part 1 on Coursera.com

@author: mfullen
'''
import unittest
from hw1.Hw1App import Hw1App

class TestHw1(unittest.TestCase):

    def testExampleOutput0(self):
        app = Hw1App()
        vol, daily_ret, sharpe, cum_ret  = app.simulate(startDate="January 1, 2011", 
                     endDate="December 31, 2011", 
                     symbols=['AAPL', 'GLD', 'GOOG', 'XOM'], 
                     allocations=[0.4, 0.4, 0.0, 0.2])
        self.assertEqual(vol, 1, "Volatility (stdev of daily returns) is incorrect")
        self.assertEqual(daily_ret, 1, "Average Daily Return is incorrect")
        self.assertEqual(sharpe, 1, "Sharpe Ratio is incorrect")
        self.assertEqual(cum_ret, 1, "Cumulative Return is incorrect")

    def testExampleOutput1(self):
        app = Hw1App()
        vol, daily_ret, sharpe, cum_ret  = app.simulate(startDate="January 1, 2011", 
                     endDate="December 31, 2011", 
                     symbols=['AAPL', 'GLD', 'GOOG', 'XOM'], 
                     allocations=[0.4, 0.4, 0.0, 0.2])
        self.assertEqual(vol, 0.0101467067654, "Volatility (stdev of daily returns) is incorrect")
        self.assertEqual(daily_ret, 0.000657261102001, "Average Daily Return is incorrect")
        self.assertEqual(sharpe, 1.02828403099, "Sharpe Ratio is incorrect")
        self.assertEqual(cum_ret, 1.16487261965, "Cumulative Return is incorrect")
        
    def testExampleOutput2(self):
        app = Hw1App()
        vol, daily_ret, sharpe, cum_ret  = app.simulate(startDate="January 1, 2010", 
                     endDate="December 31, 2010", 
                     symbols=['AXP', 'HPQ', 'IBM', 'HNZ'], 
                     allocations=[0.0, 0.0, 0.0, 1.0])
        self.assertEqual(vol, 0.00924299255937, "Volatility (stdev of daily returns) is incorrect")
        self.assertEqual(daily_ret, 0.000756285585593, "Average Daily Return is incorrect")
        self.assertEqual(sharpe, 1.29889334008, "Sharpe Ratio is incorrect")
        self.assertEqual(cum_ret, 1.1960583568, "Cumulative Return is incorrect")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'TestHw1.testName']
    unittest.main()