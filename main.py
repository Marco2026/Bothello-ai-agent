import pygame as pg
from othello.board import Board
from othello.game_config import WIDTH, HEIGHT, SQUARE_SIZE

# Constants for the game
FPS = 60
NAME = "Othello Game"
SIZE = (WIDTH, HEIGHT)

pg.init()
pg.display.set_caption(NAME)
screen = pg.display.set_mode(SIZE)

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    running = True
    clock = pg.time.Clock()
    board = Board()

    board.build_initial_board()

    while running:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                board.put_piece(row, col)

        board.draw_screen(screen)

        pg.display.flip()


    pg.quit()

main()
