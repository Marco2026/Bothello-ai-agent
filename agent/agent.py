import random
from .montecarlo_tree_search import uct_search

class Agent:

    def __init__(self):
        self.state = None
        self.action = None

    def make_decision(self, board):
        if not board.possible_movements:
            self.action = None
            return
        self.action = uct_search(board)

    def make_naive_decision(self, board):
        if not board.possible_movements:
            self.action = None
            return
        self.action = random.choice(board.possible_movements)

