from pymongo import MongoClient
from bson.binary import Binary
from datetime import date
from ib.ext.Contract import Contract
import time
import copy

import logging
log = logging.getLogger(__name__)

HOST = 'localhost'
PORT =  27017
DB   = 'fund'
COB = int(date.today().strftime("%Y%m%d"))
TickTypes = []

def connArgs():
    db = MongoClient(HOST, PORT)[DB]
    result = db.client.find_one()
    host, port, id = 'localhost', 7496, 0
    if result:
        id = result['id'] + 1 
    db.client.update{},{"$se(t": {'id': id}}, upsert=True)    
    return host, port, id
    
def cantor(x, y):
    return (x + y) * (x + y + 1) / 2 + y

def toDict(obj):
    d = copy.deepcopy(obj.__dict__)  
    for k in d.keys():
        if hasattr(d[k], '__dict__'):
            d[k] = toDict(d[k])
    return d
    
class dbFund(object):
    _db = MongoClient(HOST, PORT)[DB]
    
    def putContractDetails(self, name, contract_details):
        d = toDict(contract_details)
        d['_id'] = d['m_summary']['m_conId']
        self._db.contract.save(d)
        
        row = {'conId':d['_id'], 'name': name, 'cob': COB}
        self._db.requestor.update(row, {"$set": row}, upsert=True )
        
        log.info("Insert Contract %s - owned by '%s'" % (d['_id'], name))
          
    def getContract(self, conId):
        doc = self._db.contract.find_one({'m_summary.m_conId': conId})
        
        if doc:
            c = Contract()
            for k,v in doc['m_summary'].iteritems():
                setattr(c,k,str(v)) if isinstance(v, unicode) else setattr(c,k,v)
            return c
    
    def updateIndicators(self, query, key, value):
        if key in ['BID', 'ASK']:
            row = self._db.ticks.find_one(query)
            try:
                delta = (value-row[key]) / row[key]
            except:
                delta = 1.0
            self._db.ticks.update(query, {"$set": {'delta'+key:delta}}, upsert=True)
               
    def updateTick(self, tickerId, key, value):
        query = {'conId': tickerId, 'COB': COB}
        data = {'conId': tickerId, 'COB': COB, key: value}
        self.updateIndicators(query, key, value)
        self._db.ticks.update(query, {"$set": data}, upsert=True )
        
        log.info("Added %s tick for conId %s" % (key, tickerId))
                    
    def getLatestTick(self, conId):
        doc = self.ticks.find({'_id': conId}, {'_id': 0, 'c': 1})
        return doc
    
    def getContractInfo(self, conId):
        return self.getContract(conId), self.getLatestTick(conId)
    
    def getContractIds(self, name):
        ids = []  
        for doc in self._db.requestor.find({'name':name, 'cob':COB}):
            ids.append(doc['conId'])
        return ids
      
    def getOwners(self, conId):
        owners=[]
        for doc in self.requestor.find({'conId':conId}):
            owners += doc['name']
        return owners
    
    def isActive(self, latest, conIds):
        current = time.time()
        row = self._db.ticks.find({'conId': {'$in': conIds}}).sort('LAST_TIMESTAMP', -1)
        if row:
            if hasattr(row[0],'LAST_TIMESTAMP'):
                return current, current < row[0]['LAST_TIMESTAMP']
        return current, True
        