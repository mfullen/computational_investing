'''
Created on Sep 28, 2013

@author: mfullen
'''
import math
import unittest

from Analyze import Analyze
from BankAccount import BankAccount
from MarketSim import MarketSim


class Hw3Test(unittest.TestCase):


    def testExample1(self):
        print("===============testExample1===============")
        sim = MarketSim()
        orders = sim.orders_from_file("orders.csv")
        matrix = sim.get_adjustedclose_matrix(orders)
        account = BankAccount()
        account.deposit(1000000)
        cash_matrix = sim.proccess_market_transaction(account,orders, matrix)
        sim.cash_to_csv("values1.csv",cash_matrix)
        self.assertEqual(1133860, account.get_balance(), "The balance doesn't match the expected value")
    
    def testExample2(self):
        print("===============testExample2===============")
        sim = MarketSim()
        orders = sim.orders_from_file("orders2.csv")
        matrix = sim.get_adjustedclose_matrix(orders)
        account = BankAccount()
        account.deposit(1000000)
        cash_matrix = sim.proccess_market_transaction(account,orders, matrix)
        sim.cash_to_csv("values2.csv",cash_matrix)
        self.assertEqual(1078753, math.ceil(account.get_balance()), "The balance (" + str(account.get_balance()) +") doesn't match the expected value")
    
    def testExample1Part2(self):
        print("===============testExample1Part2===============")
        analyzer = Analyze()
        ports = analyzer.portfolio_from_file("values1.csv")
        timestamps = list([ports.ix[i]['date'] for i in ports.index])
        timestamps.sort()
        vol, daily_ret, sharpe, cum_ret = analyzer.benchmark(["$SPX"], timestamps)

        self.assertAlmostEqual(0.0183391412227, sharpe, 7,"Result Sharpe Ratio: " + str(sharpe) +" is incorrect", delta=None)
        self.assertAlmostEqual(vol, 0.0149090969828, 7, "Volatility (stdev of daily returns) " + str(vol) +" is incorrect", delta=None)
        self.assertAlmostEqual(daily_ret, 1.72238432443e-05, 7, "Average Daily Return " + str(daily_ret) +" is incorrect", delta=None)
        self.assertAlmostEqual(cum_ret, 0.97759401457,7, "Result: " + str(cum_ret) +" doesn't match expected Cumulative Return", delta=None)
    
    def testExample2Part2(self):
        print("===============testExample2Part2===============")
        analyzer = Analyze()
        ports = analyzer.portfolio_from_file("values2.csv")
        timestamps = list([ports.ix[i]['date'] for i in ports.index])
        timestamps.sort()
        vol, daily_ret, sharpe, cum_ret = analyzer.benchmark(["$SPX"], timestamps)

        self.assertAlmostEqual(-0.177204632551, sharpe, 7,"Result Sharpe Ratio: " + str(sharpe) +" is incorrect", delta=None)
        self.assertAlmostEqual(vol, 0.0149914504972, 7, "Volatility (stdev of daily returns) " + str(vol) +" is incorrect", delta=None)
        self.assertAlmostEqual(daily_ret, -0.000167347202139, 7, "Average Daily Return " + str(daily_ret) +" is incorrect", delta=None)
        self.assertAlmostEqual(cum_ret, 0.937041848381,7, "Result: " + str(cum_ret) +" doesn't match expected Cumulative Return", delta=None)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Hw3Test.testExample1']
    unittest.main()