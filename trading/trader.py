'''
Created on Dec 12, 2013

@author: Colin
'''
from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
from multiprocessing import Process, Queue
from trading import STRATEGIES
from trading.request import ContractRequest, TickRequest
from trading.ticks import Tick
from time import sleep
from dbConfig import dbFund,connArgs
import logging
log = logging.getLogger(__name__)
    
class Trader(Process):
    ''' Trader
          - Gateway to the market
    '''
    def __init__(self, strats, *a, **kw):
        self.orders = Queue()
        self.strats = strats
        self.db = dbFund()
        self.connect()
                    
    def connect(self):
        host, port, clientId = connArgs()
        self.conn = ibConnection(host, port, clientId)
        self.register()
        self.conn.enableLogging()
        self.conn.connect()
    
    def disconnect(self):
        self.conn.disconnect()
        
    def error_handler(self, msg):
        log.info('ERROR - %s' % msg)
    
    def contract_handler(self, msg):
        name = self.req.get(msg.reqId)
        self.db.putContractDetails(name, msg.contractDetails)
        
    def contract_end_handler(self, msg):
        name = self.req.get(msg.reqId)
        self.req.remove(msg.reqId)
        log.info('End Contract Detail request for %s Strategy' % (name))
            
    def tick_handler(self, msg):
        k, v = self.tick.parseTick(msg)

        if k and v:
            self.db.updateTick(msg.tickerId, k, v)
                 
    def reqContractDetails(self, strat):
        for c in strat.getContractDetails():
            id = self.req.nextId(strat.name)
            self.conn.reqContractDetails(id, c)
    
    def reqMarketData(self, strat):
        for c in strat.getContracts():
            self.conn.reqMktData(c.m_conId, c, '', 1) 
    
class BlindTrader(Trader):
    ''' BlindTrader
          - Request Contracts based on details from each ACTIVE strat
          - Insert each <contract> and (contract_id, stratname) into FundDB
    '''
    def __init__(self, strats, *a, **kw):
        super(BlindTrader, self).__init__(strats, *a, **kw)
        self.req = ContractRequest()
 
    def register(self):
        self.conn.register(self.contract_handler, 'ContractDetails')   
        self.conn.register(self.contract_end_handler, 'ContractDetailsEnd')
                    
    def run(self): 
        [self.reqContractDetails(s) for s in self.strats]
        while not self.req.isEmpty(): 
            log.info("Request Queue isn't empty ...sleeping...")
            sleep(10)
        
class MarketTrader(Trader):
    ''' MarketTrader
          - Request market data based on the contracts
          - Saved ticks to FundDB
    '''
    def __init__(self, strats, *a, **kw):
        super(MarketTrader, self).__init__(strats, *a, **kw)
        self.req = TickRequest()
        self.tick = Tick()
        
    def register(self):
        self.conn.register(self.tick_handler, 'TickPrice')
        self.conn.register(self.tick_handler, 'TickSize')
        self.conn.register(self.tick_handler, 'TickString')
        self.conn.register(self.tick_handler, 'TickGeneric')
                    
    def run(self, i=1):
        while i != 0:
            [self.reqMarketData(s) for s in self.strats]
            log.info("...sleeping...")            
            sleep(5)
            i = i-1
        return True