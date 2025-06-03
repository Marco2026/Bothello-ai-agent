import pygame as pg
from othello.board import Board
import othello.game_config as gc
from othello.colors import BLACK, WHITE
from agent.agent import Agent
from othello.button import Button

pg.init()
pg.font.init()

FPS = 60
NAME = "Othello Game"
SIZE = (gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT)
FONT = pg.font.Font("othello/assets/bahnschrift.ttf", 30)
MENU_BACKGROUND = pg.image.load("othello/assets/othello_menu_background_blurred.jpg")

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

        screen.blit(MENU_BACKGROUND, (-200,0))
        screen.blit(pg.image.load("othello/assets/text_menu_rect.png"), (gc.SCREEN_WIDTH // 12, 75))
        
        MOUSE_POS = pg.mouse.get_pos()
        PLAY_BUTTON = Button(image=pg.image.load("othello/assets/button_rect.png"), pos=(gc.SCREEN_WIDTH // 2, gc.SCREEN_HEIGHT // 2),
                             text_input="PLAY", font=FONT, base_color=BLACK, hovering_color=WHITE)
        OPTIONS_BUTTON = Button(image=pg.image.load("othello/assets/button_rect.png"), pos=(gc.SCREEN_WIDTH // 2, gc.SCREEN_HEIGHT // 2 + 100),
                             text_input="OPTIONS", font=FONT, base_color=BLACK, hovering_color=WHITE)
        QUIT_BUTTON = Button(image=pg.image.load("othello/assets/button_rect.png"), pos=(gc.SCREEN_WIDTH // 2, gc.SCREEN_HEIGHT // 2 + 200),
                             text_input="QUIT", font=FONT, base_color=BLACK, hovering_color=WHITE)
        
        screen.blit(MENU_TEXT, MENU_RECT)
        
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MOUSE_POS)
            button.update(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MOUSE_POS):
                    play_game()
                if OPTIONS_BUTTON.checkForInput(MOUSE_POS):
                    options_menu()
                if QUIT_BUTTON.checkForInput(MOUSE_POS):
                    running = False

        pg.display.flip()
    pg.quit()

def options_menu():
    screen.fill(BLACK)
    running = True
    clock = pg.time.Clock()

    while running:
        clock.tick(FPS)

        OPTIONS_TEXT = FONT.render("Here you can change the options", True, BLACK)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(gc.SCREEN_WIDTH // 2,100))

        screen.blit(MENU_BACKGROUND, (-200,0))
        screen.blit(pg.image.load("othello/assets/text_menu_rect.png"), (gc.SCREEN_WIDTH // 12, 75))

        MOUSE_POS = pg.mouse.get_pos()
        MODE_BUTTON = Button(image=pg.image.load("othello/assets/text_menu_rect.png"), pos=(gc.SCREEN_WIDTH // 2, gc.SCREEN_HEIGHT // 2),
                             text_input=f"CHANGE MODE: {parse_mode(gc.MODE)}", font=FONT, base_color=BLACK, hovering_color=WHITE)
        TRAINING_DATA_BUTTON = Button(image=pg.image.load("othello/assets/text_menu_rect.png"), pos=(gc.SCREEN_WIDTH // 2, gc.SCREEN_HEIGHT // 2 + 100),
                             text_input=f"GENERATE TRAINING DATA: {gc.GENERATE_TRAINING_DATA}", font=FONT, base_color=BLACK, hovering_color=WHITE)
        MENU_BUTTON = Button(image=pg.image.load("othello/assets/button_rect.png"), pos=(gc.SCREEN_WIDTH // 2, gc.SCREEN_HEIGHT // 2 + 200),
                             text_input="MENU", font=FONT, base_color=BLACK, hovering_color=WHITE)
        
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
        
        for button in [MODE_BUTTON, TRAINING_DATA_BUTTON, MENU_BUTTON]:
            button.changeColor(MOUSE_POS)
            button.update(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if MODE_BUTTON.checkForInput(MOUSE_POS):
                    change_mode()
                if TRAINING_DATA_BUTTON.checkForInput(MOUSE_POS):
                    change_generate_training_data()
                if MENU_BUTTON.checkForInput(MOUSE_POS):
                    main_menu()

        pg.display.flip()

def play_game():
    screen.fill(BLACK)
    board = Board()
    board.build_initial_board()

    running = True
    clock = pg.time.Clock()

    last_move_time = pg.time.get_ticks()
    
    if gc.MODE != gc.MODE.HUMAN_VS_HUMAN: 
        agent = Agent()

    while running:
        clock.tick(FPS)
        screen.fill(BLACK)
        board.draw_screen(screen)

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
        current_time = pg.time.get_ticks()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if gc.MODE == gc.MODE.HUMAN_VS_AGENT and board.current_player is BLACK:
                    last_move_time = current_time
                    put_human_piece(board)
                elif gc.MODE == gc.MODE.HUMAN_VS_HUMAN:
                    put_human_piece(board)

        if gc.MODE == gc.MODE.HUMAN_VS_AGENT and board.current_player is WHITE:
            if current_time - last_move_time > gc.AGENT_MOVE_TIME:
                last_move_time = current_time
                put_agent_piece(agent, board)

        elif gc.MODE == gc.MODE.AGENT_VS_AGENT:
            if current_time - last_move_time > gc.AGENT_MOVE_TIME:
                last_move_time = current_time
                put_agent_piece(agent, board)
        
        if board.black_pieces + board.white_pieces == gc.ROWS * gc.COLS:
            board.finish_game()
        
        pg.display.flip()


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

def change_mode():
    if gc.MODE == gc.MODE.HUMAN_VS_HUMAN:
        gc.MODE = gc.MODE.HUMAN_VS_AGENT
    elif gc.MODE == gc.MODE.HUMAN_VS_AGENT:
        gc.MODE = gc.MODE.AGENT_VS_AGENT
    else:
        gc.MODE = gc.MODE.HUMAN_VS_HUMAN

def change_generate_training_data():
    gc.GENERATE_TRAINING_DATA = not gc.GENERATE_TRAINING_DATA

def parse_mode(mode):
    res = "Unknown"
    match mode:
        case gc.MODE.HUMAN_VS_HUMAN:
            res = "Human vs Human"
        case gc.MODE.HUMAN_VS_AGENT:
            res = "Human vs Agent"
        case gc.MODE.AGENT_VS_AGENT:
            res = "Agent vs Agent"
    return res

main_menu()
