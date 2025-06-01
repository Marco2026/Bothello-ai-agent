import pygame as pg
from othello.board import Board
from othello.game_config import SCREEN_WIDTH, SCREEN_HEIGHT, SQUARE_SIZE, BOARD_HEIGHT, BOARD_WIDTH, MODE, GameMode, AGENT_MOVE_TIME
from othello.colors import BLACK
from agent.agent import Agent

pg.init()
pg.font.init()

FPS = 60
NAME = "Othello Game"
SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
FONT = pg.font.Font("othello/assets/bahnschrift.ttf", 30)

pg.display.set_caption(NAME)
screen = pg.display.set_mode(SIZE)


def main():
    board = Board()
    board.build_initial_board()

    running = True
    clock = pg.time.Clock()

    last_move_time = pg.time.get_ticks()
    
    if MODE != GameMode.HUMAN_VS_HUMAN: 
        agent= Agent()

    while running:
        clock.tick(FPS)

        board.draw_screen(screen)

        turn_information = FONT.render(f"The turn is: {board.turn}", True, BLACK)
        if board.current_player is None and len(board.possible_movements) == 0:
            current_player_information = FONT.render("Game Over!", True, BLACK)
        else: current_player_information = FONT.render(f"Current player: {get_color_from_rgb(board.current_player)}", True, BLACK)
        white_pieces_information = FONT.render(f"White pieces: {board.white_pieces}", True, BLACK)
        black_pieces_information = FONT.render(f"Black pieces: {board.black_pieces}", True, BLACK)

        screen.blit(turn_information, (10, BOARD_HEIGHT + 10))
        screen.blit(current_player_information, (10, BOARD_HEIGHT + 40))
        screen.blit(black_pieces_information, (BOARD_WIDTH - 250, BOARD_HEIGHT + 10))
        screen.blit(white_pieces_information, (BOARD_WIDTH - 250, BOARD_HEIGHT + 40))
        current_time = pg.time.get_ticks()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        if MODE == GameMode.HUMAN_VS_AGENT:
            if board.current_player is BLACK:
                if event.type == pg.MOUSEBUTTONDOWN:
                    last_move_time = current_time
                    put_human_piece(board)
            else:
                if current_time - last_move_time > AGENT_MOVE_TIME:
                    last_move_time = current_time
                    put_agent_piece(agent, board)
        elif MODE == GameMode.AGENT_VS_AGENT:
            if current_time - last_move_time > AGENT_MOVE_TIME:
                last_move_time = current_time
                put_agent_piece(agent, board)
        else:
            if event.type == pg.MOUSEBUTTONDOWN:
                put_human_piece(board)

       
        pg.display.flip()

    pg.quit()

def put_human_piece(board):
    pos = pg.mouse.get_pos()
    row, col = get_row_col_from_mouse(pos)
    board.put_piece(row, col)

def put_agent_piece(agent, board):
    if not board.possible_movements:
        return
    agent.make_decision(board)
    row, col = agent.action
    board.put_piece(row, col)

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def get_color_from_rgb(rgb_color):
    res = "unknown color"
    if rgb_color == (0, 0, 0):
        res = "Black"
    elif rgb_color == (255, 255, 255):
        res = "White"
    return res 

main()
