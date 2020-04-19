import json
from math import floor
from time import sleep

import websockets

from supply import Supply
from market import Market
from population import Populace 
from industry import Industry

if __name__ == "__main__":
    supplies = []
    civs = []
    industries = []
    
    market = Market()
    player_supply = Supply("player", 100, 10, 0, 10, 0, 1000, market)
    player_civ = Populace(5, 0, 0, player_supply)    
    # (id, food, mead, trinkets, lumber, ducats, market)
    player_industry = Industry(player_civ, player_supply)
    
    civs += [player_civ]
    supplies += [player_supply]
    industries += [player_industry]

    while True:
        for ind in industries:
            ind.produce()

        for civ in civs:
            civ.sustain_food()
            civ.sustain_mead()
            civ.sustain_trinkets()
            civ.promote()
            civ.demote()
 
        market.clear_stock()
 
        for stock in supplies:
            stock.collect_profit()
            stock.export()

        # TODO: update GUI with exported + hoard stock levels
        market.update_shares()

        sleep(3)

    
