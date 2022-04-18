# Game Settings
import random
import os
import pygame as pg

#set directories
game_Folder = os.path.dirname(__file__)
assets_Folder = os.path.join(game_Folder, "assets")
img_Folder = os.path.join(assets_Folder, "imgs")
audio_Folder = os.path.join(assets_Folder, "audio")

print(img_Folder)

#High score file
HS_FILE = "highscore.txt"

#Spritesheet file
SPRITESHEET = "spritesheet_jumper.png"


# game title
TITLE = "Runner" #Sets title
FONT_NAME = 'arial'

# screen size
WIDTH = 1024 # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768 # 16 * 48 or 32 * 24 or 64 * 12


#tile properties
TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = "tile_12.png"
MOB_IMG = "zoimbie1_hold.png"

# Player Size
PLAYER_HEIGHT = 32
PLAYER_WIDTH = 32

#player properties
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250
PLAYER_IMG = 'manBlue_gun.png'
PLAYER_HIT_RECT = pg.Rect(0,0,35,35)

# Mob Properties
MOB_SPEED = 150
MOB_HIT_RECT = pg.Rect(0,0,30,30)


# clock speed
FPS = 60 #sets frames per second (clock tick)

# difficulty
diff = "Normal" #sets difficulty


# Colors (R,G,B)
BLACK = (0, 0, 0)
GRAY = (50,50,50)
LIGHTGRAY = (100,100,100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255 ,0)
BLUE = (0, 0 ,255)
YELLOW = (255, 255, 0)
skyBlue = (135,206,235)
darkBlue = (86, 105, 184)
cfBlue = (100, 149, 237)
BROWN = (106, 55, 5)