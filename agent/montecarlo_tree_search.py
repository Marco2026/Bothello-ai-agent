import time
from hyperparameters import TIME_TO_SEARCH, CONSTANT_C
import math
import random

class Node:
    def __init__(self):
        self.children = []
        self.score = 0
        self.visits = 0
        self.isTerminal = False
        self.isExpanded = False
        self.actions = []

    def calculate_average_value(self):
        res = 1000000
        if self.visits != 0:
            res = self.score / self.visits
        return res
    
    def calculate_upper_confidence_bound(self, state):
        return state.calculate_average_value() + 2 * CONSTANT_C * math.sqrt(2 * math.log(self.visits) / state.visits)


def uct_search(state):
    root = Node(state)
    time_elapsed = time.time()
    time_limit = time.time() + TIME_TO_SEARCH
    while is_time_remaining(time_elapsed, time_limit):
        leaf = tree_policy(root)
        score = default_policy(leaf)
        backup(leaf, score)
    return action(best_child(root, 0))

def tree_policy(node):
    while node.isTerminal == False:
        if node.isExpanded == False:
            return expand(node)
        else:
            node = best_child(node, CONSTANT_C)

def expand(node):
    for a in node.actions:
        pass

def default_policy(state):
    while state.isTerminal == False:
        action = random.choice(state.actions)
        state = next_state(state, action)
    return state.score

def backup(node, score):
    while node != None:
        node.visits += 1
        node.score += score

def next_state(state, action):
    # Devolver el estado resultante de aplicar una accion al estado actual (conexion con el juego)
    pass

def is_time_remaining(actual_moment, time_limit):
    return (time_limit - actual_moment) > 0