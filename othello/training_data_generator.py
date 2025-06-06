from .colors import WHITE, BLACK
from .game_config import ROWS, COLS, SIMULATION_MODE
import csv
import os
from pathlib import Path

LETTERS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n"]
NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]

FILE = "agent/training/training_data.csv"
TEMP_FILE = "agent/training/training_data_for_current_game.csv"

def training_data_initializer():
    if not Path(FILE).exists():
        f = open(FILE, "w")
        f.write(parse_state() + "current_player_won" + "\n")
        f.close()
    if Path(TEMP_FILE).exists(): os.remove(TEMP_FILE)
    with open(TEMP_FILE, mode="a", newline="\n") as f:
        f.write(parse_state() + "current_player_won" + "\n")

def training_data_generator(state):
    board = parse_board(state.board)
    current_player = str(state.current_player)  
    
    with open(TEMP_FILE, mode="a", newline="\n") as f:
        f.write(board + current_player + "\n")

    pieces = state.white_pieces + state.black_pieces
    if pieces == ROWS * COLS:
        player_winner = get_player_winner(state.white_pieces, state.black_pieces)
        last_move_formatter(player_winner)
        
def last_move_formatter(player_winner):
    moves = []
    with open(TEMP_FILE, mode="r", encoding="UTF-8", newline="\n") as f:
        lector = csv.reader(f, delimiter=";")
        next(lector)
        for line in lector:
            moves.append((line[:-1], parse_winner(line[-1], player_winner)))
    
    with open(FILE, mode="a", newline="\n") as f:
        for move in moves:
            f.write(parse_move(move))

    if not SIMULATION_MODE: os.remove(TEMP_FILE)

def get_player_winner(white_pieces, black_pieces):
    res = None
    if white_pieces > black_pieces:
        res = WHITE
    elif white_pieces < black_pieces:
        res = BLACK
    return res 

def parse_board(board):
    res = ''
    for row in range(ROWS):
        for col in range(COLS):
            pos = board[row][col]
            if pos is None:
                res = res + "0;"
            else:
                if pos.color == WHITE:
                    res = res + "1;"
                else:
                    res = res + "2;"
    return res

def parse_winner(current_player, player_winner):
    res = "0"
    if player_winner is not None:
        if str(current_player) == str(player_winner):
            res = "1"
        else:
            res = "-1"
    return res

def parse_state():
    res = ""
    for row in range(ROWS):
        for col in range(COLS):
            res += LETTERS[row] + NUMBERS[col] + ";"
    return res

def parse_move(move):
    return ';'.join(move[0]) + ";" + move[1] + "\n"