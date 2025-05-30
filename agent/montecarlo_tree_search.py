import time
from hyperparameters import TIME_TO_SEARCH, CONSTANT_C
import math

class Node:
    def __init__(self):
        self.children = []
        self.score = 0
        self.visits = 0

    def calculate_average_value(self):
        res = None
        if self.visits != 0:
            res = self.score / self.visits
        return res
    
    def calculate_upper_confidence_bound(self, state):
        return state.calculate_average_value() + CONSTANT_C * math.sqrt(math.log(self.visits) / state.visits)

def montecarlo_tree_search(state):
    tree = Node(state)
    time_elapsed = time.time()
    time_limit = time.time() + TIME_TO_SEARCH
    while is_time_remaining(time_elapsed, time_limit):
        leaf = select(tree)
        child = expand(leaf)
        result = simulate(child)
        back_propagate(result, child)
        time_elapsed = time.time()
    return action

def is_time_remaining(actual_moment, time_limit):
    return (time_limit - actual_moment) > 0