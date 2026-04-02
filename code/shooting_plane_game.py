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

WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
RED = (220, 60, 60)
YELLOW = (245, 210, 70)
BLUE = (80, 160, 255)
GREEN = (90, 220, 120)
DARK_OVERLAY = (0, 0, 0, 160)

_sound_manager = None


class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_playing = False
        self.load_all_sounds()

    def load_all_sounds(self):
        try:
            sound_path = resource_path("assets/laser.wav") #

            self.sounds["shoot"] = pygame.mixer.Sound(str(sound_path))
            self.sounds["shoot"].set_volume(0.03)

            sound_path = resource_path("assets/bgm.mp3")

            self.sounds["bgm"] = pygame.mixer.Sound(str(sound_path))
            self.sounds["bgm"].set_volume(0.1)

            return True

        except (pygame.error, FileNotFoundError) as e:
            print(f"Sound load failed: {e}")
            print("Game will run without sound")
            return False

    def play(self, sound_name, times = 0):
        if sound_name in self.sounds and self.sounds[sound_name]:
            self.sounds[sound_name].play(times)
            return True
        return False

def get_sound_manager():
    global _sound_manager
    if _sound_manager is None:
        _sound_manager = SoundManager()
    return _sound_manager


class Player:
    def __init__(self):
        self.width = 44
        self.height = 50
        self.rect = pygame.Rect(WIDTH // 2 - self.width // 2, HEIGHT - 80, self.width, self.height)
        self.cooldown = 0

    def move(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_w]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_s]:
            self.rect.y += PLAYER_SPEED

        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y))

        if self.cooldown > 0:
            self.cooldown -= 1

    def draw(self, screen):
        body_points = [
            (self.rect.centerx, self.rect.top),
            (self.rect.left + 10, self.rect.bottom - 8),
            (self.rect.centerx, self.rect.bottom - 18),
            (self.rect.right - 10, self.rect.bottom - 8),
        ]
        pygame.draw.polygon(screen, BLUE, body_points)
        pygame.draw.circle(screen, WHITE, (self.rect.centerx, self.rect.top + 18), 6)
        pygame.draw.polygon(
            screen,
            GREEN,
            [
                (self.rect.left + 4, self.rect.centery + 4),
                (self.rect.centerx, self.rect.centery - 4),
                (self.rect.right - 4, self.rect.centery + 4),
                (self.rect.centerx, self.rect.centery + 10),
            ],
        )

    def can_shoot(self):
        return self.cooldown == 0

    def shoot(self):
        get_sound_manager().play("shoot")
        self.cooldown = 12
        return Bullet(self.rect.centerx - 3, self.rect.top - 10)


class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 6, 12)

    def update(self):
        self.rect.y -= BULLET_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, self.rect, border_radius=3)


