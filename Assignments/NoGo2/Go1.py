#!/usr/bin/python3
from gtp_connection import GtpConnection
from board_util import GoBoardUtil
from timeout import timeout
class RandomPlayer():
    def __init__(self):
        """
        Player that selects moves randomly from the set of legal moves.
        Does not fill single-point eyes.

        Parameters
        ----------
        name : str
            name of the player (used by the GTP interface).
        version : float
            version number (used by the GTP interface).
        """
        self.name = "NoGo2"
        self.version = 0.1
        self.timeout = -1
    def get_move(self, board, color):
        if self.timeout > 0:
            f = timeout(self.timeout, GoBoardUtil.generate_best_move, GoBoardUtil.generate_random_move(board, color))
        else:
            f = GoBoardUtil.generate_best_move
        return f(board, color)
    

def run():
    """
    start the gtp connection and wait for commands.
    """
    con = GtpConnection(RandomPlayer())
    con.start_connection()

if __name__=='__main__':
    run()
