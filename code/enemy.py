import math
import random
import pygame
from config import (
    WIDTH,
    ENEMY_MIN_SPEED,
    ENEMY_MAX_SPEED,
    ELITE_ENEMY_WIDTH,
    ELITE_ENEMY_HEIGHT,
    ELITE_ENEMY_SPEED,
    ELITE_HEALTH,
    ELITE_SCORE,
    NORMAL_ENEMY_SHOOT_DELAY_MS,
    ELITE_ENEMY_SHOOT_DELAY_MS,
    ELITE_BULLET_SPEED,
    resource_path,
)
from bullet import EnemyBullet, EliteBullet
from music import get_sound_manager

NORMAL_ENEMY_BULLET_SPEED = max(3.5, ELITE_BULLET_SPEED - 1.2)


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

        self.image = pygame.image.load(
            resource_path("assets/image/enemy.png")
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        # 加入隨機偏移，避免全部敵機同時齊射
        self.last_shot_time = pygame.time.get_ticks() - random.randint(
            0, NORMAL_ENEMY_SHOOT_DELAY_MS
        )

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

    def shoot(self, now_ms):
        """
        普通敵機：3-way 小扇形彈幕
        """
        if now_ms - self.last_shot_time < NORMAL_ENEMY_SHOOT_DELAY_MS:
            return []

        self.last_shot_time = now_ms
        origin_x = self.rect.centerx - 4
        origin_y = self.rect.bottom - 2

        angles = (-16, 0, 16)
        bullets = []
        for angle in angles:
            rad = math.radians(angle)
            vx = math.sin(rad) * NORMAL_ENEMY_BULLET_SPEED
            vy = math.cos(rad) * NORMAL_ENEMY_BULLET_SPEED
            bullets.append(EnemyBullet(origin_x, origin_y, vx=vx, vy=vy))

        # 每次發射彈幕播放一次敵方子彈音效
        get_sound_manager().play("enemyshoot")
        return bullets


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

        self.image = pygame.image.load(
            resource_path("assets/image/Elite-enemy.png")
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.last_shot_time = pygame.time.get_ticks() - random.randint(
            0, ELITE_ENEMY_SHOOT_DELAY_MS
        )

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
        """
        精英敵機：7-way 更密集扇形彈幕
        """
        if now_ms - self.last_shot_time < ELITE_ENEMY_SHOOT_DELAY_MS:
            return []

        self.last_shot_time = now_ms
        origin_x = self.rect.centerx - 5
        origin_y = self.rect.bottom - 2
        speed = ELITE_BULLET_SPEED + 1.0

        angles = (-42, -28, -14, 0, 14, 28, 42)
        bullets = []
        for angle in angles:
            rad = math.radians(angle)
            vx = math.sin(rad) * speed
            vy = math.cos(rad) * speed
            bullets.append(EliteBullet(origin_x, origin_y, vx=vx, vy=vy))

        # 每次發射彈幕播放一次敵方子彈音效
        get_sound_manager().play("enemyshoot")
        return bullets