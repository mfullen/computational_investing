'''
Created on Sep 28, 2013

@author: mfullen
'''
import math
import unittest

from Analyze import Analyze
from MarketSim import MarketSim


class Hw3Test(unittest.TestCase):


    def testExample1(self):
        print("===============testExample1===============")
        orders_file = "orders.csv"
        sim = MarketSim()
        orders = sim.orders_from_file(orders_file)
        matrix = sim.get_adjustedclose_matrix(orders)
        cash_matrix = sim.calculate_cash(matrix, 1000000, orders_file)
        sim.cash_to_csv("values1.csv",cash_matrix)
        self.assertEqual(1133860, cash_matrix[-1], "The balance doesn't match the expected value")
    
    def testExample2(self):
        print("===============testExample2===============")
        orders_file = "orders2.csv"
        sim = MarketSim()
        orders = sim.orders_from_file(orders_file)
        matrix = sim.get_adjustedclose_matrix(orders)
        cash_matrix = sim.calculate_cash(matrix, 1000000, orders_file)
        sim.cash_to_csv("values2.csv",cash_matrix)
        self.assertEqual(1078753, math.ceil(cash_matrix[-1]), "The balance (" + str(cash_matrix[-1]) +") doesn't match the expected value")
    
    def testExample1Part2(self):
        print("===============testExample1Part2===============")
        analyzer = Analyze()
        filename = "values1.csv"
        ports = analyzer.portfolio_from_file(filename)
        timestamps = list([i for i in ports.index])
        timestamps.sort()
        vol, daily_ret, sharpe, cum_ret = analyzer.benchmark(["$SPX"], timestamps)

        self.assertAlmostEqual(0.0183391412227, sharpe, 7,"Result Sharpe Ratio: " + str(sharpe) +" is incorrect", delta=None)
        self.assertAlmostEqual(0.0149090969828, vol, 7, "Volatility (stdev of daily returns) " + str(vol) +" is incorrect", delta=None)
        self.assertAlmostEqual(1.72238432443e-05, daily_ret, 7, "Average Daily Return " + str(daily_ret) +" is incorrect", delta=None)
        self.assertAlmostEqual(0.97759401457,cum_ret,7, "Result: " + str(cum_ret) +" doesn't match expected Cumulative Return", delta=None)
        
        p2 = analyzer.read_values(filename)
        pt_volatility, pt_daily_return, pt_sharpe_ratio, pt_cumulative_return = analyzer.simulate(p2)
        
        self.assertAlmostEqual(1.21540462111, pt_sharpe_ratio, 7,"Result Sharpe Ratio: " + str(pt_sharpe_ratio) +" is incorrect", delta=None)
        self.assertAlmostEqual(0.00717514512699, pt_volatility, 7, "Volatility (stdev of daily returns) " + str(pt_volatility) +" is incorrect", delta=None)
        self.assertAlmostEqual(0.000549352749569, pt_daily_return, 7, "Average Daily Return " + str(pt_daily_return) +" is incorrect", delta=None)
        self.assertAlmostEqual(1.13386,pt_cumulative_return,7, "Result: " + str(pt_cumulative_return) +" doesn't match expected Cumulative Return", delta=None)
    
    def testExample2Part2(self):
        print("===============testExample2Part2===============")
        analyzer = Analyze()
        filename = "values2.csv"
        ports = analyzer.portfolio_from_file(filename)
        timestamps = list([i for i in ports.index])
        timestamps.sort()
        vol, daily_ret, sharpe, cum_ret = analyzer.benchmark(["$SPX"], timestamps)

        self.assertAlmostEqual(-0.177204632551, sharpe, 7,"Result Sharpe Ratio: " + str(sharpe) +" is incorrect", delta=None)
        self.assertAlmostEqual(0.0149914504972,vol, 7, "Volatility (stdev of daily returns) " + str(vol) +" is incorrect", delta=None)
        self.assertAlmostEqual(-0.000167347202139, daily_ret, 7, "Average Daily Return " + str(daily_ret) +" is incorrect", delta=None)
        self.assertAlmostEqual(0.937041848381, cum_ret,7, "Result: " + str(cum_ret) +" doesn't match expected Cumulative Return", delta=None)
        
        p2 = analyzer.read_values(filename)
        pt_volatility, pt_daily_return, pt_sharpe_ratio, pt_cumulative_return = analyzer.simulate(p2)
        
        self.assertAlmostEqual(0.788988545538, pt_sharpe_ratio, 6,"Result Sharpe Ratio: " + str(pt_sharpe_ratio) +" is incorrect", delta=None)
        self.assertAlmostEqual(0.00708034656073, pt_volatility, 7, "Volatility (stdev of daily returns) " + str(pt_volatility) +" is incorrect", delta=None)
        self.assertAlmostEqual(0.000351904599618, pt_daily_return, 7, "Average Daily Return " + str(pt_daily_return) +" is incorrect", delta=None)
        self.assertAlmostEqual(1.078753,pt_cumulative_return,7, "Result: " + str(pt_cumulative_return) +" doesn't match expected Cumulative Return", delta=None)
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Hw3Test.testExample1']
    unittest.main()