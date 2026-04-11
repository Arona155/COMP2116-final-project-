import pygame

from config import BULLET_SPEED, ELITE_BULLET_SPEED, YELLOW, RED

class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 6, 12)

    def update(self):
        self.rect.y -= BULLET_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, self.rect, border_radius=3)

class EliteBullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 8, 12)

    def update(self):
        self.rect.y += ELITE_BULLET_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect, border_radius=3)
