import random
from .montecarlo_tree_search import uct_search
from .training.neural_network import OthelloNet

class Agent:

    def __init__(self, use_neural_network=False):
        self.state = None
        self.action = None
        self.neural_network = None
        if use_neural_network:
            self.neural_network = self.initialize_neural_network()            

    def make_decision(self, board):
        if not board.possible_movements:
            self.action = None
            return
        self.action = uct_search(board, self.neural_network)

    def make_naive_decision(self, board):
        if not board.possible_movements:
            self.action = None
            return
        self.action = random.choice(board.possible_movements)

    def initialize_neural_network(self):
        neural_network = OthelloNet()
        neural_network.prepare_data()
        neural_network.train_model()
        return neural_network
