WIDTH = 800
HEIGHT = 800
ROWS = 8
COLS = 8
SQUARE_SIZE = WIDTH // COLS
DIRECTIONS = {
        'right': (1, 0),
        'left': (-1, 0),
        'up': (0, 1),
        'down': (0, -1),
        'up_right': (1, 1),
        'up_left': (-1, 1),
        'down_right': (1, -1),
        'down_left': (-1, -1)
    }