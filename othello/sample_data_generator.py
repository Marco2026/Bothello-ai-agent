from .colors import WHITE
from .game_config import ROWS, COLS
import csv

FILE = "agent/training/sample_data.csv"

def sample_data_generator(state):
    board = parse_board(state.board)
    current_player = str(state.current_player)  
    
    with open(FILE, mode="a", newline="\n") as f:
        f.write(str(board) + current_player + "\n")

    pieces = state.white_pieces + state.black_pieces
    if pieces == ROWS * COLS:
        last_move_formatter(current_player)
        
def last_move_formatter(current_player):
    # Esta funcion tiene que tomar el ultimo jugador del juego, comprobar si ha ganado, y poner en cada fila escrita si el jugador gano o perdio
    # Como hay dos problemas (encontrar la primera linea a partir de la cual se gano o perdio, y cambiar ciertas lineas del fichero), creo que lo
    # mejor sería crear un fichero auxiliar y, desde esta funcion añadir los datos al fichero que tenga todos los datos despues de tratarlos
    pass

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
    res = res[:-1] + ","
    return res