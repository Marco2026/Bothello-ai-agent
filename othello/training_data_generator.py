from game.colors import WHITE, BLACK
import game.game_var as gv
from game.game_const import ROWS, COLS
import csv
import os
from pathlib import Path

LETTERS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n"]
NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]


def parse_filename():
    if not gv.GENERATE_TRAINING_DATA:
        return 
    player_1 = gv.PLAYER_1.name
    agent_1_type = ""
    if gv.PLAYER_1 == gv.PlayerMode.AGENT:
        if gv.AGENT_1_NEURAL_NETWORK is None:
            agent_1_type = "_UCT"
        else:
            agent_1_type = "_" + gv.AGENT_1_NEURAL_NETWORK.name
    player_2 = gv.PLAYER_2.name
    agent_2_type = ""
    if gv.PLAYER_2 == gv.PlayerMode.AGENT:
        if gv.AGENT_1_NEURAL_NETWORK is None:
            agent_2_type = "_UCT"
        else:
            agent_2_type = "_" + gv.AGENT_1_NEURAL_NETWORK.name
    return "agent/training/games/" + player_1 + agent_1_type + "vs" + player_2 + agent_2_type + ".csv"
   

def training_data_initializer(temp_file):
    if not gv.GENERATE_TRAINING_DATA:
        return
    file = parse_filename()
    if not Path(file).exists():
        with open(file, "w") as f:
            f.write(parse_state() + "current_player_won\n")

    if Path(temp_file).exists():
        os.remove(temp_file)

def training_data_generator(state, temp_file):
    board = parse_board(state.board)
    current_player = str(state.current_player)

    with open(temp_file, mode="a", newline="\n") as f:
        f.write(board + current_player + "\n")
        

    pieces = state.white_pieces + state.black_pieces
    if pieces == ROWS * COLS:
        player_winner = get_player_winner(state.white_pieces, state.black_pieces)
        last_move_formatter(player_winner, temp_file)


def last_move_formatter(player_winner, temp_file):
    file = parse_filename()
    moves = []
    with open(temp_file, mode="r", encoding="UTF-8", newline="\n") as f:
        lector = csv.reader(f, delimiter=";")
        next(lector)
        for line in lector:  
            if len(line) < ROWS* COLS:
                continue              
            moves.append((line[:-1], parse_winner(line[-1], player_winner)))

    with open(file, mode="a", newline="\n") as f:
        for move in moves:
            f.write(parse_move(move))



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


def delete_all_temp_csv():
    temp_folder = Path("agent/training/temp")
    if not temp_folder.exists():
        return
    
    for file in temp_folder.glob("*.csv"):
        os.remove(file)


            



