import math
import random
import sys
from pathlib import Path

import pygame

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller 暫存資料夾
    except Exception:
        base_path = Path(__file__).parent
    return Path(base_path) / relative_path


# =========================
# Shooting Plane Game
# Controls:
#   A / D   -> move left / right
#   W / S   -> move up / down
#   SPACE   -> shoot
#   ESC     -> pause menu
#   R       -> restart after game over
# =========================

WIDTH, HEIGHT = 800, 600
FPS = 60
TITLE = "Shooting Plane Game"

PLAYER_SPEED = 6
BULLET_SPEED = 10
ENEMY_MIN_SPEED = 2
ENEMY_MAX_SPEED = 5
ENEMY_SPAWN_MS = 900
MAX_ENEMIES = 12

ELITE_ENEMY_WIDTH = 50
ELITE_ENEMY_HEIGHT = 60
ELITE_ENEMY_SPEED = 4
ELITE_ENEMY_SHOOT_DELAY_MS = 1500 
ELITE_BULLET_SPEED = 8
ELITE_SCORE = 50 
ELITE_HEALTH = 3 

WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
RED = (220, 60, 60)
YELLOW = (245, 210, 70)
BLUE = (80, 160, 255)
GREEN = (90, 220, 120)
DARK_OVERLAY = (0, 0, 0, 160)

