'''
Created on Dec 18, 2013

@author: Colin
'''
class Request(object):
    def __init__(self, *a, **kw):
        self._i=0
        self.map = {}
        
    def get(self, i):
        return self.map[i]
    
    def getIds(self):
        return [k for k,v in self.map.iteritems()]
        
    def remove(self, i):
        return self.map.pop(i)
    
    def isEmpty(self):
        return not self.map
        
class ContractRequest(Request):
    def nextId(self, name):
        self._i += 1
        self.map[self._i] = name
        return self._i

class TickRequest(Request):
    def __init__(self, *a, **kw):
        super(TickRequest, self).__init__(*a, **kw)
        self.t = {}
    
    def add(self, name, i):
        if self.map[i]:
            self.map[i].append(name)
        else:
            self.map[i] = [name]

class Bid(object):
    def __init__(self, msg):
        self.msg = msg
        self.type = self.getMsgType(msg)
                        
class Response(object):
    def __init__(self, msg):
        self.msg = msg
        self.type = self.getMsgType(msg)
        
    def getMsgType(self):
        raise NotImplemented
    
    def getClass(self):
        pass
     
    def action(self):
        try:
            self.message = 1  
        except NotImplemented:
            pass
        