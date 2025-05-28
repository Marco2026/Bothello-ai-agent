import pygame
from othello.board import WIDTH, HEIGHT, BLACK, WHITE

# Constants for the game
FPS = 60
NAME = "Othello Game"
SIZE = (WIDTH, HEIGHT)

pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(NAME)

def main():
    running = True
    clock = pygame.time.Clock() 

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(BLACK)


    pygame.quit()

main()
