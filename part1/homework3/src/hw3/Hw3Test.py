'''
Created on Sep 28, 2013

@author: ifull
'''
import unittest
from MarketSim import MarketSim
from BankAccount import BankAccount
import math
class Hw3Test(unittest.TestCase):


    def testExample1(self):
        sim = MarketSim()
        orders = sim.orders_from_file("orders.csv")
        matrix = sim.get_adjustedclose_matrix(orders)
        account = BankAccount()
        account.deposit(1000000)
        print account.get_balance()
        sim.proccess_market_transaction(account,orders, matrix)
        self.assertEqual(1133860, account.get_balance(), "The balance doesn't match the expected value")
    
    def testExample2(self):
        sim = MarketSim()
        orders = sim.orders_from_file("orders2.csv")
        matrix = sim.get_adjustedclose_matrix(orders)
        account = BankAccount()
        account.deposit(1000000)
        print account.get_balance()
        sim.proccess_market_transaction(account,orders, matrix)
        self.assertEqual(1078753, math.ceil(account.get_balance()), "The balance (" + str(account.get_balance()) +") doesn't match the expected value")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Hw3Test.testExample1']
    unittest.main()