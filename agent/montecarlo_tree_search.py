import time
from hyperparameters import TIME_TO_SEARCH, CONSTANT_C
import math
import random
from othello.board import Board

class Node:
    def __init__(self, board, current_player, action_selected=None, parent=None):
        current_state = State(board, current_player)
        self.children = []
        self.parent = parent
        self.reward = 0
        self.visits = 0
        self.isExpanded = False
        self.state = current_state
        self.action_selected = action_selected
        self.isTerminal = current_state.isTerminal

    def calculate_average_value(self):
        res = 1000000
        if self.visits != 0:
            res = self.reward / self.visits
        return res
    
class State:
    def __init__(self, board, current_player):
        game = Board (board, current_player)
        game_copy = game.copy()
        self.game = game_copy
        self.board = board
        self.current_player = current_player
        self.actions = game_copy.get_possible_movements(current_player)
        self.isTerminal = game_copy.game_finished
        self.reward = 0

    def copy(self):
        return State(self)

    def apply_action(self, action):
        self.game.put_piece(action.row, action.col)
        self.game.change_current_player()
        self.current_player = self.game.current_player
        self.actions = self.game.get_possible_movements(self.current_player)
        self.isTerminal = self.game.game_finished


class Action:
    def __init__(self, row, col, player_color=None):
        self.row = row
        self.col = col
        self.player_color = player_color

    def __repr__(self):
        return f"{self.player_color} to row {self.row}, col {self.col})"

    def __eq__(self, other_action):
        return isinstance(other_action, Action) and (
            self.row == other_action.row and
            self.col == other_action.col and
            self.player_color == other_action.player_color
        )

    def __hash__(self):
        return hash((self.row, self.col, self.player_color))

def expand(node):
    for action in node.state.actions:
        new_state = next_state(node.state, action)
        new_child = Node(new_state.board, new_state.current_player, action_selected=action, parent=node)
        node.children.append(new_child)
    if node.children:
        node.isExpanded = True
    return random.choice(node.children)

def best_child(node, constant_c):
    return max(
        node.children,
        key=lambda child: calculate_upper_confidence_bound(child, node.visits, constant_c)
    )

def default_policy(state):
    simulation_state = state.copy()
    while not simulation_state.isTerminal:
        action = random.choice(simulation_state.actions)
        simulation_state.apply_action(action)
    return simulation_state.reward

def backup(node, reward):
    while node is not None:
        node.visits += 1
        node.reward += reward
        node = node.parent

def next_state(state, action):
    new_state = state.copy()
    new_state.apply_action(action)
    return new_state

def calculate_upper_confidence_bound(node, parent_visits, constant_c):
    return node.calculate_average_value() + 2 * constant_c * math.sqrt(math.log(parent_visits) / node.visits)

def generate_time_countdown(time_to_search):
    return time.time(), time.time() + time_to_search

def is_time_remaining(actual_moment, time_limit):
    return (time_limit - actual_moment) > 0