from matplotlib import image, pyplot
import numpy

from supply import Supply
from market import Market
from population import Populace 
from industry import Industry, MAP_X, MAP_Y

if __name__ == "__main__":
    market = Market()
    player_supply = Supply("player", 100, 10, 0, 10, 0, 1000, market)
    player_civ = Populace(5, 0, 0, player_supply)    
    # (id, food, mead, trinkets, lumber, ducats, market)
    player_industry = Industry(player_civ, player_supply)

    plains = []
    plains += [image.imread("/home/falcon/Git/ld46/assets/plains_0.png")]
    plains += [image.imread("/home/falcon/Git/ld46/assets/plains_1.png")]

    woods = []
    woods += [image.imread("/home/falcon/Git/ld46/assets/woods_0.png")]
    woods += [image.imread("/home/falcon/Git/ld46/assets/woods_1.png")]

    hills = []
    hills += [image.imread("/home/falcon/Git/ld46/assets/hills_0.png")]
    # woods += [scipy.misc.imread("/home/falcon/Git/ld46/assets/woods_1")]
    
    X = plains[0].shape[0]
    Y = plains[0].shape[1]
    C = plains[0].shape[2]
    play_map = numpy.zeros([X*MAP_X, Y*MAP_Y, C], dtype=plains[0].dtype) 

    for i in range(MAP_Y):
        for j in range(MAP_X):
            # 0-2: plains, 3-4: woods, 5: hills
            tile = numpy.zeros([X,Y,C])
            if player_industry.map[i][j] in [0, 1, 2]:
                tile = plains[0]            
            elif player_industry.map[i][j] in [3, 4]:
                tile = woods[0]            
            elif player_industry.map[i][j] == 5:
                tile = hills[0]
            site = player_industry.buildings[i][j]
            if site[0] == "food":
                tile = plains[site[1]]
            elif site[0] == "lumber":
                tile = woods[site[1]]
            play_map[(i*X):((i+1)*X),(j*Y):((j+1)*Y),:] = tile

    pyplot.imshow(play_map)
    pyplot.show()


