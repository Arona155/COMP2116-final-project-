from player import Player
from ui import create_stars
from config import PLAYER_MAX_HEALTH


def get_elite_spawn_probability(score):
    if score < 100:
        return 0.0
    extra = (score - 100) // 200 * 0.1
    return min(0.6, 0.1 + extra)


def reset_game():
    """
    初始化遊戲狀態。
    保留 elite_bullets 以相容目前 main.py，
    同時提供 enemy_bullets 作為更清楚的別名。
    """
    enemy_bullet_list = []
    return {
        "player": Player(),
        "bullets": [],
        "enemies": [],
        "elite_bullets": enemy_bullet_list,
        "enemy_bullets": enemy_bullet_list,
        "score": 0,
        "graze": 0,
        "player_health": PLAYER_MAX_HEALTH,
        "invulnerable_until": 0,
        "current_state": "menu",
        "spawn_timer": 0,
        "stars": create_stars(),
    }