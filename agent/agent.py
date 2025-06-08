from .montecarlo_tree_search import uct_search
from .training.neural_network import OthelloNet
from .hyperparameters import NEURAL_NETWORK_MODEL

class Agent:

    def __init__(self, neural_network=None):
        self.state = None
        self.action = None
        self.neural_network = neural_network
        if neural_network:
            self.neural_network = self.initialize_neural_network() 
        self.is_thinking = False           

    def make_decision(self, board):
        if not board.possible_movements:
            self.action = None
            return
        self.action = uct_search(board, self.neural_network)
        self.is_thinking = False   

    def initialize_neural_network(self):
        neural_network = OthelloNet(NEURAL_NETWORK_MODEL)
        return neural_network
