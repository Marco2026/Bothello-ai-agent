from enum import Enum

GENERATE_TRAINING_DATA = True

class PlayerMode(Enum):
    HUMAN = 0
    BOT = 1
    AGENT = 2

class NeuralNetwork(Enum):
    STARTER = 0
    IMPROVED = 1  

PLAYER_1 = PlayerMode(1)
PLAYER_2 = PlayerMode(1)

AGENT_1_NEURAL_NETWORK = NeuralNetwork(0)
AGENT_2_NEURAL_NETWORK = NeuralNetwork(0)


SIMULATIONS = 200