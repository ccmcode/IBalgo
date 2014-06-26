from ib.opt import ibConnection
from dbConfig import dbFund,connArgs
from multiprocessing import Lock
import logging
log = logging.getLogger(__name__)
    

class Market(object):
    ''' Gateway to the market
    '''
    def __init__(self, *a, **kw):
        self.lock = Lock()
        self.connect()
                
    def connect(self):
        host, port, clientId = connArgs()
        self.conn = ibConnection(host, port, clientId)
        self.register()
        self.conn.enableLogging()
        self.conn.connect()
    
    def disconnect(self):
        self.conn.disconnect()
        
    def getConnection(self):
        return self.conn