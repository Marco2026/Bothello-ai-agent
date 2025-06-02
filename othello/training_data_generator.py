from .colors import WHITE, BLACK
from .game_config import ROWS, COLS
import csv
import os
from pathlib import Path

FILE = "agent/training/training_data.csv"
TEMP_FILE = "agent/training/training_data_for_current_game.csv"

def training_data_initializer():
    if not Path(FILE).exists():
        f = open(FILE, "w")
        f.write("state;current_player_won" + "\n")
        f.close()
    if Path(TEMP_FILE).exists():
        os.remove(TEMP_FILE)
    with open(TEMP_FILE, mode="a", newline="\n") as f:
        f.write("state;current_player_won" + "\n")

def training_data_generator(state):
    board = parse_board(state.board)
    current_player = str(state.current_player)  
    
    with open(TEMP_FILE, mode="a", newline="\n") as f:
        f.write(str(board) + current_player + "\n")

    pieces = state.white_pieces + state.black_pieces
    if pieces == ROWS * COLS:
        player_winner = get_player_winner(state.white_pieces, state.black_pieces)
        last_move_formatter(player_winner)
        
def last_move_formatter(player_winner):
    moves = []
    with open(TEMP_FILE, mode="r", encoding="UTF-8", newline="\n") as f:
        lector = csv.reader(f, delimiter=";")
        next(lector)
        for state, current_player_won in lector:
            moves.append((state, parse_winner(current_player_won, player_winner)))
    
    with open(FILE, mode="a", newline="\n") as f:
        for state, current_player_won in moves:
            f.write(state + ";" + current_player_won + "\n")

    os.remove(TEMP_FILE)

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
                res = res + "0,"
            else:
                if pos.color == WHITE:
                    res = res + "1,"
                else:
                    res = res + "2,"
    res = res[:-1] + ";"
    return res

def parse_winner(current_player, player_winner):
    res = "0"
    if player_winner is not None:
        if str(current_player) == str(player_winner):
            res = "1"
        else:
            res = "-1"
    return res