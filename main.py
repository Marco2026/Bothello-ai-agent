import pygame as pg
from othello.board import Board
from othello.colors import BLACK
from othello.game_config import WIDTH, HEIGHT

# Constants for the game
FPS = 60
NAME = "Othello Game"
SIZE = (WIDTH, HEIGHT)
WHITE_PIECE = './othello/assets/white_piece.png'
BLACK_PIECE = './othello/assets/black_piece.png'

pg.init()
pg.display.set_caption(NAME)
screen = pg.display.set_mode(SIZE)
white_piece = pg.image.load(WHITE_PIECE)
white_piece.convert()
white_rect = white_piece.get_rect()
white_rect.center = 800 // 2, 800 // 2
black_piece = pg.image.load(BLACK_PIECE)
black_piece.convert()

def main():
    running = True
    clock = pg.time.Clock()
    board = Board()

    while running:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        board.draw_board(screen)
        

        screen.blit(white_piece, white_rect)
        pg.draw.rect(screen, BLACK, white_rect, 1)

        pg.display.flip()


    pg.quit()

main()
