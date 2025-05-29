import pygame as pg
from .game_config import WIDTH, HEIGHT, ROWS, COLS, SQUARE_SIZE
from .colors import BLACK, WHITE, GREEN
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.turn = 0
        self.selected_piece = None
        self.possible_placements = None
        self.white_pieces = 2
        self.black_pieces = 2
        self.build_initial_board()

    def build_initial_board(self):
        for row in range(ROWS + 1):
            self.board.append([])
            for col in range(COLS):
                self.board[row].append(None)

        self.board[ROWS // 2 - 1][COLS // 2 - 1] = Piece(ROWS // 2 - 1, COLS // 2 - 1, WHITE) # Casilla (4, 4)
        self.board[ROWS // 2 - 1][COLS // 2] = Piece(ROWS // 2 - 1, COLS // 2, BLACK) # Casilla (4, 5)
        self.board[ROWS // 2][COLS // 2 - 1] = Piece(ROWS // 2, COLS // 2 - 1, BLACK) # Casilla (5, 4)
        self.board[ROWS // 2][COLS // 2] = Piece(ROWS // 2, COLS // 2, WHITE) # Casilla (5, 5)

    def put_piece(self, row, col):
        if self.board[row][col] == None:
            self.board[row][col] = Piece(row, col, BLACK)
            self.turn += 1

    def draw_board(self, screen):
        screen.fill(GREEN)
        for row in range(ROWS + 1):
            pg.draw.line(screen, BLACK, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), 2)
        for col in range (COLS + 1):
            pg.draw.line(screen, BLACK, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), 2)

    def draw_pieces(self, screen):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != None:
                    piece.draw_piece(screen)

    def draw_screen(self, screen):
        self.draw_board(screen)
        self.draw_pieces(screen)

    def place_piece(self, position):
        self.board[position[0]][position[1]] = self.selected_piece
        self.selected_piece = None