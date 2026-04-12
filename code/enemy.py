import random
import pygame

from config import (
    WIDTH,
    HEIGHT,
    ENEMY_MIN_SPEED,
    ENEMY_MAX_SPEED,
    ELITE_ENEMY_WIDTH,
    ELITE_ENEMY_HEIGHT,
    ELITE_ENEMY_SPEED,
    ELITE_HEALTH,
    ELITE_SCORE,
    ELITE_ENEMY_SHOOT_DELAY_MS,
    resource_path,
)
from bullet import EliteBullet

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
        self.image = pygame.image.load(resource_path("assets/image/enemy.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

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
        screen.blit(self.image, self.rect)

class EliteEnemy:
    def __init__(self):
        self.width = ELITE_ENEMY_WIDTH
        self.height = ELITE_ENEMY_HEIGHT
        self.rect = pygame.Rect(
            random.randint(0, WIDTH - self.width),
            random.randint(-150, -40),
            self.width,
            self.height,
        )
        self.speed = ELITE_ENEMY_SPEED + random.uniform(-0.5, 0.5) 
        self.x_drift = random.choice([-1, 0, 1]) * random.uniform(0.3, 1.3)
        self.health = ELITE_HEALTH
        self.score_value = ELITE_SCORE
        self.image = pygame.image.load(resource_path("assets/image/Elite-enemy.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.last_shot_time = pygame.time.get_ticks()

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
        screen.blit(self.image, self.rect)

    def take_damage(self):
        self.health -= 1
        return self.health <= 0

    def shoot(self, now_ms):
        if now_ms - self.last_shot_time >= ELITE_ENEMY_SHOOT_DELAY_MS:
            self.last_shot_time = now_ms
            bullet_x = self.rect.centerx - 4
            bullet_y = self.rect.bottom
            return EliteBullet(bullet_x, bullet_y)
        return None
