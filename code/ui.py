import random
import pygame

from config import WIDTH, HEIGHT, TITLE, FPS, WHITE, BLACK, RED, GREEN, BLUE, YELLOW, DARK_OVERLAY
from music import get_sound_manager

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
