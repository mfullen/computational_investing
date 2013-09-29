'''
Created on Sep 28, 2013

@author: mfullen
'''

class BankAccount(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.total = 0.0
    
    def deposit(self, amount):
        self.total += amount
        return self.total
    
    def withdraw(self, amount):
        self.total -= amount
        return self.total
    
    def get_balance(self):
        return self.total
        
        