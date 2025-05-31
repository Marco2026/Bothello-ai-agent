import random

class Agent:

    def __init__(self):
        self.state = None
        self.action = None

    def make_decision(self, board):
        self.action = random.choice(board.possible_movements)

