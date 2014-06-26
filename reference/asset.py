"""
        Assets interface
        Colin Mimnaugh
"""
from pandas import DataFrame

def price(spot):
    if isinstance(spot, float):
        return float(spot)
    
class Asset(object):
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns
        self.contracts = []
        self.points = DataFrame()
        
    def addContract(self, c):
        self.contracts.append(c)
    
    def addPoint(self, date, *a, **kw):
        d = toDate(date)
        self.points[d] = (a, kw)
        
    def getPrice(self, d=None):
        return self.points
    
    def getContracts(self, d, t):
        return [c for c in self.contracts if c.isApplicable(d, t)]
    
    def average(self):
        return 5
        
class Yield(object):
    def __init__(self, *a, **kw):
        self.dividends = []    
                
class Contract(Asset):
    def __init__(self, underlyer, types, *a, **kw):
        self.underlyer = underlyer
        self.types = types
        self.maturity = a[0]
        self.points = {}
        self.stats = kw
    
    def addPoint(self, date, *a, **kw):
        d = toDate(date)
        self.points[d] = (a[0], kw)
        
    def isApplicable(self, d, t):
        return self.points.has_key(d) and t in self.types

class VanillaCall(Contract):
    def __init__(self, strike, *a, **kw):
        super(VanillaCall).__init__(*a, **kw)
        self.k = strike
        self.types.append('CALL')
        
    def intrinsicValue(self, d):
        return self.k - self.asset.getPrice(d)
    
class VanillaPut(Contract):
    def __init__(self, strike, *a, **kw):
        super(VanillaPut).__init__(*a, **kw)
        self.k = strike
        self.types.append('PUT')
        
    def intrinsicValue(self, d):
        return self.k - self.asset.getPrice(d)

class Future(Contract):
    def __init__(self, strike, *a, **kw):
        super(VanillaCall).__init__(*a, **kw)
        
class FutureCurve(Asset):
    def __init__(self, asset, date):
        self.asset = asset
        self.date = toDate(date)
        self.type = 'Future'
        
    def getCurve(self, date):
        d = toDate(date)
        return self.asset.getContracts(self.type, d)
    
class OptionSurface(Asset):
    def __init__(self, asset, date):
        self.asset = asset
        self.date = toDate(date)
        self.type = 'Option'
        
    def getCurve(self, date):
        d = toDate(date)
        return self.asset.getContracts(self.type, d)
    
if __name__ == "__main__":
    df = DataFrame(columns = ['a', 'b'])
    print(df)