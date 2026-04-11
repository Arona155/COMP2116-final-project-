import pygame

from config import WIDTH, HEIGHT, PLAYER_SPEED, resource_path
from bullet import Bullet
from music import get_sound_manager


class Player:
    def __init__(self):
        self.width = 44
        self.height = 50
        self.rect = pygame.Rect(WIDTH // 2 - self.width // 2, HEIGHT - 80, self.width, self.height)
        self.cooldown = 0
        self.image = pygame.image.load(resource_path("assets/image/player.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

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
        screen.blit(self.image, self.rect)

    def can_shoot(self):
        return self.cooldown == 0

    def shoot(self):
        self.cooldown = 10
        get_sound_manager().play("shoot")
        return Bullet(self.rect.centerx - 3, self.rect.top - 12)