class Enemy:
    def __init__(self):
        self.width = random.randint(34, 52)
        self.height = random.randint(34, 54)
        self.rect = pygame.Rect(
            random.randint(0, WIDTH - self.width),
            random.randint(-150, -40),
            self.width,
            self.height,
        )
        self.speed = random.randint(ENEMY_MIN_SPEED, ENEMY_MAX_SPEED)
        self.x_drift = random.choice([-1, 0, 1]) * random.uniform(0.2, 1.1)
        self.score_value = 10 if self.width < 44 else 20

    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.x_drift

        if self.rect.left < 0:
            self.rect.left = 0
            self.x_drift *= -1
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.x_drift *= -1

    def draw(self, screen):
        body = [
            (self.rect.centerx, self.rect.bottom),
            (self.rect.left + 8, self.rect.top + 12),
            (self.rect.centerx, self.rect.top),
            (self.rect.right - 8, self.rect.top + 12),
        ]
        pygame.draw.polygon(screen, RED, body)
        pygame.draw.polygon(
            screen,
            WHITE,
            [
                (self.rect.left, self.rect.centery),
                (self.rect.centerx - 8, self.rect.centery + 8),
                (self.rect.right, self.rect.centery),
                (self.rect.centerx + 8, self.rect.centery - 2),
            ],
        )
        pygame.draw.circle(screen, BLACK, (self.rect.centerx, self.rect.top + 12), 4)


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, self.text_color, self.rect, 2, border_radius=10)
        draw_text(screen, self.text, 32, self.text_color, self.rect.centerx, self.rect.centery, center=True)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        button_width = 250
        button_height = 60
        button_x = WIDTH // 2 - button_width // 2

        self.start_button = Button(
            button_x, HEIGHT // 2 - 40,
            button_width, button_height,
            "Start Game", GREEN, BLACK, WHITE
        )

        self.quit_button = Button(
            button_x, HEIGHT // 2 + 40,
            button_width, button_height,
            "Quit", (255, 100, 100), BLACK, WHITE
        )

        self.bg_color1 = (20, 20, 40)
        self.bg_color2 = (40, 40, 60)

    def draw_background(self):
        for i in range(HEIGHT):
            color = (
                self.bg_color1[0] + (self.bg_color2[0] - self.bg_color1[0]) * i // HEIGHT,
                self.bg_color1[1] + (self.bg_color2[1] - self.bg_color1[1]) * i // HEIGHT,
                self.bg_color1[2] + (self.bg_color2[2] - self.bg_color1[2]) * i // HEIGHT,
            )
            pygame.draw.line(self.screen, color, (0, i), (WIDTH, i))

    def draw_title(self):
        draw_text(self.screen, TITLE, 68, WHITE, WIDTH // 2, HEIGHT // 4, center=True)

    def run(self):
        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if self.start_button.handle_event(event):
                    return "start"
                if self.quit_button.handle_event(event):
                    return "quit"

            self.draw_background()
            self.draw_title()
            self.start_button.draw(self.screen)
            self.quit_button.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        return "quit"


class OverlayMenu:
    def __init__(self, screen, title, subtitle=None):
        self.screen = screen
        self.title = title
        self.subtitle = subtitle

        button_width = 250
        button_height = 60
        button_x = WIDTH // 2 - button_width // 2
        button_gap = 18
        start_y = HEIGHT // 2 - button_height - button_gap

        self.restart_button = Button(
            button_x, start_y,
            button_width, button_height,
            "Restart", GREEN, BLACK, WHITE
        )
        self.home_button = Button(
            button_x, start_y + button_height + button_gap,
            button_width, button_height,
            "Home", BLUE, BLACK, WHITE
        )
        self.quit_button = Button(
            button_x, start_y + (button_height + button_gap) * 2,
            button_width, button_height,
            "Quit", (255, 100, 100), BLACK, WHITE
        )

    def draw(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill(DARK_OVERLAY)
        self.screen.blit(overlay, (0, 0))

        draw_text(self.screen, self.title, 56, WHITE, WIDTH // 2, HEIGHT // 2 - 140)
        if self.subtitle:
            draw_text(self.screen, self.subtitle, 24, YELLOW, WIDTH // 2, HEIGHT // 2 - 97)

        self.restart_button.draw(self.screen)
        self.home_button.draw(self.screen)
        self.quit_button.draw(self.screen)

    def handle_event(self, event):
        if self.restart_button.handle_event(event):
            return "restart"
        if self.home_button.handle_event(event):
            return "home"
        if self.quit_button.handle_event(event):
            return "quit"
        return None


def draw_background(screen, stars):
    screen.fill(BLACK)
    for star in stars:
        x, y, r, speed = star
        pygame.draw.circle(screen, WHITE, (int(x), int(y)), r)


def create_stars():
    stars = []
    for _ in range(80):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        r = random.randint(1, 2)
        speed = random.uniform(0.4, 1.8)
        stars.append([x, y, r, speed])
    return stars


def update_stars(stars):
    for s in stars:
        s[1] += s[3]
        if s[1] > HEIGHT:
            s[0] = random.randint(0, WIDTH)
            s[1] = random.randint(-20, -5)
            s[2] = random.randint(1, 2)
            s[3] = random.uniform(0.4, 1.8)


def draw_text(screen, text, size, color, x, y, center=True):
    font = pygame.font.SysFont("arial", size, bold=True)
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)


def reset_game():
    return {
        "player": Player(),
        "bullets": [],
        "enemies": [],
        "score": 0,
        "current_state": "menu",
        "spawn_timer": 0,
        "stars": create_stars(),
    }


def main():
    pygame.init()
    try:
        pygame.mixer.init()
    except pygame.error:
        pass

    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    get_sound_manager().play("bgm",-1) #loop bgm
    # _ = sound  # keep for future use

    menu = MainMenu(screen)
    state = reset_game()
    pause_menu = OverlayMenu(
        screen,
        "PAUSED",
        "Press ESC to resume"
    )

    game_over_menu = OverlayMenu(
        screen,
        "GAME OVER",
        "Final Score: 0 " # placeholder
    )
    running = True
    

    while running:
        dt = clock.tick(FPS)

        if state["current_state"] == "menu":
            result = menu.run()
            if result == "start":
                state = reset_game()
                state["current_state"] = "game"
                continue
            if result == "quit":
                running = False
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            
            if state["current_state"] == "game":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state["current_state"] = "pause"
                    elif event.key == pygame.K_SPACE:
                        if state["player"].can_shoot():
                            state["bullets"].append(state["player"].shoot())

            elif state["current_state"] == "pause":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state["current_state"] = "game"
                action = pause_menu.handle_event(event)
                if action == "restart":
                    state = reset_game()
                    state["current_state"] = "game"
                elif action == "home":
                    state = reset_game()
                elif action == "quit":
                    running = False
                    break

            elif state["current_state"] == "game_over":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    state = reset_game()
                    state["current_state"] = "game"
                action = game_over_menu.handle_event(event)
                if action == "restart":
                    state = reset_game()
                    state["current_state"] = "game"
                elif action == "home":
                    state = reset_game()
                elif action == "quit":
                    running = False
                    break

        if not running:
            break

        if state["current_state"] == "game":
            keys = pygame.key.get_pressed()
            state["player"].move(keys)
            update_stars(state["stars"])

            for bullet in state["bullets"][:]:
                bullet.update()
                if bullet.rect.bottom < 0:
                    state["bullets"].remove(bullet)

            state["spawn_timer"] += dt
            if state["spawn_timer"] >= ENEMY_SPAWN_MS and len(state["enemies"]) < MAX_ENEMIES:
                state["spawn_timer"] = 0
                state["enemies"].append(Enemy())

            for enemy in state["enemies"][:]:
                enemy.update()
                if enemy.rect.top > HEIGHT:
                    state["enemies"].remove(enemy)

            for bullet in state["bullets"][:]:
                hit_enemy = None
                for enemy in state["enemies"]:
                    if bullet.rect.colliderect(enemy.rect):
                        hit_enemy = enemy
                        break
                if hit_enemy:
                    state["score"] += hit_enemy.score_value
                    if bullet in state["bullets"]:
                        state["bullets"].remove(bullet)
                    if hit_enemy in state["enemies"]:
                        state["enemies"].remove(hit_enemy)

            for enemy in state["enemies"]:
                if state["player"].rect.colliderect(enemy.rect):
                    state["current_state"] = "game_over"
                    game_over_menu = OverlayMenu(
                        screen,
                        "GAME OVER",
                        f"Final Score: {state['score']}"
                    )
                    break

        draw_background(screen, state["stars"])

        for star in state["stars"]:
            pygame.draw.circle(screen, WHITE, (int(star[0]), int(star[1])), star[2])

        for bullet in state["bullets"]:
            bullet.draw(screen)
        for enemy in state["enemies"]:
            enemy.draw(screen)
        state["player"].draw(screen)

        draw_text(screen, TITLE, 28, WHITE, WIDTH // 2, 28)
        draw_text(screen, f"Score: {state['score']}", 24, WHITE, 12, 12, center=False)

        if state["current_state"] == "game":
            draw_text(screen, "W A S D Move   SPACE Shoot   ESC Pause", 18, WHITE, WIDTH // 2, HEIGHT - 28)
        elif state["current_state"] == "pause":
            draw_text(screen, "Game paused", 18, WHITE, WIDTH // 2, HEIGHT - 28)
            pause_menu.draw()
        elif state["current_state"] == "game_over":
            draw_text(screen, "Use Restart / Home / Quit", 18, WHITE, WIDTH // 2, HEIGHT - 28)
            game_over_menu.draw()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
