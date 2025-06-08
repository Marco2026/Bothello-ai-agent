import os
from pathlib import Path
import sys
import threading
import time
import pygame as pg
import random
from othello.board import Board
import othello.game_config as gc
from othello.colors import BLACK, WHITE
from agent.agent import Agent
from othello.button import Button
from othello.training_data_generator import delete_all_temp_csv

pg.init()
pg.font.init()

FPS = 60
NAME = "Othello Game"
SIZE = (gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT)
FONT = pg.font.Font("othello/assets/bahnschrift.ttf", 30)
SMALL_FONT = pg.font.Font("othello/assets/bahnschrift.ttf", 18)
MENU_BACKGROUND = pg.image.load("othello/assets/othello_menu_background_blurred.jpg")

BUTTON_MENU = pg.image.load("othello/assets/button_menu.png")
BUTTON_MENU_DISABLED = pg.image.load("othello/assets/button_menu_disabled.png")
BUTTON_SMALL_TEXT = pg.image.load("othello/assets/button_small_text.png")
BUTTON_SMALL_TEXT_DISABLED = pg.image.load("othello/assets/button_small_text_disabled.png")
BUTTON_TEXT = pg.image.load("othello/assets/button_text.png")


pg.display.set_caption(NAME)
pg.display.set_icon(pg.image.load("othello/assets/white_piece.png"))
screen = pg.display.set_mode(SIZE)


