import pygame as pg
from .colors import BLACK, WHITE
from .game_config import SQUARE_SIZE

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.x = 0
        self.y = 0
        self.calculate_position()

    def calculate_position(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def change_color(self):
        if self.color == WHITE:
            self.color = BLACK
        else:
            self.color = WHITE
    
    def draw_piece(self, screen):
        pass