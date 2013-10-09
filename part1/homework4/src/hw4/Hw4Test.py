'''
Created on Oct 8, 2013

@author: mfullen
'''
import unittest
import datetime as dt
from hw4.Hw4App import Hw4App
from hw3.MarketSim import MarketSim
from hw3.Analyze import Analyze


class Hw4UnitTest(unittest.TestCase):


    def testExample1(self):
        dt_start = dt.datetime(2008, 1, 1)
        dt_end = dt.datetime(2009, 12, 31)
        symbols_list = 'sp5002012'
        event_price = 5.0
        
        app = Hw4App()
        app.event_study(dt_start, dt_end, symbols_list, event_price)
        
        orders_file = "event_orders.csv"
        sim = MarketSim()
        orders = sim.orders_from_file(orders_file)
        matrix = sim.get_adjustedclose_matrix(orders)
        cash_matrix = sim.calculate_cash(matrix, 50000, orders_file)
        values_file = "event_values.csv"
        sim.cash_to_csv(values_file,cash_matrix)
        
        analyzer = Analyze()
        filename = values_file
        ports = analyzer.portfolio_from_file(filename)
        timestamps = list([i for i in ports.index])
        timestamps.sort()
        vol, daily_ret, sharpe, cum_ret = analyzer.benchmark(["$SPX"], timestamps)
        
        p2 = analyzer.read_values(filename)
        pt_volatility, pt_daily_return, pt_sharpe_ratio, pt_cumulative_return = analyzer.simulate(p2)
        
        self.assertAlmostEqual(-0.184202673931, sharpe, 7,"Result Sharpe Ratio: " + str(sharpe) +" is incorrect", delta=None)
        self.assertAlmostEqual(0.022004631521,vol, 7, "Volatility (stdev of daily returns) " + str(vol) +" is incorrect", delta=None)
        self.assertAlmostEqual(-0.000255334653467, daily_ret, 7, "Average Daily Return " + str(daily_ret) +" is incorrect", delta=None)
        self.assertAlmostEqual(0.779305674563, cum_ret,7, "Result: " + str(cum_ret) +" doesn't match expected Cumulative Return", delta=None)
        
        self.assertAlmostEqual(0.527865227084, pt_sharpe_ratio, 6,"Result Sharpe Ratio: " + str(pt_sharpe_ratio) +" is incorrect", delta=None)
        self.assertAlmostEqual(0.0060854156452, pt_volatility, 7, "Volatility (stdev of daily returns) " + str(pt_volatility) +" is incorrect", delta=None)
        self.assertAlmostEqual(0.000202354576186, pt_daily_return, 7, "Average Daily Return " + str(pt_daily_return) +" is incorrect", delta=None)
        self.assertAlmostEqual(1.09648,pt_cumulative_return,7, "Result: " + str(pt_cumulative_return) +" doesn't match expected Cumulative Return", delta=None)
    
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Hw4UnitTest.testExample1']
    unittest.main()