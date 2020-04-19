from random import randint
from math import floor

MAP_X = 10
MAP_Y = 10

class Industry:
    def __init__(self, population, supply):
        self.workers = population
        self.supply = supply
	self.map = []
        self.buildings = []
        self.assigned_workers = []
        for i in range(MAP_Y):
            row_tiles = []
            row_buildings = []
            row_workers = []
            for j in range(MAP_X):
                # 0-2: plains, 3-4: woods, 5: hills
                row_tiles += [randint(0, 5)]
                row_buildings += [["" ,0]]
                row_workers += [0]
            
            self.assigned_workers += [row_workers]    
            self.map += [row_tiles]
            self.buildings += [row_buildings]
        start_farms = 0
        start_lumber = 0
        ind = int(floor(0.5*(MAP_Y - 1)))
        while ind < MAP_Y and (start_farms < 3 or start_lumber < 1):
            for i in range(MAP_X):
                if self.map[ind][i] in [0, 1, 2] and start_farms < 3:
                    self.buildings[ind][i] = ["food", 1]
                    self.assign(ind, i, 1) 
                    start_farms += 1
                if self.map[ind][i] in [3, 4] and start_lumber < 1:
                    self.buildings[ind][i] = ["lumber", 1]
                    self.assign(ind, i, 1) 
                    start_lumber += 1
            ind += 1 

    def produce(self):
        for i in range(MAP_Y):
            for j in range(MAP_X):
                self.supply.produce(self.buildings[i][j][0], self.buildings[i][j][1]*self.assigned_workers[i][j]*2)
                
    def assign(self, y, x, num_workers):
        current_workers = self.assigned_workers[y][x]
        site = self.buildings[y][x]
        if (num_workers + current_workers) <= site[1]:
            if site[0] in ["food", "lumber", "mead"]:
                if (self.workers.num_peasants - self.workers.assigned_peasants) > num_workers:
                    self.workers.assigned_peasants += num_workers
                    self.assigned_workers[y][x] += num_workers
            elif site[0] in ["metal", "trinkets"]:
                if (self.workers.num_crafters - self.workers.assigned_crafters) > num_workers:
                    self.workers.assigned_crafters += num_workers
                    site[1] += num_workers


