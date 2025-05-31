import pygame as pg
from othello.board import Board
from othello.game_config import SCREEN_WIDTH, SCREEN_HEIGHT, SQUARE_SIZE, BOARD_HEIGHT, BOARD_WIDTH
from othello.colors import BLACK

pg.init()
pg.font.init()

FPS = 60
NAME = "Othello Game"
SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
FONT = pg.font.Font("othello/assets/bahnschrift.ttf", 30)

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
        turn_information = FONT.render(f"The turn is: {board.turn}", True, BLACK)
        current_player_information = FONT.render(f"Current player: {get_color_from_rgb(board.current_player)}", True, BLACK)
        white_pieces_information = FONT.render(f"White pieces: {board.white_pieces}", True, BLACK)
        black_pieces_information = FONT.render(f"Black pieces: {board.black_pieces}", True, BLACK)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                board.put_piece(row, col)

        board.draw_screen(screen)
        screen.blit(turn_information, (10, BOARD_HEIGHT + 10))
        screen.blit(current_player_information, (10, BOARD_HEIGHT + 40))
        screen.blit(black_pieces_information, (BOARD_WIDTH - 250, BOARD_HEIGHT + 10))
        screen.blit(white_pieces_information, (BOARD_WIDTH - 250, BOARD_HEIGHT + 40))

        pg.display.flip()

    pg.quit()

def get_color_from_rgb(rgb_color):
    res = "unknown color"
    if rgb_color == (0, 0, 0):
        res = "Black"
    elif rgb_color == (255, 255, 255):
        res = "White"
    return res 

main()
