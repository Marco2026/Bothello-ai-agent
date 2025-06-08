import time
from .hyperparameters import TIME_TO_SEARCH, CONSTANT_C
from othello.game_config import ROWS, COLS
from othello.colors import WHITE
import math
import random
from othello.board import Board

class Node:
    def __init__(self, state, parent=None, action_selected=None):
        self.children = []
        self.parent = parent
        self.reward = 0
        self.visits = 0
        self.isExpanded = False
        self.state = state
        self.action_selected = action_selected
        self.isTerminal = state.isTerminal
        self.untried_actions = list(state.actions)

    def calculate_average_value(self):
        if self.visits == 0:
            return float("inf")
        return  self.reward / self.visits
    
class State:
    def __init__(self, board, current_player, root_player=None):
        self.game = Board(board, current_player)
        self.board = self.game.board
        self.current_player = self.game.current_player
        self.actions = self.game.possible_movements
        self.isTerminal = self.game.game_finished
        self.reward = 0
        self.root_player = root_player

    def copy(self):
        new_game = self.game.copy()
        new_state = State(new_game.board, new_game.current_player, self.root_player)
        new_state.game = new_game
        new_state.board = new_game.board
        new_state.actions = new_game.possible_movements
        new_state.isTerminal = new_game.game_finished
        return new_state

    def apply_action(self, action):
        self.game.put_piece(action[0], action[1])
        self.current_player = self.game.current_player
        self.board = self.game.board
        self.actions = self.game.possible_movements
        self.isTerminal = self.game.game_finished

    def caculate_reward(self):
        winner = self.game.get_winner()
        if winner == self.root_player:
            return 1
        elif winner is None:
            return 0
        else:
            return -1

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
    
def uct_search(state, neural_network):
    root_state = State(state.board, state.current_player, state.current_player)
    root = Node(root_state)
    time_elapsed, time_limit = generate_time_countdown(TIME_TO_SEARCH)
    while is_time_remaining(time_elapsed, time_limit):
        leaf = tree_policy(root)
        reward = default_policy(leaf.state) if neural_network is None else neural_network_policy(state, neural_network)
        backup(leaf, reward)
        time_elapsed = time.time()
    return best_child(root, 0).action_selected

def tree_policy(node):
    while not node.isTerminal:
        if not node.isExpanded:
            return expand(node)
        else:
            node = best_child(node, CONSTANT_C)
    return node

def expand(node):
    if not node.untried_actions:
        node.isExpanded = True
        return 

    action = random.choice(node.untried_actions)
    node.untried_actions.remove(action)

    new_state = next_state(node.state, action)
    new_child = Node(new_state, parent=node, action_selected=action)
    node.children.append(new_child)

    if not node.untried_actions:
        node.isExpanded = True

    return new_child

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
    return simulation_state.caculate_reward()

def neural_network_policy(state, neural_network):
    simulation_state = state.copy()
    prepared_state = parse_state(simulation_state)
    reward = neural_network.predict(prepared_state)
    return float(reward[0][0])

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
    if node.visits == 0: 
        return float("inf")
    return node.calculate_average_value() + 2 * constant_c * math.sqrt(( 2 * math.log(parent_visits)) / node.visits)

def generate_time_countdown(time_to_search):
    return time.time(), time.time() + time_to_search

def is_time_remaining(actual_moment, time_limit):
    return (time_limit - actual_moment) > 0

def parse_state(raw_state):
    prepared_state = parse_board(raw_state.board)
    return prepared_state

def parse_board(board):
    res = []
    for row in range(ROWS):
        for col in range(COLS):
            pos = board[row][col]
            if pos is None:
                res.append(0)
            else:
                if pos.color == WHITE:
                    res.append(1)
                else:
                    res.append(2)
    return res