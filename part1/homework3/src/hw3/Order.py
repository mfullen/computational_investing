'''
Created on Sep 28, 2013

@author: mfullen
'''

class Order(object):
    '''
    classdocs
    '''
   
    def __init__(self, dt_order,s_symbol, s_action ,n_share_quant):
        '''
        Constructor
        '''
        self.order_date = dt_order
        self.symbol = s_symbol
        self.share_quantity = n_share_quant
        self.action = s_action
        
    def __str__(self):
        return self.order_date.strftime("%Y-%m-%d") + " - " + self.symbol + " - " + self.share_quantity + " - " + self.action
    
    def __unicode__(self):
        return self.__str__()
    def __repr__(self):
        return self.__str__()
        
    def get_order_date(self):
        return self.order_date
    
    def get_symbol(self):
        return self.symbol
    
    def get_number_of_shares(self):
        return self.share_quantity
    
    def get_action(self):
        return self.action