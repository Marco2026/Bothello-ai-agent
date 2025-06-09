import pygame as pg
from game.colors import WHITE
from game.game_const import SQUARE_SIZE

WHITE_PIECE = pg.image.load('game/assets/white_piece.png')
BLACK_PIECE = pg.image.load('game/assets/black_piece.png')

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

    def change_color(self, color):
        self.color = color
    
    def draw_piece(self, screen):
        if self.color == WHITE:
            piece = scale_piece(WHITE_PIECE)
        else:
            piece = scale_piece(BLACK_PIECE)
        
        piece_rect = piece.get_rect()
        piece_rect.center = self.col * SQUARE_SIZE + SQUARE_SIZE // 2, self.row * SQUARE_SIZE + SQUARE_SIZE // 2 

        screen.blit(piece, piece_rect)

    def __repr__(self):
        return str(f'Piece(row: {self.row}, col: {self.col}, color:{self.color})')
    
    def copy(self):
        return Piece(self.row, self.col, self.color)
    
def scale_piece(piece):
    return pg.transform.scale(piece, (SQUARE_SIZE, SQUARE_SIZE))