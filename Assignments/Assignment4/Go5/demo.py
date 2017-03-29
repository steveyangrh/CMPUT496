#!/usr/bin/python3
from board import GoBoard
from board_util import GoBoardUtil, BLACK, WHITE, EMPTY, BORDER, FLOODFILL
import numpy as np
from Go5 import Go5Player
import time 
board=GoBoard(4)
player=Go5Player(num_simulation = 200, limit=100, exploration = np.sqrt(2))
player.MCTS.komi = 6.5
player.num_nodes = 5

cboard = board.copy()
print("\nrunning playout 200 times\n")
player.run( cboard, BLACK,print_info=True)


#time.sleep(30) # sleeping
player.num_simulation = 300
print("\nrunning it 300 more times\n")
cboard = board.copy()
player.run( cboard, BLACK,print_info=True)


#time.sleep(30)
print("\nrunning it 300 more times\n")
cboard = board.copy()
player.run( cboard, BLACK, print_info=True)


#time.sleep(30)
print("\nrunning it 300 more times\n")
cboard = board.copy()
player.run( cboard, BLACK, print_info=True)
