import pygame as pg
from othello.board import Board
from othello.game_config import WIDTH, HEIGHT

# Constants for the game
FPS = 60
NAME = "Othello Game"
SIZE = (WIDTH, HEIGHT)

pg.init()
pg.display.set_caption(NAME)
screen = pg.display.set_mode(SIZE)

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

        board.draw_screen(screen)

        pg.display.flip()


    pg.quit()

main()
