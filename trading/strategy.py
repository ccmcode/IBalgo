'''
Created on Dec 1, 2013

@author: Colin
'''
from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
from multiprocessing import Process, Queue, Pool
from trading.market import Market
from dbConfig import dbFund
from time import sleep
import abc

class Strategy(Process):
    '''  Strategy class
         provides -framework of how each strategy runs
                  -interfaces to the market
    '''
    def __init__(self, connection, *a, **kw):
        super(Strategy, self).__init__(*a, **kw)
        self.name = type(self).__name__
        self.conn = connection
        self.last = 0
        self.sleep = 30
    
    def TickPrice(self, msg):
        return 2      
        
    def monitor(self):
        pass    
    
    def run(self):
        self.getContracts()
        
        while True:
            self.last, run = self.db.isActive(self.last, self.contractIds)  
            if run:
                self.monitor()
            sleep(self.sleep)

class BaseStrategy(Strategy):
    '''  Strategy class
         provides and interface to the db
    '''
    def __init__(self, *a, **kw):
        super(BaseStrategy, self).__init__(*a, **kw)
        self.db = dbFund()        
        self.contracts, self.contractIds = None, None

    def makeContract(self, details):
        c = Contract()
        c.m_symbol = details[0]
        c.m_secType = details[1]
        c.m_currency = details[2]
        c.m_exchange = details[3]
        return c
        
    def getContractDetails(self):
        return [self.makeContract(t) for t in self.details]    
    
    def getContracts(self):
        if self.contracts: return self.contracts
        if not self.contractIds: self.contractIds = self.db.getContractIds(self.name)
        self.contracts = [self.db.getContract(i) for i in self.contractIds]
        return self.contracts                    
                        
class VIX(BaseStrategy):
    details = [('VIX', 'FUT', 'USD', 'CFE'),
               ('VIX', 'IND', 'USD', 'CBOE')]
    
    def __init__(self, *a, **kw):
        super(VIX, self).__init__(*a, **kw)
    
    def monitor(self, tick):
        pass
    
class OIL(BaseStrategy):
    def __init__(self, *a, **kw):
        super(Strategy).__init__(*a, **kw)
        self.vix = Vix()
    
    def getContracts(self):
        return 1
    
    def monitor(self, tick):
        pass
         
class RISK(BaseStrategy):
    def __init__(self, *a, **kw):
        super(Strategy).__init__(*a, **kw)
        self.vix = Vix()
    
    def getContracts(self):
        return 1
    
    def monitor(self, tick):
        pass

class Test(BaseStrategy):
    details = [('SPY','STK','USD','SMART')]
    
if __name__ == '__main__':
    t = Test()
    print t.is_alive()
    print 2