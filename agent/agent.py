from .montecarlo_tree_search import uct_search
from .training.neural_network import OthelloNet
from .hyperparameters import NEURAL_NETWORK_MODEL_1, NEURAL_NETWORK_MODEL_2
from game.game_var import NeuralNetwork

class Agent:

    def __init__(self, neural_network=None):
        self.state = None
        self.action = None
        self.neural_network = neural_network
        if neural_network == NeuralNetwork.STARTER:
            self.neural_network = self.initialize_first_neural_network()
        elif neural_network == NeuralNetwork.IMPROVED:
            self.neural_network = self.initialize_second_neural_network()
        self.is_thinking = False           

    def make_decision(self, board):
        if not board.possible_movements:
            self.action = None
            return
        self.action = uct_search(board, self.neural_network)
        self.is_thinking = False   

    def initialize_first_neural_network(self):
        neural_network = OthelloNet(NEURAL_NETWORK_MODEL_1)
        return neural_network
    
    def initialize_second_neural_network(self):
        neural_network = OthelloNet(NEURAL_NETWORK_MODEL_2)
        return neural_network
