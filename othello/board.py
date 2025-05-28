import pygame as pg
from .game_config import WIDTH, HEIGHT, ROWS, COLS, SQUARE_SIZE
from .colors import BLACK, GREEN

class Board:
    def __init__(self):
        self.board = []
        self.turn = 0
        self.selected_piece = None
        self.possible_placements = None
        self.white_pieces = 2
        self.black_pieces = 2

    def draw_board(self, screen):
        screen.fill(GREEN)

        for i in range(ROWS + 1):
            pg.draw.line(screen, BLACK, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), 2)
        
        for j in range (COLS + 1):
            pg.draw.line(screen, BLACK, (j * SQUARE_SIZE, 0), (j * SQUARE_SIZE, HEIGHT), 2)

    def draw_pieces(self, screen):
        pass

    def place_piece(self, position):
        self.board[position[0]][position[1]] = self.selected_piece
        self.selected_piece = None