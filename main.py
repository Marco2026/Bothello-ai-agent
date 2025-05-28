import pygame as pg
from othello.board import WIDTH, HEIGHT, ROWS, COLS, GREEN, BLACK, SQUARE_SIZE

# Constants for the game
FPS = 60
NAME = "Othello Game"
SIZE = (WIDTH, HEIGHT)

pg.init()
screen = pg.display.set_mode(SIZE)
pg.display.set_caption(NAME)

def main():
    running = True
    clock = pg.time.Clock() 

    while running:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill(GREEN)
        
        for i in range(ROWS + 1):
            pg.draw.line(screen, BLACK, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), 2)
        
        for j in range (COLS + 1):
            pg.draw.line(screen, BLACK, (j * SQUARE_SIZE, 0), (j * SQUARE_SIZE, HEIGHT), 2)

        pg.display.flip()



    pg.quit()

main()
