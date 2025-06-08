import pygame as pg
import game.game_const as gc
import game.game_var as gv
from game.game_assets import FONT, MENU_BACKGROUND, BUTTON_MENU, BUTTON_MENU_DISABLED, WHITE_PIECE

from game.colors import BLACK, WHITE
from game.button import Button
from othello.training_data_generator import delete_all_temp_csv
from game.play_game import play_game
from game.options_menu import options_menu, simulate_games

pg.init()

pg.display.set_caption(gc.NAME)
pg.display.set_icon(WHITE_PIECE)
screen = pg.display.set_mode(gc.SIZE)


def main_menu():
    running = True
    clock = pg.time.Clock()

    while running:
        clock.tick(gc.FPS)

        MENU_TEXT = FONT.render("Othello, creado por Fran y Marco", True, BLACK)
        MENU_RECT = MENU_TEXT.get_rect(center=(gc.SCREEN_WIDTH // 2,100))
        MOUSE_POS = pg.mouse.get_pos()
        PLAY_BUTTON = Button(image=BUTTON_MENU, pos=(gc.SCREEN_WIDTH // 2, gc.SCREEN_HEIGHT // 2),
                             text_input="PLAY", font=FONT, base_color=BLACK, hovering_color=WHITE)
        if gv.PLAYER_2 == gv.PlayerMode(0) or gv.PLAYER_1 == gv.PlayerMode(0) or not  gv.GENERATE_TRAINING_DATA:
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
        screen.blit(pg.image.load("game/assets/button_text.png"), (gc.SCREEN_WIDTH // 12, 75))
        screen.blit(MENU_TEXT, MENU_RECT)
        
        for button in [PLAY_BUTTON, SIMULATION_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MOUSE_POS)
            button.update(screen)
            if button is SIMULATION_BUTTON and not ( gv.PLAYER_2 == gv.PlayerMode(0) or gv.PLAYER_1 == gv.PlayerMode(0) or not gv.GENERATE_TRAINING_DATA):
                button.changeColor(MOUSE_POS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MOUSE_POS):
                    setattr(gc,"SIMULATION_MODE", False)
                    play_game()
                if gv.GENERATE_TRAINING_DATA or gv.PLAYER_2 == gv.PlayerMode(0) or gv.PLAYER_1 == gv.PlayerMode(0):
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


main_menu()
