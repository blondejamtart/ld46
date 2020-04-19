from math import floor
from queue import Queue
import json


class Supply:
    def __init__(self, unique_id, food, mead, trinkets, lumber, metal, ducats, market):
        self.__id = unique_id
        self.stockpile = {"food": food, "mead": mead, "lumber": lumber, "trinkets": trinkets, "metal": metal}
   
        self.hoard = {"food": 0.1, "mead": 0.1, "lumber": 0.1, "trinkets": 0.1, "metal": 0.1}

        self.ducats = ducats
        self.market = market
        
        self.deliveries = Queue()

    def consume(self, resource, amount):
        self.stockpile[resource] -= amount

    def produce(self, resource, amount):
        self.stockpile[resource] += amount

    def import_resource(self, resource, amount): 
        to_import = amount 
        if amount > self.market.available[resource]:
            to_import = self.market.available[resource]
        cost = to_import*self.market.prices[resource]
        if cost > self.ducats:
            to_import = floor(self.ducats/self.market.prices[resource]) 
              
        self.market.buy(resource, to_import, self.deliveries)
        purchased = self.deliveries.get()
        self.ducats -= purchased*self.market.prices[resource]
        return purchased

    def export(self):
        for resource in self.stockpile.keys():
            self.market.export(resource, floor(self.stockpile[resource]*(1.0 - self.hoard[resource])), self.__id)
            self.stockpile[resource] -= self.stockpile[resource]*(1.0 - self.hoard[resource])         

    def collect_profit(self):
        gains = self.market.collect(self.__id)
        self.ducats += gains[0]
        resources = json.loads(gains[1])
        for k, v in resources.items():
            self.stockpile[k] += floor(v)
            
        
