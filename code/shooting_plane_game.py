import math
import random
import sys
from pathlib import Path

import pygame


# =========================
# Shooting Plane Game
# Controls:
#   A / D   -> move left / right
#   SPACE   -> shoot
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
        # Body
        body_points = [
            (self.rect.centerx, self.rect.top),
            (self.rect.left + 10, self.rect.bottom - 8),
            (self.rect.centerx, self.rect.bottom - 18),
            (self.rect.right - 10, self.rect.bottom - 8),
        ]
        pygame.draw.polygon(screen, BLUE, body_points)
        # Cockpit
        pygame.draw.circle(screen, WHITE, (self.rect.centerx, self.rect.top + 18), 6)
        # Wings
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
        # Enemy plane body
        body = [
            (self.rect.centerx, self.rect.bottom),
            (self.rect.left + 8, self.rect.top + 12),
            (self.rect.centerx, self.rect.top),
            (self.rect.right - 8, self.rect.top + 12),
        ]
        pygame.draw.polygon(screen, RED, body)
        # Wings
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
        # Window
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
        # Draw button background
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, self.text_color, self.rect, 2)  # Border
        
        # Draw button text
        draw_text(screen, self.text, 36, self.text_color, self.rect.centerx, self.rect.centery, center=True)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:    #mouse overlap button 
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered and event.button == 1: #hovered and clicked
                return True
        return False
        

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
    
        # Create buttons
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
        
        # Background gradient colors
        self.bg_color1 = (20, 20, 40) #grey
        self.bg_color2 = (40, 40, 60) #light grey
        
    def draw_background(self):
        # Create gradient background
        for i in range(HEIGHT):
            color = (
                self.bg_color1[0] + (self.bg_color2[0] - self.bg_color1[0]) * i // HEIGHT,
                self.bg_color1[1] + (self.bg_color2[1] - self.bg_color1[1]) * i // HEIGHT,
                self.bg_color1[2] + (self.bg_color2[2] - self.bg_color1[2]) * i // HEIGHT
            )
            pygame.draw.line(self.screen, color, (0, i), (WIDTH, i))
    
    def draw_title(self):
        # Draw title
        draw_text(self.screen, TITLE, 68, WHITE, WIDTH//2, HEIGHT//4, center=True)
        
    
    def run(self):
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                # Check button clicks
                if self.start_button.handle_event(event):
                    return "start"
                if self.quit_button.handle_event(event):
                    return "quit"
            
            # Draw everything
            self.draw_background()
            self.draw_title()
            self.start_button.draw(self.screen)
            self.quit_button.draw(self.screen)
            
            # Update display
            pygame.display.flip()
            self.clock.tick(60)
        
        return "quit"
    
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
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    menu = MainMenu(screen)
    state = reset_game()
    running = True

    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r and state["current_state"]== "game_over":
                    state = reset_game()
                if event.key == pygame.K_SPACE and state["current_state"] == "game":
                    if state["player"].can_shoot():
                        state["bullets"].append(state["player"].shoot())

        # Menu
        if state["current_state"] == "menu":
            result = menu.run()
            if result == "start":
                state["current_state"] = "game"
            elif result == "quit":
                running = False
                break

        # Game
        if state["current_state"] == "game":
            keys = pygame.key.get_pressed()
            state["player"].move(keys)
            update_stars(state["stars"])

            # Bullets update
            for bullet in state["bullets"][:]:
                bullet.update()
                if bullet.rect.bottom < 0:
                    state["bullets"].remove(bullet)

            # Enemy spawn
            state["spawn_timer"] += dt
            if state["spawn_timer"] >= ENEMY_SPAWN_MS and len(state["enemies"]) < MAX_ENEMIES:
                state["spawn_timer"] = 0
                state["enemies"].append(Enemy())

            # Enemies update
            for enemy in state["enemies"][:]:
                enemy.update()
                if enemy.rect.top > HEIGHT:
                    state["enemies"].remove(enemy)

            # Bullet-enemy collisions
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

            # Player-enemy collision => game over
            for enemy in state["enemies"]:
                if state["player"].rect.colliderect(enemy.rect):
                    state["current_state"] = "game_over"
                    break

        # Draw
        draw_background(screen, state["stars"])

        for star in state["stars"]:
            pygame.draw.circle(screen, WHITE, (int(star[0]), int(star[1])), star[2])

        for bullet in state["bullets"]:
            bullet.draw(screen)
        for enemy in state["enemies"]:
            enemy.draw(screen)
        state["player"].draw(screen)

        # UI
        draw_text(screen, TITLE, 28, WHITE, WIDTH // 2, 28)
        draw_text(screen, f"Score: {state['score']}", 24, WHITE, 12, 12, center=False)
        draw_text(screen, "W A S D Move   SPACE Shoot", 18, WHITE, WIDTH // 2, HEIGHT - 28)

        if state["current_state"] == "game_over":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))
            draw_text(screen, "GAME OVER", 56, RED, WIDTH // 2, HEIGHT // 2 - 40)
            draw_text(screen, f"Final Score: {state['score']}", 30, WHITE, WIDTH // 2, HEIGHT // 2 + 10)
            draw_text(screen, "Press R to Restart", 24, YELLOW, WIDTH // 2, HEIGHT // 2 + 50)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