def main_menu():
    running = True
    clock = pg.time.Clock()

    while running:
        clock.tick(FPS)

        MENU_TEXT = FONT.render("Othello, creado por Fran y Marco", True, BLACK)
        MENU_RECT = MENU_TEXT.get_rect(center=(gc.SCREEN_WIDTH // 2,100))
        MOUSE_POS = pg.mouse.get_pos()
        PLAY_BUTTON = Button(image=BUTTON_MENU, pos=(gc.SCREEN_WIDTH // 2, gc.SCREEN_HEIGHT // 2),
                             text_input="PLAY", font=FONT, base_color=BLACK, hovering_color=WHITE)
        if gc.PLAYER_2 == gc.PlayerMode(0) or gc.PLAYER_1 == gc.PlayerMode(0) or not  gc.GENERATE_TRAINING_DATA:
            button = BUTTON_MENU_DISABLED
            hover = BLACK
        else: 
           button = BUTTON_MENU
           hover = WHITE
        SIMULATION_BUTTON = Button(image=button, pos=(gc.SCREEN_WIDTH // 2, gc.SCREEN_HEIGHT // 2 + 100),
                             text_input="SIMULATE", font=FONT, base_color=BLACK, hovering_color=hover)
        OPTIONS_BUTTON = Button(image=BUTTON_MENU, pos=(gc.SCREEN_WIDTH // 2, gc.SCREEN_HEIGHT // 2 + 200),
                             text_input="OPTIONS", font=FONT, base_color=BLACK, hovering_color=WHITE)
        QUIT_BUTTON = Button(image=BUTTON_MENU, pos=(gc.SCREEN_WIDTH // 2, gc.SCREEN_HEIGHT // 2 + 300),
                             text_input="QUIT", font=FONT, base_color=BLACK, hovering_color=WHITE)
        
        screen.blit(MENU_BACKGROUND, (-200,0))
        screen.blit(pg.image.load("othello/assets/button_text.png"), (gc.SCREEN_WIDTH // 12, 75))
        screen.blit(MENU_TEXT, MENU_RECT)
        
        for button in [PLAY_BUTTON, SIMULATION_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MOUSE_POS)
            button.update(screen)
            if button is SIMULATION_BUTTON and not ( gc.PLAYER_2 == gc.PlayerMode(0) or gc.PLAYER_1 == gc.PlayerMode(0) or not gc.GENERATE_TRAINING_DATA):
                button.changeColor(MOUSE_POS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MOUSE_POS):
                    setattr(gc,"SIMULATION_MODE", False)
                    play_game()
                if SIMULATION_BUTTON.checkForInput(MOUSE_POS):
                    setattr(gc,"SIMULATION_MODE", True)
                    simulate_games()
                if OPTIONS_BUTTON.checkForInput(MOUSE_POS):
                    options_menu()
                if QUIT_BUTTON.checkForInput(MOUSE_POS):
                    running = False

        pg.display.flip()

    delete_all_temp_csv()
    pg.quit()

def options_menu():
    screen.fill(BLACK)
    running = True
    clock = pg.time.Clock()

    while running:
        clock.tick(FPS)

        OPTIONS_TEXT = FONT.render("Here you can change the options", True, BLACK)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(gc.SCREEN_WIDTH // 2,100))
        MOUSE_POS = pg.mouse.get_pos()
        PLAYER_1_BUTTON = Button(image=BUTTON_SMALL_TEXT, pos=(gc.SCREEN_WIDTH // 2 - 150, gc.SCREEN_HEIGHT // 2 + 55),
                             text_input=f"PLAYER 1: {parse_player_mode(gc.PLAYER_1)}", font=FONT, base_color=BLACK, hovering_color=WHITE)
        PLAYER_2_BUTTON = Button(image=BUTTON_SMALL_TEXT, pos=(gc.SCREEN_WIDTH // 2 + 150, gc.SCREEN_HEIGHT // 2 + 55),
                             text_input=f"PLAYER 2: {parse_player_mode(gc.PLAYER_2)}", font=FONT, base_color=BLACK, hovering_color=WHITE)
        if gc.PLAYER_1 == gc.PlayerMode(2):
            button1 = BUTTON_SMALL_TEXT
            hover1 = WHITE
        else: 
           button1 = BUTTON_SMALL_TEXT_DISABLED
           hover1 = BLACK
        AGENT_1_BUTTON = Button(image=button1, pos=(gc.SCREEN_WIDTH // 2 -  150, gc.SCREEN_HEIGHT // 2 + 100),
                            text_input=f"{parse_agent_mode(gc.AGENT_1_NEURAL_NETWORK )}", font=SMALL_FONT, base_color=BLACK, hovering_color=hover1)
        if gc.PLAYER_2 == gc.PlayerMode(2):
            button2 = BUTTON_SMALL_TEXT
            hover2 = WHITE
        else: 
           button2 = BUTTON_SMALL_TEXT_DISABLED
           hover2 = BLACK
        AGENT_2_BUTTON = Button(image=button2, pos=(gc.SCREEN_WIDTH // 2 + 150, gc.SCREEN_HEIGHT // 2 + 100),
                            text_input=f"{parse_agent_mode(gc.AGENT_2_NEURAL_NETWORK )}", font=SMALL_FONT, base_color=BLACK, hovering_color=hover2)
        TRAINING_DATA_BUTTON = Button(image=BUTTON_TEXT, pos=(gc.SCREEN_WIDTH // 2, gc.SCREEN_HEIGHT // 2 + 200),
                             text_input=f"GENERATE TRAINING DATA: {gc.GENERATE_TRAINING_DATA}", font=FONT, base_color=BLACK, hovering_color=WHITE)
        
        MENU_BUTTON = Button(image=BUTTON_MENU, pos=(gc.SCREEN_WIDTH // 2, gc.SCREEN_HEIGHT // 2 + 300),
                             text_input="MENU", font=FONT, base_color=BLACK, hovering_color=WHITE)
        
        screen.blit(MENU_BACKGROUND, (-200,0))
        screen.blit(pg.image.load("othello/assets/button_text.png"), (gc.SCREEN_WIDTH // 12, 75))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
        
        
        for button in [PLAYER_1_BUTTON, PLAYER_2_BUTTON, AGENT_1_BUTTON, AGENT_2_BUTTON,TRAINING_DATA_BUTTON, MENU_BUTTON]:
            if button is AGENT_1_BUTTON and gc.PLAYER_1 != gc.PlayerMode(2):
                button.changeColor(MOUSE_POS)
            elif button is AGENT_2_BUTTON and gc.PLAYER_2 != gc.PlayerMode(2):
                button.changeColor(MOUSE_POS)
            else:
                button.changeColor(MOUSE_POS)
            button.update(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if PLAYER_1_BUTTON.checkForInput(MOUSE_POS):
                    change_player_mode("PLAYER_1")
                if PLAYER_2_BUTTON.checkForInput(MOUSE_POS):
                    change_player_mode("PLAYER_2")
                if gc.PLAYER_1 == gc.PlayerMode(2):
                    if AGENT_1_BUTTON.checkForInput(MOUSE_POS):
                        change_agent_mode("AGENT_1_NEURAL_NETWORK", "PLAYER_1")
                if AGENT_2_BUTTON.checkForInput(MOUSE_POS):
                    change_agent_mode("AGENT_2_NEURAL_NETWORK", "PLAYER_2")
                if TRAINING_DATA_BUTTON.checkForInput(MOUSE_POS):
                    change_generate_training_data()
                if MENU_BUTTON.checkForInput(MOUSE_POS):
                    running = False
        pg.display.flip()

def play_game():
    
    running = True
    clock = pg.time.Clock()

    board = Board()
    board.build_initial_board()
    last_move_time = pg.time.get_ticks()
    clic_position = (99, 99)    
    agent1 = Agent(gc.AGENT_1_NEURAL_NETWORK)
    agent2 = Agent(gc.AGENT_2_NEURAL_NETWORK)
    
    

    while running:
        clock.tick(FPS)
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
            mode = gc.PLAYER_1
            agent = agent1
        else:
            mode = gc.PLAYER_2
            agent = agent2
            
        if mode == gc.PlayerMode(0):
            put_human_piece(board, clic_position)
            last_move_time
        elif mode == gc.PlayerMode(1) and current_time - last_move_time >= gc.BOT_MOVE_TIME:
            put_bot_piece(board)
            last_move_time = pg.time.get_ticks()
        elif mode == gc.PlayerMode(2) and not agent.is_thinking:
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

def change_generate_training_data():
    gc.GENERATE_TRAINING_DATA = not gc.GENERATE_TRAINING_DATA

def parse_player_mode(player_mode):
    res = player_mode.name.replace('_', ' ').title()
    return res

def change_player_mode(player_name):
    current_mode = getattr(gc, player_name)
    new_mode = gc.PlayerMode((current_mode.value + 1) % 3)
    setattr(gc, player_name, new_mode)
    return new_mode

def parse_agent_mode(agent):
    res = "Unknown"
    if agent is None:
        res= "UCT without Neural Network"
    else :
        res = agent.name.replace('_', ' ').title()
    return res

def change_agent_mode(agent, player_name): # Descomentar cuando se implemente la red neuronal
    pass
    # current_mode = getattr(gc, player_name)
    # if current_mode != gc.PlayerMode(2):
    #     return
    # current_agent = getattr(gc, agent)
    # if current_agent is None:
    #     new_agent = gc.NeuralNetwork(0)
    # else:
    #     current_agent = getattr(gc, agent)
    #     if current_agent.value == len(gc.NeuralNetwork) - 1 :
    #         new_agent = None
    #     else:
    #         new_agent = gc.NeuralNetwork((current_agent.value + 1))
    # setattr(gc, agent, new_agent)
    # return new_agent
    
def simulate_games (num_games = gc.SIMULATIONS):  
    tick = "\u2714"
    if gc.PLAYER_1 == gc.PlayerMode(0) or gc.PLAYER_2 == gc.PlayerMode(0):
        return
    i=0
    while i< num_games and  gc.SIMULATION_MODE:
        print(f"Simulating game {i+1} / {num_games}")
        play_game()
        if gc.SIMULATION_MODE:
            i += 1
            print(f"{tick} Game {i} / {num_games} simulated succesfully.")
    if i == num_games: print(f"{tick} Simulated {num_games} games successfully.")
    else: 
        if i<1: plural = "s"
        else: plural = ""
        cross = "\u2716"
        print(f"{cross} Simulation stopped after {i} completed game{plural}.")

main_menu()
