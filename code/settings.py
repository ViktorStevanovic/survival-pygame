import pygame 
from os.path import join, dirname, abspath 
from os import walk

WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720 
TILE_SIZE = 64
PLAYER_SPEED = 600
FPS = 120
BG_COLOR = "#FFE8E8"
BASE_DIR = dirname(dirname(abspath(__file__)))