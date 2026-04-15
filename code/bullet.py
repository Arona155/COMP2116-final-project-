import pygame
from config import BULLET_SPEED, ELITE_BULLET_SPEED, YELLOW, RED


class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 6, 12)
        self.speed = BULLET_SPEED

    def update(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, self.rect)


class EnemyBullet:
    """
    通用敵方彈幕：
    - 支援 vx / vy，方便做扇形彈幕
    - grazed 用來避免同一顆子彈被重複計算 Graze
    """
    def __init__(self, x, y, vx=0.0, vy=None, width=8, height=12, color=RED):
        if vy is None:
            vy = ELITE_BULLET_SPEED

        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.color = color
        self.grazed = False
        self.rect = pygame.Rect(int(self.x), int(self.y), width, height)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class EliteBullet(EnemyBullet):
    """
    精英彈幕：尺寸更大、速度稍快
    """
    def __init__(self, x, y, vx=0.0, vy=None):
        if vy is None:
            vy = ELITE_BULLET_SPEED + 1.0
        super().__init__(x, y, vx=vx, vy=vy, width=10, height=14, color=RED)