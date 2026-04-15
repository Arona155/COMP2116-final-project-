import pygame
from config import (
    WIDTH,
    HEIGHT,
    PLAYER_SPEED,
    PLAYER_FOCUS_SPEED,
    PLAYER_SHOOT_COOLDOWN_FRAMES,
    PLAYER_HITBOX_RADIUS,
    PLAYER_GRAZE_RADIUS,
    WHITE,
    RED,
    resource_path,
)
from bullet import Bullet
from music import get_sound_manager


class Player:
    def __init__(self):
        self.width = 44
        self.height = 50
        self.rect = pygame.Rect(
            WIDTH // 2 - self.width // 2,
            HEIGHT - 80,
            self.width,
            self.height,
        )

        self.cooldown = 0
        self.focused = False
        self.hitbox_radius = PLAYER_HITBOX_RADIUS
        self.graze_radius = PLAYER_GRAZE_RADIUS

        self.image = pygame.image.load(
            resource_path("assets/image/player.png")
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    @property
    def hitbox_center(self):
        return self.rect.centerx, self.rect.centery

    def move(self, input_state):
        """
        只吃 main.py 傳進來的 input_state
        避免整個專案出現兩套輸入邏輯。
        """
        self.focused = bool(input_state.get("focus", False))
        speed = PLAYER_FOCUS_SPEED if self.focused else PLAYER_SPEED

        dx = 0
        dy = 0

        if input_state.get("left", False):
            dx -= speed
        if input_state.get("right", False):
            dx += speed
        if input_state.get("up", False):
            dy -= speed
        if input_state.get("down", False):
            dy += speed

        self.rect.x += dx
        self.rect.y += dy

        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y))

        if self.cooldown > 0:
            self.cooldown -= 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def draw_hitbox(self, screen):
        px, py = self.hitbox_center
        if self.focused:
            pygame.draw.circle(screen, WHITE, (px, py), self.graze_radius, 1)
            pygame.draw.circle(screen, WHITE, (px, py), self.hitbox_radius, 1)
            pygame.draw.circle(screen, RED, (px, py), 2)

    def can_shoot(self):
        return self.cooldown == 0

    def shoot(self):
        self.cooldown = PLAYER_SHOOT_COOLDOWN_FRAMES
        get_sound_manager().play("shoot")
        return Bullet(self.rect.centerx - 3, self.rect.top - 12)

    @staticmethod
    def _distance_sq_point_to_rect(px, py, rect):
        nearest_x = max(rect.left, min(px, rect.right))
        nearest_y = max(rect.top, min(py, rect.bottom))
        dx = px - nearest_x
        dy = py - nearest_y
        return dx * dx + dy * dy

    def bullet_hits(self, bullet_rect):
        px, py = self.hitbox_center
        d2 = self._distance_sq_point_to_rect(px, py, bullet_rect)
        return d2 <= self.hitbox_radius * self.hitbox_radius

    def bullet_grazes(self, bullet_rect):
        px, py = self.hitbox_center
        d2 = self._distance_sq_point_to_rect(px, py, bullet_rect)
        return (
            d2 <= self.graze_radius * self.graze_radius
            and d2 > self.hitbox_radius * self.hitbox_radius
        )