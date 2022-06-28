# Constants.py
import pygame



# Contants value for checkers game

# Interface size (width and height)
WIDTH, HEIGHT = 480, 570
# value for 8x8 2D checkers game board
ROWS, COLS = 8, 8
SIZE_BOARD = 8
SIZE_TILE = 60

FPS = 30

# Set the color with RGB value
RED =       (255, 0, 0)
WHITE =     (255, 255, 255)
BLACK =     (0, 0, 0)
DARKRED =   (115, 20, 13)
BLUE =      (0, 0, 255)
YELLOW =    (249, 215, 28)
DARKBLUE =  (71, 95, 119)
DEEPBLUE =  (53, 75, 94)
BRIGHTRED = (215, 75, 75)

FONT_SIZE = 30

# Input the png image to the program
CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (90, 90))
REDMEN = pygame.transform.scale(pygame.image.load('assets/redMen.png'), (90, 90))
WHITEMEN = pygame.transform.scale(pygame.image.load('assets/whiteMen.png'), (90, 90))