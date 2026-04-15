import sys
from pathlib import Path
import pygame


def resource_path(relative_path: str) -> Path:
    """
    兼容開發環境與 PyInstaller 打包後的資源路徑。
    """
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent
    return base_path / relative_path


# =========================
# Game Window
# =========================
WIDTH, HEIGHT = 800, 600
FPS = 60
TITLE = "Shooting Plane Game"


# =========================
# Player
# =========================
PLAYER_SPEED = 6
PLAYER_FOCUS_SPEED = 3

# 原本 10，現在稍微放慢
PLAYER_SHOOT_COOLDOWN_FRAMES = 14

PLAYER_MAX_HEALTH = 3
PLAYER_HITBOX_RADIUS = 4
PLAYER_GRAZE_RADIUS = 22
PLAYER_HIT_INVULN_MS = 1200

# 中彈後透明閃爍的切換節奏
PLAYER_HIT_FLASH_INTERVAL_MS = 120

# ===== Focus 鍵設定（重點修正）=====
# 不再用 Shift / Ctrl 當預設，避免鍵盤 ghosting / rollover 問題
PLAYER_FOCUS_KEY = pygame.K_c
PLAYER_FOCUS_KEY_NAME = "C"

# 滑鼠右鍵也可以當 Focus
PLAYER_FOCUS_MOUSE_BUTTON_INDEX = 2  # 左0 中1 右2


# =========================
# Bullets
# =========================
BULLET_SPEED = 10
ELITE_BULLET_SPEED = 6


# =========================
# Enemies
# =========================
ENEMY_MIN_SPEED = 2
ENEMY_MAX_SPEED = 3
ENEMY_SPAWN_MS = 900
MAX_ENEMIES = 9

# 普通敵機開火間隔
NORMAL_ENEMY_SHOOT_DELAY_MS = 2200

ELITE_ENEMY_WIDTH = 50
ELITE_ENEMY_HEIGHT = 60
ELITE_ENEMY_SPEED = 4

# 精英敵機開火間隔
ELITE_ENEMY_SHOOT_DELAY_MS = 2600

ELITE_SCORE = 50
ELITE_HEALTH = 3


# =========================
# Colors
# =========================
WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
RED = (220, 60, 60)
YELLOW = (245, 210, 70)
BLUE = (80, 160, 255)
GREEN = (90, 220, 120)
DARK_OVERLAY = (0, 0, 0, 160)