from enum import Enum

GENERATE_TRAINING_DATA = True

class PlayerMode(Enum):
    HUMAN = 0
    BOT = 1
    AGENT = 2

class NeuralNetwork(Enum):
    STARTER = 0
    IMPROVED = 1  

PLAYER_1 = PlayerMode(2)
PLAYER_2 = PlayerMode(2)

AGENT_1_NEURAL_NETWORK = None
AGENT_2_NEURAL_NETWORK = None


SIMULATIONS = 50