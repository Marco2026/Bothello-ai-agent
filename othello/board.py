import pygame as pg
from .game_config import BOARD_WIDTH, BOARD_HEIGHT, ROWS, COLS, SQUARE_SIZE, PLAY_VS_AGENT
from .colors import BLACK, WHITE, GREEN
from .piece import Piece

DIRECTIONS = {
    'right': (1, 0),
    'left': (-1, 0),
    'up': (0, 1),
    'down': (0, -1),
    'up_right': (1, 1),
    'up_left': (-1, 1),
    'down_right': (1, -1),
    'down_left': (-1, -1)
}

class Board:

    def __init__(self):
        self.board = []
        self.possible_movements = []
        self.turn = 0
        self.last_piece = None 
        self.white_pieces = 2
        self.black_pieces = 2
        self.current_player = BLACK
        self.build_initial_board()

    def build_initial_board(self):
        for row in range(ROWS + 1):
            self.board.append([])
            for col in range(COLS):
                self.board[row].append(None)

        self.board[ROWS // 2 - 1][COLS // 2 - 1] = Piece(ROWS // 2 - 1, COLS // 2 - 1, WHITE) 
        self.board[ROWS // 2 - 1][COLS // 2] = Piece(ROWS // 2 - 1, COLS // 2, BLACK) 
        self.board[ROWS // 2][COLS // 2 - 1] = Piece(ROWS // 2, COLS // 2 - 1, BLACK) 
        self.board[ROWS // 2][COLS // 2] = Piece(ROWS // 2, COLS // 2, WHITE) 

        self.get_possible_movements()

    def put_piece(self, row, col):
        if self.board[row][col] == None and (row,col) in self.possible_movements:
            piece = Piece(row, col, color=self.current_player)
            self.board[row][col] = piece
            self.last_piece = piece
            self.capture_pieces() 
            self.change_current_player()
            self.update_number_of_pieces()
            self.turn += 1

    def change_current_player(self):
        if self.current_player == WHITE: self.current_player = BLACK 
        else: self.current_player = WHITE 
        self.get_possible_movements()

        if len(self.possible_movements) == 0:
            if self.current_player == WHITE: self.current_player = BLACK 
            else: self.current_player = WHITE 
            self.get_possible_movements()

            if not self.possible_movements:
                self.current_player = None

    def get_possible_movements(self):
        res = set()
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] is None and self.valid_movement(row, col):
                    res.add((row, col))

        self.possible_movements = list(res)
        
    def valid_movement(self, row, col):
        future_piece = Piece(row, col, self.current_player)
        res = False
        for direction in DIRECTIONS.keys():
            pieces_to_capture = self.get_pieces_direction(future_piece, direction)
            if len(pieces_to_capture) > 1 and pieces_to_capture[-1].color == self.current_player:
                res = True
                break
        return res


    def capture_pieces(self):
        pieces_to_capture = []
        for direction in DIRECTIONS.keys():
            pieces_to_capture += self.get_pieces_direction(self.last_piece, direction)
        self.change_pieces_color(pieces_to_capture)


    def get_pieces_direction(self, last_piece, direction):
        res = []
        if direction not in DIRECTIONS:
            return res

        dx, dy = DIRECTIONS[direction]
        row, col = last_piece.row, last_piece.col
        
        while True:
            row += dy
            col += dx
            if not (0 <= row < ROWS and 0 <= col < COLS):
                res = []
                break
            piece = self.board[row][col]
            if piece is None:
                res = []
                break
            res.append(piece)
            if piece.color == last_piece.color:
                break
        return res

    def change_pieces_color (self, placed_pieces):
        if not placed_pieces:
            return
        if placed_pieces[-1].color == self.current_player:
            for piece in placed_pieces:
                piece.change_color(self.current_player)
            

    def update_number_of_pieces(self):
        black_number = 0
        white_number = 0
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece is not None:
                    if piece.color is WHITE:
                        white_number += 1
                    else:
                        black_number += 1
        self.white_pieces = white_number
        self.black_pieces = black_number
            
    def draw_screen(self, screen):
        self.draw_board(screen)
        self.draw_pieces(screen)
        self.draw_movements(screen, current_player=self.current_player, possible_movements=self.possible_movements)
                

    def draw_board(self, screen):
        screen.fill(GREEN)
        for row in range(ROWS + 1):
            pg.draw.line(screen, BLACK, (0, row * SQUARE_SIZE), (BOARD_WIDTH, row * SQUARE_SIZE), 2)
        for col in range (COLS + 1):
            pg.draw.line(screen, BLACK, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, BOARD_HEIGHT), 2)

    def draw_pieces(self, screen):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != None:
                    piece.draw_piece(screen)

    def draw_movements(self, screen, current_player=None, possible_movements=None):
        if self.current_player is None:
            for row in range(ROWS + 1):
                pg.draw.line(screen, WHITE, (0, row * SQUARE_SIZE), (BOARD_WIDTH, row * SQUARE_SIZE), 2)
            for col in range (COLS + 1):
                pg.draw.line(screen, WHITE, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, BOARD_HEIGHT), 2) 
            return

        show_flash = (pg.time.get_ticks() // 500) % 2 == 0
    
        if not show_flash:
            return

        highlight = pg.Surface((SQUARE_SIZE - 2, SQUARE_SIZE - 2), pg.SRCALPHA)

        if current_player == WHITE:
            highlight.fill((255, 255, 255, 160))
        elif current_player == BLACK:
            highlight.fill((0, 0, 0, 200))
        else:
            highlight.fill((0, 0, 0, 0))  

        for (row, col) in possible_movements:
            pos = (col * SQUARE_SIZE + 2, row * SQUARE_SIZE + 2)
            screen.blit(highlight, pos)
        