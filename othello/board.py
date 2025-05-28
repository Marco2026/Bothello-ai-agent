import pygame

# Constants for the game board
WIDTH = 800
HEIGHT = 800
ROWS = 8
COLS = 8
SQUARE_SIZE = WIDTH // COLS

# Colors used in the game in rgb format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (20,134,58)

class Board:
    def __init__(self):
        self.board = [[],
                      []]
        self.turn = 0
        self.selected_piece = None
        self.possible_placements = None
        self.white_pieces = 2
        self.black_pieces = 2

    def place_piece(self):
        pass