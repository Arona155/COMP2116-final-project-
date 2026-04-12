from player import Player
from ui import create_stars

def get_elite_spawn_probability(score):
    if score < 100:
        return 0.0
    extra = (score - 100) // 200 * 0.1
    return min(0.6, 0.1 + extra)

def reset_game():
    return {
        "player": Player(),
        "bullets": [],
        "enemies": [],
        "elite_bullets": [], 
        "score": 0,
        "current_state": "menu",
        "spawn_timer": 0,
        "stars": create_stars(),
    }
