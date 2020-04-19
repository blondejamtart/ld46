from math import floor
from queue import Queue
import json


class Market:
    def __init__(self):
        self.prices = {"food": 10.0, "mead": 50.0, "trinkets": 200.0, "lumber": 50.0}
        self.available = {"food": 0, "mead": 0, "trinkets": 0, "lumber": 0}
        self.profits = {}
        self.shares = {}
        self.pot = {}
        self.sellers = []
        self.purchases = Queue()
        self.registation = Queue()

    def buy(self, resource, amount, seller_delivery):
        self.purchases.put[resource, amount, seller_delivery])

    def register(self, seller_id):
        self.registration.put(seller_id)

    def __buy(self, request):
        resource, amount, seller_delivery = request
        if amount > self.available[resource]
            amount = self.available[resource]
        self.available[resource] -= amount
        for seller_id in self.shares.keys():
            self.profits[seller_id] += self.shares[seller_id][resource]*self.prices[resource]*amount
            self.pot[seller_id][resource] -= self.shares[seller_id][resource]*amount
        seller_delivery.put(amount)

    def __register(seller_id):
        if seller_id not in self.sellers:
            self.sellers += [seller_id]
            self.pot[seller_id] = {"food": 0, "mead": 0, "trinkets": 0, "lumber": 0}
            self.profits[seller_id] = 0.0
            self.shares[seller_id] = {"food": 0.0, "mead": 0.0, "trinkets": 0.0, "lumber": 0.0}    

    def evolve_prices(self):
        # TODO: maybe make prices update based on supply & demand?
        pass

    def export(self, resource, amount, seller_id):
        self.available[resource] += amount
        self.pot[seller_id][resource] = amount

    def update_shares(self):
        for seller_id in self.pot.keys():
            for resource in self.pot[seller_id].keys():
                self.shares[seller_id][resource] = float(self.pot[seller_id][resource])/float(self.available[resource])

    def clear_stock(self):
        for k in self.available.keys():
            self.available[k] = 0

    def collect(self, seller_id):
        profit = self.profits[seller_id]
        self.profits[seller_id] = 0
        unsold = json.dumps(self.pot[seller_id])
        self.pot[seller_id] = {"food": 0, "mead": 0, "trinkets": 0, "lumber": 0}
        return [profit, unsold]
  
    def process_transactions(self):
        while not self.registration.empty():
            self.__register(self.registration.get())
        while not self.purchases.empty():
            self.__buy(self.purchases.get())
        
            
  
