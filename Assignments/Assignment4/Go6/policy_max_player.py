#!/usr/bin/python3
"""
This function is loosely based on https://github.com/Rochester-NRT/RocAlphaGo/blob/develop/AlphaGo/mcts.py
"""

import numpy as np
import random
from board_util import GoBoardUtil, BLACK, WHITE
from feature import Feature
from feature import Features_weight

PASS = 'pass'

def uct_val(node, child, exploration, max_flag):
    if child._n_visits == 0:
        return float("inf")
    if max_flag:
        return float(child._black_wins)/child._n_visits + exploration*np.sqrt(np.log(node._n_visits)/child._n_visits) + node._prob_simple_feature / (1.0 + node._n_visits)
    else:
        return float(child._n_visits - child._black_wins)/child._n_visits + exploration*np.sqrt(np.log(node._n_visits)/child._n_visits) + node._prob_simple_feature / (1.0 + node._n_visits)

class TreeNode(object):
    """A node in the MCTS tree.
    """
    version = 0.1
    name = "MCTS Player"
    def __init__(self, parent):
        """
        parent is set when a node gets expanded
        """
        
        """
        """
        self._parent = parent
        self._children = {}  # a map from move to TreeNode
        self._n_visits = 0
        self._black_wins = 0
        self._expanded = False
        self._move = None
        self._prob_simple_feature = 1.0
        
    def Node_PolicyMove(self, board, color):
        """simulation .
        """
        gammas_sum = 0.0
        moves = board.get_empty_points()
        all_board_features = Feature.find_all_features(board)
        
        
        for move in moves:
            if move not in self._children:
                if board.check_legal(move, color) and not board.is_eye(move, color):
                    self._children[move] = TreeNode(self)
                    self._children[move]._move = move
                    if len(Features_weight) != 0:
                        # when we have features weight, use that to compute knowledge (gamma) of each move
                        assert move in all_board_features
                        
                        # may need to change here to consistence with given result
                        self._children[move]._prob_simple_feature = Feature.compute_move_gamma(Features_weight, all_board_features[move])                        
                                                
                        gammas_sum += self._children[move]._prob_simple_feature
        mctsMoves =[]
        mctsProbs=[]
        # appending normalized probability to each move
        for move in moves:        
            if board.check_legal(move, color) and not board.is_eye(move, color):
                self._children[move] = TreeNode(self)
                self._children[move]._move = move
                if len(Features_weight) != 0:
                    # when we have features weight, use that to compute knowledge (gamma) of each move
                    assert move in all_board_features
                    
                    # may need to change here to consistence with given result
                    self._children[move]._prob_simple_feature = Feature.compute_move_gamma(Features_weight, all_board_features[move])
                    mctsMoves.append(move)
                    mctsProbs.append(self._children[move]._prob_simple_feature/gammas_sum)
                    
        return mctsMoves,mctsProbs


    def select(self, exploration, max_flag):
        """Select move among children that gives maximizes UCT. 
        If number of visits are zero for a node, value for that node is infinity so definitely will  gets selected

        It uses: argmax(child_num_black_wins/child_num_vists + C * sqrt(2 * ln * Parent_num_vists/child_num_visits) )
        Returns:
        A tuple of (move, next_node)
        """
        return max(self._children.items(), key=lambda items:uct_val(self, items[1], exploration, max_flag))

    def update(self, leaf_value):
        """Update node values from leaf evaluation.
        Arguments:
        leaf_value -- the value of subtree evaluation from the current player's perspective.
        
        Returns:
        None
        """
        self._black_wins += leaf_value
        self._n_visits += 1

    def update_recursive(self, leaf_value):
        """Like a call to update(), but applied recursively for all ancestors.

        Note: it is important that this happens from the root downward so that 'parent' visit
        counts are correct.
        """
        # If it is not root, this node's parent should be updated first.
        if self._parent:
            self._parent.update_recursive(leaf_value)
        self.update(leaf_value)


    def is_leaf(self):
        """Check if leaf node (i.e. no nodes below this have been expanded).
        """
        return self._children == {}

    def is_root(self):
        return self._parent is None

s,visits))
        print("Statistics: {}".format(sorted(stats,key=lambda i:i[3],reverse=True)))
