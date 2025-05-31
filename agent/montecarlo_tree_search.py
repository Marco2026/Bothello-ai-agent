import time
from hyperparameters import TIME_TO_SEARCH, CONSTANT_C
import math
import random

class Node:
    def __init__(self, state):
        self.children = []
        self.score = 0
        self.visits = 0
        self.isExpanded = False
        self.state = state

    def calculate_average_value(self):
        res = 1000000
        if self.visits != 0:
            res = self.score / self.visits
        return res

def uct_search(state):
    root = Node(state)
    time_elapsed, time_limit = generate_time_countdown(TIME_TO_SEARCH)
    while is_time_remaining(time_elapsed, time_limit):
        leaf = tree_policy(root)
        score = default_policy(leaf.state)
        backup(leaf, score)
        time_elapsed = time.time()
    return action(best_child(root, 0))

def tree_policy(node):
    while node.isTerminal == False:
        if node.isExpanded == False:
            return expand(node)
        else:
            node = best_child(node, CONSTANT_C)

def expand(node):
    for action in node.state.actions:
        new_child = Node(next_state(node.state, action))
        node.children.append(new_child)
    return new_child

def best_child(node, constant_c):
    return sorted([child for child in node.children], key = lambda child : calculate_upper_confidence_bound(child, node.visits, constant_c), reverse=True)[0]

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

def calculate_upper_confidence_bound(node, parent_visits, constant_c):
    return node.calculate_average_value() + 2 * constant_c * math.sqrt(2 * math.log(parent_visits) / node.visits)

def generate_time_countdown(time_to_search):
    return time.time(), time.time() + time_to_search

def is_time_remaining(actual_moment, time_limit):
    return (time_limit - actual_moment) > 0