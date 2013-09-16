'''
Created on Sep 15, 2013

Computational Investing Part 1 HW 2: Event Studies

@author: mfullen
'''
import unittest

import datetime as dt
from hw2.Hw2App import Hw2App

class Hw2Test(unittest.TestCase):


    def testExample1(self):
        print("======================testExample1===============")
        app = Hw2App()
        startDate = dt.datetime(2008,1,1)
        endDate = dt.datetime(2009,1,1)
        eventPrice = 5.0
        expectedEvents = 176
        resultEventNumber = app.calc_event_study(startDate,endDate,eventPrice)
        self.assertEqual(expectedEvents, resultEventNumber, "Events are not equal")

    def testExample2(self):
        print("======================testExample2===============")
        app = Hw2App()
        startDate = dt.datetime(2008,1,1)
        endDate = dt.datetime(2009,1,1)
        eventPrice = 5.0
        expectedEvents = 326
        resultEventNumber = app.calc_event_study(startDate,endDate,eventPrice)
        self.assertEqual(expectedEvents, resultEventNumber, "Events are not equal")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Hw2Test.testName']
    unittest.main()