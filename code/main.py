import math
import random
import sys
import ctypes
from pathlib import Path

import pygame

from config import *
from music import get_sound_manager
from player import Player
from bullet import Bullet, EliteBullet
from enemy import Enemy, EliteEnemy
from ui import (
    Button,
    MainMenu,
    OverlayMenu,
    draw_background,
    create_stars,
    update_stars,
    draw_text,
)
from shooting import get_elite_spawn_probability, reset_game


def resource_path(relative_path: str) -> Path:
    """
    兼容開發環境與 PyInstaller 打包後的資源路徑。
    """
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_dir = Path(sys._MEIPASS)
    else:
        base_dir = Path(__file__).resolve().parent
    return base_dir / relative_path


def set_windows_appusermodel_id(app_id: str) -> None:
    """
    設定 Windows AppUserModelID，讓工作列更穩定識別本應用程式。
    必須在顯示任何 UI 前呼叫。
    """
    if sys.platform == "win32":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)


def set_windows_taskbar_icon_from_ico(hwnd: int, ico_path: Path) -> None:
    """
    使用 Win32 API 將 icon.ico 設定到視窗的大 / 小圖示。
    這會影響標題列 / Alt+Tab / 工作列顯示（較穩定）。
    """
    if sys.platform != "win32" or not hwnd or not ico_path.exists():
        return

    user32 = ctypes.windll.user32

    WM_SETICON = 0x0080
    ICON_SMALL = 0
    ICON_BIG = 1
    IMAGE_ICON = 1
    LR_LOADFROMFILE = 0x0010
    LR_DEFAULTSIZE = 0x0040

    hicon = user32.LoadImageW(
        None,
        str(ico_path),
        IMAGE_ICON,
        0,
        0,
        LR_LOADFROMFILE | LR_DEFAULTSIZE,
    )

    if hicon:
        user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon)
        user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon)


def main():
    pygame.init()

    # Windows 工作列應用程式識別（要在任何 UI 出現前）
    set_windows_appusermodel_id("LAMCHONHIN.ShootingPlaneGame")

    try:
        pygame.mixer.init()
    except pygame.error:
        pass

    # Pygame 視窗圖示（PNG）
    png_icon_path = resource_path("assets/image/icon.png")
    if png_icon_path.exists():
        icon_surface = pygame.image.load(str(png_icon_path))
        pygame.display.set_icon(icon_surface)

    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Windows 工作列 / Alt+Tab / 視窗標題列圖示（ICO）
    ico_icon_path = resource_path("icon.ico")
    if sys.platform == "win32":
        wm_info = pygame.display.get_wm_info()
        hwnd = wm_info.get("window")
        set_windows_taskbar_icon_from_ico(hwnd, ico_icon_path)

    clock = pygame.time.Clock()
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
        "Final Score: 0 "  # placeholder
    )

    running = True

    while running:
        dt = clock.tick(FPS)

        if state["current_state"] == "menu":
            get_sound_manager().play_menu_music(restart=True)
            result = menu.run()

            if result == "start":
                state = reset_game()
                state["current_state"] = "game"
                get_sound_manager().play_ingame_music(restart=True)
                continue

            if result == "quit":
                get_sound_manager().stop_music()
                running = False
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if state["current_state"] == "game":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        get_sound_manager().stop_music()
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
                    get_sound_manager().stop_all_sounds()
                    state = reset_game()
                    state["current_state"] = "game"
                    get_sound_manager().play_ingame_music(restart=True)

                action = game_over_menu.handle_event(event)
                if action == "restart":
                    get_sound_manager().stop_all_sounds()
                    state = reset_game()
                    state["current_state"] = "game"
                    get_sound_manager().play_ingame_music(restart=True)
                elif action == "home":
                    get_sound_manager().stop_all_sounds()
                    get_sound_manager().stop_music()
                    state = reset_game()
                elif action == "quit":
                    get_sound_manager().stop_all_sounds()
                    get_sound_manager().stop_music()
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

            for eb in state["elite_bullets"][:]:
                eb.update()
                if eb.rect.top > HEIGHT:
                    state["elite_bullets"].remove(eb)

            state["spawn_timer"] += dt
            if state["spawn_timer"] >= ENEMY_SPAWN_MS and len(state["enemies"]) < MAX_ENEMIES:
                state["spawn_timer"] = 0
                score = state["score"]
                elite_prob = get_elite_spawn_probability(score)
                if random.random() < elite_prob:
                    state["enemies"].append(EliteEnemy())
                else:
                    state["enemies"].append(Enemy())

            now_ms = pygame.time.get_ticks()
            for enemy in state["enemies"][:]:
                enemy.update()
                if isinstance(enemy, EliteEnemy):
                    eb = enemy.shoot(now_ms)
                    if eb:
                        state["elite_bullets"].append(eb)
                if enemy.rect.top > HEIGHT:
                    state["enemies"].remove(enemy)

            for bullet in state["bullets"][:]:
                hit_enemy = None
                for enemy in state["enemies"]:
                    if bullet.rect.colliderect(enemy.rect):
                        hit_enemy = enemy
                        break

                if hit_enemy:
                    if isinstance(hit_enemy, EliteEnemy):
                        if hit_enemy.take_damage():
                            state["score"] += hit_enemy.score_value
                            state["enemies"].remove(hit_enemy)
                            get_sound_manager().play("enemyboom")
                        if bullet in state["bullets"]:
                            state["bullets"].remove(bullet)
                    else:
                        state["score"] += hit_enemy.score_value
                        if bullet in state["bullets"]:
                            state["bullets"].remove(bullet)
                        if hit_enemy in state["enemies"]:
                            state["enemies"].remove(hit_enemy)
                        get_sound_manager().play("enemyboom")

            for enemy in state["enemies"]:
                if state["player"].rect.colliderect(enemy.rect):
                    get_sound_manager().play("gameover")
                    get_sound_manager().stop_music()
                    state["current_state"] = "game_over"
                    game_over_menu = OverlayMenu(
                        screen,
                        "GAME OVER",
                        f"Final Score: {state['score']}"
                    )
                    break

            for eb in state["elite_bullets"]:
                if state["player"].rect.colliderect(eb.rect):
                    get_sound_manager().play("gameover")
                    get_sound_manager().stop_music()
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

        for eb in state["elite_bullets"]:
            eb.draw(screen)

        for enemy in state["enemies"]:
            enemy.draw(screen)

        state["player"].draw(screen)

        draw_text(screen, TITLE, 28, WHITE, WIDTH // 2, 28)
        draw_text(screen, f"Score: {state['score']}", 24, WHITE, 12, 12, center=False)

        if state["current_state"] == "game":
            draw_text(screen, "W A S D Move SPACE Shoot ESC Pause", 18, WHITE, WIDTH // 2, HEIGHT - 28)
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