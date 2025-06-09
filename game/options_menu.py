import pygame as pg

import game.game_const as gc
import game.game_var as gv
from game.game_assets import FONT, SMALL_FONT,MENU_BACKGROUND, BUTTON_MENU, BUTTON_SMALL_TEXT, BUTTON_SMALL_TEXT_DISABLED, BUTTON_TEXT
from .colors import BLACK, WHITE
from .button import Button
from .play_game import play_game

pg.init()



pg.display.set_caption(gc.NAME)
pg.display.set_icon(pg.image.load("game/assets/white_piece.png"))
screen = pg.display.set_mode(gc.SIZE)


def options_menu():
    screen.fill(BLACK)
    running = True
    clock = pg.time.Clock()

    while running:
        clock.tick(gc.FPS)

        OPTIONS_TEXT = FONT.render("Here you can change the options", True, BLACK)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(gc.SCREEN_WIDTH // 2,100))
        MOUSE_POS = pg.mouse.get_pos()
        PLAYER_1_BUTTON = Button(image=BUTTON_SMALL_TEXT, pos=(gc.SCREEN_WIDTH // 2 - 150, gc.SCREEN_HEIGHT // 2 + 55),
                             text_input=f"PLAYER 1: {parse_player_mode(gv.PLAYER_1)}", font=FONT, base_color=BLACK, hovering_color=WHITE)
        PLAYER_2_BUTTON = Button(image=BUTTON_SMALL_TEXT, pos=(gc.SCREEN_WIDTH // 2 + 150, gc.SCREEN_HEIGHT // 2 + 55),
                             text_input=f"PLAYER 2: {parse_player_mode(gv.PLAYER_2)}", font=FONT, base_color=BLACK, hovering_color=WHITE)
        if gv.PLAYER_1 == gv.PlayerMode(2):
            button1 = BUTTON_SMALL_TEXT
            hover1 = WHITE
        else: 
           button1 = BUTTON_SMALL_TEXT_DISABLED
           hover1 = BLACK
        AGENT_1_BUTTON = Button(image=button1, pos=(gc.SCREEN_WIDTH // 2 -  150, gc.SCREEN_HEIGHT // 2 + 100),
                            text_input=f"{parse_agent_mode(gv.AGENT_1_NEURAL_NETWORK )}", font=SMALL_FONT, base_color=BLACK, hovering_color=hover1)
        if gv.PLAYER_2 == gv.PlayerMode(2):
            button2 = BUTTON_SMALL_TEXT
            hover2 = WHITE
        else: 
           button2 = BUTTON_SMALL_TEXT_DISABLED
           hover2 = BLACK
        AGENT_2_BUTTON = Button(image=button2, pos=(gc.SCREEN_WIDTH // 2 + 150, gc.SCREEN_HEIGHT // 2 + 100),
                            text_input=f"{parse_agent_mode(gv.AGENT_2_NEURAL_NETWORK )}", font=SMALL_FONT, base_color=BLACK, hovering_color=hover2)
        TRAINING_DATA_BUTTON = Button(image=BUTTON_TEXT, pos=(gc.SCREEN_WIDTH // 2, gc.SCREEN_HEIGHT // 2 + 200),
                             text_input=f"GENERATE TRAINING DATA: {gv.GENERATE_TRAINING_DATA}", font=FONT, base_color=BLACK, hovering_color=WHITE)
        
        MENU_BUTTON = Button(image=BUTTON_MENU, pos=(gc.SCREEN_WIDTH // 2, gc.SCREEN_HEIGHT // 2 + 300),
                             text_input="MENU", font=FONT, base_color=BLACK, hovering_color=WHITE)
        
        screen.blit(MENU_BACKGROUND, (-200,0))
        screen.blit(pg.image.load("game/assets/button_text.png"), (gc.SCREEN_WIDTH // 12, 75))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
        
        
        for button in [PLAYER_1_BUTTON, PLAYER_2_BUTTON, AGENT_1_BUTTON, AGENT_2_BUTTON,TRAINING_DATA_BUTTON, MENU_BUTTON]:
            if button is AGENT_1_BUTTON and gv.PLAYER_1 != gv.PlayerMode(2):
                button.changeColor(MOUSE_POS)
            elif button is AGENT_2_BUTTON and gv.PLAYER_2 != gv.PlayerMode(2):
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
                if gv.PLAYER_1 == gv.PlayerMode(2):
                    if AGENT_1_BUTTON.checkForInput(MOUSE_POS):
                        change_agent_mode("AGENT_1_NEURAL_NETWORK", "PLAYER_1")
                if gv.PLAYER_2 == gv.PlayerMode(2):
                    if AGENT_2_BUTTON.checkForInput(MOUSE_POS):
                        change_agent_mode("AGENT_2_NEURAL_NETWORK", "PLAYER_2")
                if TRAINING_DATA_BUTTON.checkForInput(MOUSE_POS):
                    setattr(gv, "GENERATE_TRAINING_DATA", not gv.GENERATE_TRAINING_DATA)
                if MENU_BUTTON.checkForInput(MOUSE_POS):
                    running = False
        pg.display.flip()


def parse_player_mode(player_mode):
    res = player_mode.name.replace('_', ' ').title()
    return res

def change_player_mode(player_name):
    current_mode = getattr(gv, player_name)
    new_mode = gv.PlayerMode((current_mode.value + 1) % 3)
    setattr(gv, player_name, new_mode)
    return new_mode

def parse_agent_mode(agent):
    res = "Unknown"
    if agent is None:
        res= "UCT without"
    else :
        res = agent.name.replace('_', ' ').title()
    return res  + " Neural Network"

def change_agent_mode(agent, player_name): 
    current_mode = getattr(gv, player_name)
    if current_mode != gv.PlayerMode(2):
        return
    current_agent = getattr(gv, agent)
    if current_agent is None:
        new_agent = gv.NeuralNetwork(0)
    else:
        current_agent = getattr(gv, agent)
        if current_agent.value == len(gv.NeuralNetwork) - 1 :
            new_agent = None
        else:
            new_agent = gv.NeuralNetwork((current_agent.value + 1))
    setattr(gv, agent, new_agent)
    return new_agent
    
def simulate_games (num_games = gv.SIMULATIONS):  
    tick = "\u2714"
    if gv.PLAYER_1 == gv.PlayerMode(0) or gv.PLAYER_2 == gv.PlayerMode(0):
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