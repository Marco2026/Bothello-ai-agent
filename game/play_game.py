import os
from pathlib import Path
import threading
import time
import pygame as pg
import random
from othello.board import Board
import game.game_var as gv
import game.game_const as gc
from game.game_assets import FONT, WHITE_PIECE
from .colors import BLACK, WHITE
from agent.agent import Agent


pg.init()

pg.display.set_caption(gc.NAME)
pg.display.set_icon(WHITE_PIECE)
screen = pg.display.set_mode(gc.SIZE)


def play_game():
    
    running = True
    clock = pg.time.Clock()

    board = Board()
    board.build_initial_board()
    last_move_time = pg.time.get_ticks()
    clic_position = (99, 99)    
    agent1 = Agent(gv.AGENT_1_NEURAL_NETWORK)
    agent2 = Agent(gv.AGENT_2_NEURAL_NETWORK)
    
    

    while running:
        clock.tick(gc.FPS)
        screen.fill(BLACK)
        board.draw_screen(screen)
        current_time = pg.time.get_ticks()

        turn_information = FONT.render(f"The turn is: {board.turn}", True, BLACK)
        if board.game_finished: 
            if board.winner is None: message = "It's a draw"
            else : message = f"{get_color_from_rgb(board.winner)} wins"
            current_player_information = FONT.render(f"Game Over! {message}", True, BLACK)
        else: current_player_information = FONT.render(f"Current player: {get_color_from_rgb(board.current_player)}", True, BLACK)
        white_pieces_information = FONT.render(f"White pieces: {board.white_pieces}", True, BLACK)
        black_pieces_information = FONT.render(f"Black pieces: {board.black_pieces}", True, BLACK)

        screen.blit(turn_information, (10, gc.BOARD_HEIGHT + 10))
        screen.blit(current_player_information, (10, gc.BOARD_HEIGHT + 40))
        screen.blit(black_pieces_information, (gc.BOARD_WIDTH - 250, gc.BOARD_HEIGHT + 10))
        screen.blit(white_pieces_information, (gc.BOARD_WIDTH - 250, gc.BOARD_HEIGHT + 40))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                setattr(gc, "SIMULATION_MODE", False)
            if event.type == pg.MOUSEBUTTONDOWN:
                clic_position = pg.mouse.get_pos()

        if board.current_player is BLACK:
            mode = gv.PLAYER_1
            agent = agent1
        else:
            mode = gv.PLAYER_2
            agent = agent2
            
        if mode == gv.PlayerMode(0):
            put_human_piece(board, clic_position)
            last_move_time
        elif mode == gv.PlayerMode(1) and current_time - last_move_time >= gc.BOT_MOVE_TIME:
            put_bot_piece(board)
            last_move_time = pg.time.get_ticks()
        elif mode == gv.PlayerMode(2) and not agent.is_thinking:
            agent.is_thinking = True
            put_agent_piece(board, agent)
            last_move_time = pg.time.get_ticks()
        
        if board.game_finished and gc.SIMULATION_MODE:
            while Path(board.temp_csv_file).exists():
                time.sleep(0.05)
                try:
                    os.remove(board.temp_csv_file)
                    # trash_bin = "\U0001F5D1"
                    # print(f"{trash_bin} Deleted file: {board.temp_csv_file}")
                except OSError as e:
                    print(f"Error deleting file {board.temp_csv_file}: {e}")
                
            running = False

        pg.display.flip()

def put_human_piece(board,pos):
    row, col = get_row_col_from_mouse(pos)
    board.put_piece(row, col)

def put_bot_piece(board):
    if not board.possible_movements:
        return
    row, col = random.choice(board.possible_movements)
    board.put_piece(row, col)
    
def put_agent_piece(board, agent):
    def decide():
        if not board.possible_movements:
            return
        agent.make_decision(board)
        row, col = agent.action
        board.put_piece(row, col)
    threading.Thread(target=decide).start()
    


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // gc.SQUARE_SIZE
    col = x // gc.SQUARE_SIZE
    return row, col

def get_color_from_rgb(rgb_color):
    res = "unknown color"
    if rgb_color == BLACK:
        res = "Black"
    elif rgb_color == WHITE:
        res = "White"
    return res 
