'''
Created on Dec 2, 2013

@author: Colin
'''
from market.asset import Asset, price

class Vix(Asset):
    def __init__(self, *a, **kw):
        super(Vix).__init__(a, kw)
        values = ['Open', 'lo']
        self.points = DataFrame()
        
    def addPoint(self, d, s):
        self.date = d
        self.open = price(s[0])      
        self.low = price(s[1])
        self.hi = price(s[2])
        if price(s[3]):
            self.points.append(price(s[3]))   