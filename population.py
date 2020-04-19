from math import floor

FOOD_COST = 1
MEAD_COST = 1
TRINKET_COST = 1


class Populace:
    def __init__(self, peasants, crafters, snobs, supply):
        self.num_peasants = peasants
        self.assigned_peasants = 0
        self.rowdy_peasants = 0
        self.happy_peasants = 0

        self.num_crafters = crafters
        self.assigned_crafters = 0
        self.rowdy_crafters = 0
        self.happy_crafters = 0

        self.num_snobs = snobs
        self.assigned_snobs = 0
        self.rowdy_snobs = 0

        self.supply = supply  # the economy which supplies this

    def sustain_food(self):
        unmet = [False, False, False]
        peasant_food_need = self.num_peasants*FOOD_COST
        crafer_food_need = self.num_crafters*FOOD_COST
        snob_food_need = self.num_snobs*FOOD_COST

        total_food_need = peasant_food_need + crafter_food_need + snob_food_need

        if total_food_need <= self.supply.food_stockpile():
            self.supply.consume_food(total_food_need)
        else:
            unmet_food = total_food_need - self.supply.food_stockpile()
            imported_food = self.supply.import_food(unmet_food)
            if imported_food < unmet_food:
                acquired_food = (imported_food + self.supply.food_stockpile())
                if  acquired_food < peasant_food_need:
                    unmet = [True, True, True]
                    self.rowdy_peasants += (peasant_food_need - acquired_food)/FOOD_COST
                    self.rowdy_crafters +=  self.num_crafters
                    self.rowdy_snobs += self.num_snobs
                elif acquired_food < (peasant_food_need + crafter_food_need):
                    unmet = [False, True, True]
                    self.rowdy_crafters +=  (peasant_food_need + crafter_food_need - acquired_food)/FOOD_COST
                    self.rowdy_snobs += self.num_snobs
                else:
                    unmet = [False, False, True]
                    self.rowdy_snobs += (peasant_food_need + crafter_food_need + snob_food_need - acquired_food)/FOOD_COST
        return unmet

    def sustain_mead(self):
        unmet = [False, False, False]
        crafer_mead_need = self.num_crafters*MEAD_COST
        snob_mead_need = self.num_snobs*MEAD_COST

        total_mead_need = crafter_mead_need + snob_mead_need

        if total_mead_need <= self.supply.mead_stockpile():
            self.supply.consume_mead(total_mead_need)
            if self.rowdy_peastants == 0:
                if self.supply.stockpile["mead"] > self.num_peasants*MEAD_COST:
                    self.happy_peasants += self.num_peasants
                    self.supply.consume_mead(self.num_peasants*MEAD_COST)
                else:
                    peasant_w_mead = floor(self.supply.mead_stockpile()/MEAD_COST)
                    self.supply.consume("mead", peasant_w_mead*MEAD_COST)
                    self.happy_peastants += peasant_w_mead                   
                
        else:
            unmet_mead = total_mead_need - self.supply.stockpile["mead"]
            imported_mead = self.supply.import_mead(unmet_mead)
            if imported_mead < unmet_mead:
                acquired_mead = (imported_mead + self.supply.stockpile["mead"])
                if acquired_mead < crafter_mead_need:
                    unmet = [False, True, True]
                    self.rowdy_crafters +=  (crafter_mead_need - acquired_mead)/MEAD_COST
                    self.rowdy_snobs += self.num_snobs
                else:
                    unmet = [False, False, True]
                    self.rowdy_snobs += (crafter_mead_need + snob_mead_need - acquired_mead)/MEAD_COST
            self.supply.consume("mead", self.supply.stockpile["mead"])
        return unmet

    def sustain_trinkets(self):
        unmet = [False, False, False]
        snob_trinket_need = self.num_snobs*TRINKET_COST

        if snob_trinket_need <= self.supply.stockpile["trinkets"]:
            self.supply.consume("trinkets", snob_trinket_need)
            if self.rowdy_crafters == 0:
                if self.supply.stockpile["trinkets"] > self.num_crafters*TRINKET_COST:
                    self.happy_crafters += self.num_crafters
                    self.supply.consume_trinkets(self.num_crafters*TRINKET_COST)
                else:
                    crafter_w_trinkets = floor(self.supply.stockpile["trinkets"]/TRINKET_COST)
                    self.supply.consume("trinkets", crafter_w_trinkets*TRINKET_COST)
                    self.happy_peastants += crafter_w_trinkets                   
                
        else:
            unmet_trinkets = snob_trinket_need - self.supply.stockpile["trinkets"]
            imported_trinkets = self.supply.import_resource("trinkets", unmet_trinkets)
            if imported_trinkets < unmet_trinkets:
                acquired_tromlets = (imported_trinkets + self.supply.stockpile["trinkets"])
                unmet = [False, False, True]
                self.rowdy_snobs += (snob_trinket_need - acquired_trinkets)/TRINKET_COST
            self.supply.consume("trinkets", self.supply.stockpile["trinkets"])
        return unmet        

    def promote(self):
        if self.happy_crafters > self.num_crafters:
            to_promote = min(self.num_crafters, floor(0.5*(self.happy_crafters - self.num_crafters)))
            self.num_crafters -= to_promote
            self.num_snobs += to_promote

        if self.happy_peasants > self.num_peasants:
            to_promote = min(self.num_peasants, floor(0.5*(self.happy_peasants - self.num_peasants)))
            self.num_peasants -= to_promote
            self.num_crafters += to_promote
 

        if self.supply.stockpile["food"] > FOOD_COST*self.num_peasants:
            self.num_peasants += floor(0.5*(self.supply.stockpile["food"] - FOOD_COST*self.num_peasants))

    def demote(self):
        pass

