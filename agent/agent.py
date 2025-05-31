import random

class Agent:

    def __init__(self):
        self.state = None
        self.action = None

    def make_decision(self, board):
        if not board.possible_movements:
            self.action = None
            return
        self.action = random.choice(board.possible_movements)

