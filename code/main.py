import random
import sys
import ctypes
from pathlib import Path

import pygame

from config import *
from music import get_sound_manager
from enemy import Enemy, EliteEnemy
from ui import (
    MainMenu,
    OverlayMenu,
    draw_background,
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
    """
    if sys.platform == "win32":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)


def set_windows_taskbar_icon_from_ico(hwnd: int, ico_path: Path) -> None:
    """
    使用 Win32 API 將 icon.ico 設定到視窗的大 / 小圖示。
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


def new_input_state():
    return {
        "left": False,
        "right": False,
        "up": False,
        "down": False,
        "shoot": False,
        "focus": False,
    }


def reset_input_state(input_state):
    for key in input_state:
        input_state[key] = False


def sync_game_input_state(input_state):
    """
    最終鍵位方案：
    - Move: WASD / Arrow keys
    - Focus: Shift
    - Shoot: Mouse Left Button
    """
    keys = pygame.key.get_pressed()
    mouse_buttons = pygame.mouse.get_pressed()

    input_state["left"] = keys[pygame.K_a] or keys[pygame.K_LEFT]
    input_state["right"] = keys[pygame.K_d] or keys[pygame.K_RIGHT]
    input_state["up"] = keys[pygame.K_w] or keys[pygame.K_UP]
    input_state["down"] = keys[pygame.K_s] or keys[pygame.K_DOWN]

    # 射擊：只用滑鼠左鍵
    input_state["shoot"] = len(mouse_buttons) > 0 and mouse_buttons[0]

    # Focus：只用 Shift（左 / 右）
    input_state["focus"] = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]


def draw_health_ui(screen, health, max_health=PLAYER_MAX_HEALTH):
    radius = 9
    gap = 8
    top = 18
    total_width = max_health * (radius * 2) + (max_health - 1) * gap
    start_x = WIDTH - 16 - total_width

    for i in range(max_health):
        x = start_x + i * (radius * 2 + gap) + radius
        color = (255, 90, 90) if i < health else (90, 40, 40)
        pygame.draw.circle(screen, color, (x, top + radius), radius)
        pygame.draw.circle(screen, WHITE, (x, top + radius), radius, 1)


def damage_player(state, screen):
    now_ms = pygame.time.get_ticks()

    if now_ms < state["invulnerable_until"]:
        return False, None

    state["player_health"] -= 1
    state["invulnerable_until"] = now_ms + PLAYER_HIT_INVULN_MS

    # 中彈後清掉敵彈，避免瞬間連續扣血
    state["enemy_bullets"].clear()

    if state["player_health"] <= 0:
        get_sound_manager().play("gameover")
        get_sound_manager().stop_music()
        state["current_state"] = "game_over"
        return True, OverlayMenu(
            screen,
            "GAME OVER",
            f"Final Score: {state['score']}"
        )

    return False, None


def begin_game(input_state):
    """
    統一開始新遊戲：
    - 重建 state
    - 切到 game
    - 清空殘留事件
    - 重置輸入狀態
    """
    state = reset_game()
    state["current_state"] = "game"
    pygame.event.clear()
    reset_input_state(input_state)
    return state


