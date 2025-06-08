import pygame as pg

pg.init
pg.font.init()
FONT = pg.font.Font("game/assets/bahnschrift.ttf", 30)
SMALL_FONT = pg.font.Font("game/assets/bahnschrift.ttf", 18)

MENU_BACKGROUND = pg.image.load("game/assets/othello_menu_background_blurred.jpg")

BUTTON_MENU = pg.image.load("game/assets/button_menu.png")
BUTTON_MENU_DISABLED = pg.image.load("game/assets/button_menu_disabled.png")
BUTTON_SMALL_TEXT = pg.image.load("game/assets/button_small_text.png")
BUTTON_SMALL_TEXT_DISABLED = pg.image.load("game/assets/button_small_text_disabled.png")
BUTTON_TEXT = pg.image.load("game/assets/button_text.png")

WHITE_PIECE = pg.image.load('game/assets/white_piece.png')