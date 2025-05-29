import pygame as pg
from .game_config import WIDTH, HEIGHT, ROWS, COLS, SQUARE_SIZE
from .colors import BLACK, WHITE, GREEN_BASE, GREEN, WOODEN
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.turn = 0
        self.selected_piece = None 
        self.possible_placements = [(2,2), (2,3), (2,4), (2,5), (3,2), (3,5), (4,2), (4,5), (5,2), (5,3), (5,4), (5,5)] 
        self.white_pieces = 2
        self.black_pieces = 2
        self.build_initial_board()
        self.current_player = WHITE
         

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
            self.board[row][col] = Piece(row, col, color=self.current_player)
            self.change_current_player()
            self.turn += 1

    def change_current_player(self): # Mejorar cuando tengamos la lista de posibles movimientos
        if self.current_player == WHITE:
            self.current_player = BLACK
        else:
            self.current_player = WHITE
        self.selected_piece = None
        # self.possible_placements = [] 

    def draw_board(self, screen):
        screen.fill(GREEN)
        for row in range(ROWS + 1):
            pg.draw.line(screen, BLACK, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), 2)
        for col in range (COLS + 1):
            pg.draw.line(screen, BLACK, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), 2)


    def draw_movements(self, screen, current_player=None, possible_movements=None):
        if not possible_movements:
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


    def draw_pieces(self, screen):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != None:
                    piece.draw_piece(screen)

    def draw_screen(self, screen):
        self.draw_board(screen)
        self.draw_pieces(screen)
        self.draw_movements(screen, current_player=self.current_player, possible_movements=self.possible_placements)

    def place_piece(self, position):
        self.board[position[0]][position[1]] = self.selected_piece
        self.selected_piece = None
        