def main():
    pygame.init()
    set_windows_appusermodel_id("LAMCHONHIN.ShootingPlaneGame")

    try:
        pygame.mixer.init()
    except pygame.error:
        pass

    png_icon_path = resource_path("assets/image/icon.png")
    if png_icon_path.exists():
        icon_surface = pygame.image.load(str(png_icon_path))
        pygame.display.set_icon(icon_surface)

    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    ico_icon_path = resource_path("icon.ico")
    if sys.platform == "win32":
        wm_info = pygame.display.get_wm_info()
        hwnd = wm_info.get("window")
        set_windows_taskbar_icon_from_ico(hwnd, ico_icon_path)

    clock = pygame.time.Clock()
    menu = MainMenu(screen)
    input_state = new_input_state()
    state = reset_game()

    pause_menu = OverlayMenu(
        screen,
        "PAUSED",
        "Press ESC to resume"
    )

    game_over_menu = OverlayMenu(
        screen,
        "GAME OVER",
        "Final Score: 0"
    )

    running = True
    while running:
        dt = clock.tick(FPS)

        # =========================
        # Menu
        # =========================
        if state["current_state"] == "menu":
            get_sound_manager().play_menu_music(restart=True)
            result = menu.run()

            if result == "start":
                state = begin_game(input_state)
                get_sound_manager().play_ingame_music(restart=True)
                continue

            if result == "quit":
                get_sound_manager().stop_music()
                running = False
                break

        # =========================
        # Event handling
        # =========================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            # 視窗失去焦點時，清掉所有輸入，避免卡鍵
            if hasattr(pygame, "WINDOWFOCUSLOST") and event.type == pygame.WINDOWFOCUSLOST:
                reset_input_state(input_state)

            # 舊版相容：有些 pygame 版本會用 ACTIVEEVENT
            if event.type == pygame.ACTIVEEVENT:
                if getattr(event, "gain", 1) == 0:
                    reset_input_state(input_state)

            if state["current_state"] == "game":
                # 遊戲中只保留 ESC 走事件
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    reset_input_state(input_state)
                    get_sound_manager().stop_music()
                    state["current_state"] = "pause"

            elif state["current_state"] == "pause":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    reset_input_state(input_state)
                    state["current_state"] = "game"
                    get_sound_manager().play_ingame_music(restart=False)

                action = pause_menu.handle_event(event)
                if action == "restart":
                    state = begin_game(input_state)
                    get_sound_manager().play_ingame_music(restart=True)
                    break
                elif action == "home":
                    get_sound_manager().stop_music()
                    reset_input_state(input_state)
                    state = reset_game()
                    break
                elif action == "quit":
                    running = False
                    break

            elif state["current_state"] == "game_over":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    get_sound_manager().stop_all_sounds()
                    state = begin_game(input_state)
                    get_sound_manager().play_ingame_music(restart=True)
                    break

                action = game_over_menu.handle_event(event)
                if action == "restart":
                    get_sound_manager().stop_all_sounds()
                    state = begin_game(input_state)
                    get_sound_manager().play_ingame_music(restart=True)
                    break
                elif action == "home":
                    get_sound_manager().stop_all_sounds()
                    get_sound_manager().stop_music()
                    reset_input_state(input_state)
                    state = reset_game()
                    break
                elif action == "quit":
                    get_sound_manager().stop_all_sounds()
                    get_sound_manager().stop_music()
                    running = False
                    break

        if not running:
            break

        # =========================
        # Game update
        # =========================
        if state["current_state"] == "game":
            # 每一幀同步實際按鍵狀態
            sync_game_input_state(input_state)

            # 玩家移動（包含 Focus）
            state["player"].move(input_state)

            # 玩家持續射擊
            if input_state["shoot"] and state["player"].can_shoot():
                state["bullets"].append(state["player"].shoot())

            update_stars(state["stars"])

            # 玩家子彈更新
            for bullet in state["bullets"][:]:
                bullet.update()
                if bullet.rect.bottom < 0:
                    state["bullets"].remove(bullet)

            # 敵方彈幕更新 + graze
            for eb in state["enemy_bullets"][:]:
                eb.update()

                if (
                    eb.rect.top > HEIGHT
                    or eb.rect.left > WIDTH + 40
                    or eb.rect.right < -40
                ):
                    state["enemy_bullets"].remove(eb)
                    continue

                if (not eb.grazed) and state["player"].bullet_grazes(eb.rect):
                    eb.grazed = True
                    state["graze"] += 1

            # 生怪
            state["spawn_timer"] += dt
            if state["spawn_timer"] >= ENEMY_SPAWN_MS and len(state["enemies"]) < MAX_ENEMIES:
                state["spawn_timer"] = 0
                elite_prob = get_elite_spawn_probability(state["score"])
                if random.random() < elite_prob:
                    state["enemies"].append(EliteEnemy())
                else:
                    state["enemies"].append(Enemy())

            now_ms = pygame.time.get_ticks()

            # 敵機更新 + 射擊
            for enemy in state["enemies"][:]:
                enemy.update()

                new_bullets = enemy.shoot(now_ms)
                if new_bullets:
                    state["enemy_bullets"].extend(new_bullets)

                if enemy.rect.top > HEIGHT:
                    state["enemies"].remove(enemy)

            # 玩家子彈打中敵機
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
                            if hit_enemy in state["enemies"]:
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

            # 玩家碰到敵機
            for enemy in state["enemies"][:]:
                if state["player"].rect.colliderect(enemy.rect):
                    if enemy in state["enemies"]:
                        state["enemies"].remove(enemy)

                    game_over, new_game_over_menu = damage_player(state, screen)
                    if game_over:
                        game_over_menu = new_game_over_menu
                        reset_input_state(input_state)
                        break

            # 玩家被敵彈命中（中心判定點）
            if state["current_state"] == "game":
                for eb in state["enemy_bullets"][:]:
                    if state["player"].bullet_hits(eb.rect):
                        if eb in state["enemy_bullets"]:
                            state["enemy_bullets"].remove(eb)

                        game_over, new_game_over_menu = damage_player(state, screen)
                        if game_over:
                            game_over_menu = new_game_over_menu
                            reset_input_state(input_state)
                            break

        # =========================
        # Draw
        # =========================
        draw_background(screen, state["stars"])

        for star in state["stars"]:
            pygame.draw.circle(screen, WHITE, (int(star[0]), int(star[1])), star[2])

        for bullet in state["bullets"]:
            bullet.draw(screen)

        for eb in state["enemy_bullets"]:
            eb.draw(screen)

        for enemy in state["enemies"]:
            enemy.draw(screen)

        # 玩家中彈後透明閃爍
        now_ms = pygame.time.get_ticks()
        player_visible = True
        if state["current_state"] == "game" and now_ms < state["invulnerable_until"]:
            flash_phase = (now_ms // PLAYER_HIT_FLASH_INTERVAL_MS) % 2
            player_visible = (flash_phase == 0)

        if player_visible:
            state["player"].draw(screen)

        # Focus 或無敵期間顯示判定點
        if state["current_state"] == "game" and (
            state["player"].focused or now_ms < state["invulnerable_until"]
        ):
            state["player"].draw_hitbox(screen)

        # UI
        draw_text(screen, TITLE, 28, WHITE, WIDTH // 2, 28)
        draw_text(screen, f"Score: {state['score']}", 24, WHITE, 12, 12, center=False)
        draw_text(screen, f"Graze: {state['graze']}", 22, WHITE, 12, 40, center=False)
        draw_health_ui(screen, state["player_health"], PLAYER_MAX_HEALTH)

        if state["current_state"] == "game":
            draw_text(
                screen,
                "WASD Move | SHIFT Focus | LMB Shoot | ESC Pause",
                18,
                WHITE,
                WIDTH // 2,
                HEIGHT - 28
            )
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
