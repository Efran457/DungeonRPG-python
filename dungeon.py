from typing_extensions import Any
from typing import Tuple
import pygame
import sys
import random
import json
import os

pygame.init()

import sys, os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    relative_path = relative_path.replace("/", os.sep).replace("\\", os.sep)
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_font(path: str, size: int) -> pygame.font.Font:
    """ Load a font safely, falling back to pygame default if not found """
    full_path = resource_path(path)
    if os.path.exists(full_path):
        return pygame.font.Font(full_path, size)
    print(f"[WARN] Font not found: {full_path} — using system default")
    return pygame.font.SysFont("arial", size)

# region Helper functions
def get_all_enemy_in_map() -> list[Tuple[int, int]]:
    all_enemys_in_map: list[Tuple[int, int]] = []
    for y in range(TILE_HEIGHT):
        for x in range(TILE_WIDTH):
            if Map[y][x] == "E":
                all_enemys_in_map.append((x, y))
    return all_enemys_in_map

def get_player_pos() -> Tuple[int, int]:
    for y in range(TILE_HEIGHT):
        for x in range(TILE_WIDTH):
            if Map[y][x] == "P":
                return x, y
    return 0, 0

def reset_game() -> None:
    global Map, TILE_HEIGHT, TILE_WIDTH, TILE_SIZE
    global WIDTH, HEIGHT, player_pos, keys_collected, max_keys, all_enemy
    global wall_tile, floor_tile, key_tile, door_tile, enemy_tile, player_tile

    TILE_HEIGHT = len(Map)
    TILE_WIDTH = len(Map[0])
    # Rescale Tiles
    wall_tile = pygame.transform.scale(
        pygame.image.load(resource_path("assets/images/wall.png")), (TILE_SIZE, TILE_SIZE))
    floor_tile = pygame.transform.scale(
        pygame.image.load(resource_path("assets/images/floor_tile1.png")), (TILE_SIZE, TILE_SIZE))
    key_tile = pygame.transform.scale(
        pygame.image.load(resource_path("assets/images/key.png")), (TILE_SIZE, TILE_SIZE))
    door_tile = pygame.transform.scale(
        pygame.image.load(resource_path("assets/images/door.png")), (TILE_SIZE, TILE_SIZE))
    enemy_tile = pygame.transform.scale(
        pygame.image.load(resource_path("assets/images/enemy.png")), (TILE_SIZE, TILE_SIZE))
    player_tile = pygame.transform.scale(
        pygame.image.load(resource_path("assets/images/Player.png")), (TILE_SIZE, TILE_SIZE))

    icon = pygame.transform.scale(
        pygame.image.load(resource_path("assets/images/icon.png")), (64, 64))

    player_pos = get_player_pos()
    keys_collected = 0
    max_keys = get_all_keys_in_map(level_path)
    all_enemy = get_all_enemy_in_map()

def spawn_animation() -> None:
    global offset, level_path, clock
    offset = (0, 100)
    name, des = get_game_name_and_description(level_path)
    small_font = load_font("assets/font/nfpixels_font.ttf", 30)
    text = font.render(name, True, (255, 255, 255))
    inftext = small_font.render(des, True, (255, 255, 255))
    showing_text = True
    duration = 2
    timer = 0
    while showing_text:
        dt = clock.tick(60) / 1000
        timer += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                showing_text = False
        draw_bg()
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, (HEIGHT // 2 - text.get_height() // 2) - 40))
        screen.blit(inftext, (WIDTH // 2 - inftext.get_width() // 2, (HEIGHT // 2 + text.get_height()) - 70))
        if timer > duration:
            showing_text = False
        pygame.display.flip()

    clock = pygame.time.Clock()
    start_y = 10
    target_y = 0
    current_y = start_y
    playing_anim = True
    fade_timer = 0

    while playing_anim:
        dt = clock.tick(60) / 1000
        fade_timer += dt * 2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current_y += (target_y - current_y) * 0.1
        if abs(current_y - target_y) < 0.01 and fade_timer >= 1:
            current_y = target_y
            playing_anim = False

        offset = (0, current_y)
        draw_bg()
        draw_entitys_no_offset(fade_timer)
        text.set_alpha(255 - int(fade_timer * 255))
        inftext.set_alpha(255 - int(fade_timer * 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, (HEIGHT // 2 - text.get_height() // 2) - 40))
        screen.blit(inftext, (WIDTH // 2 - inftext.get_width() // 2, (HEIGHT // 2 + text.get_height()) - 70))
        pygame.display.flip()

    offset = (0, 0)
    Map[player_pos[1]][player_pos[0]] = "P"

def draw_entitys_no_offset(opasety: float) -> None:
    for y in range(TILE_HEIGHT):
        for x in range(TILE_WIDTH):
            tile = Map[y][x]
            match tile:
                case "W":
                    screen.blit(wall_tile, (calculate_kord(x + offset[0], y + offset[1])))
                case "D":
                    screen.blit(door_tile, (calculate_kord(x + offset[0], y + offset[1])))
                case "E":
                    enemy_tile.set_alpha(int(opasety * 255))
                    screen.blit(enemy_tile, (calculate_kord(x, y)))
                case "P":
                    player_tile.set_alpha(int(opasety * 255))
                    screen.blit(player_tile, (calculate_kord(x, y)))
                case "K":
                    screen.blit(key_tile, (calculate_kord(x + offset[0], y + offset[1])))

def move_player(dx: int, dy: int) -> Tuple[int, int]:
    global player_pos, state
    try:
        x, y = player_pos
        new_x = x + dx
        new_y = y + dy
        if not can_player_move((new_x, new_y)):
            return player_pos
        Map[y][x] = " "
        Map[new_y][new_x] = "P"
        update_camera()
        return new_x, new_y
    except IndexError:
        state = f"{'win' if can_win() else 'game_over'}"
        return player_pos

def update_camera() -> None:
    global offset
    screen_tiles_x = WIDTH // TILE_SIZE
    screen_tiles_y = HEIGHT // TILE_SIZE
    cam_x = (screen_tiles_x // 2) - player_pos[0]
    cam_y = (screen_tiles_y // 2) - player_pos[1]
    cam_x = min(0, max(cam_x, screen_tiles_x - TILE_WIDTH))
    cam_y = min(0, max(cam_y, screen_tiles_y - TILE_HEIGHT))
    offset = (cam_x, cam_y)

def can_player_move(pos: Tuple[int, int]) -> bool:
    global keys_collected, max_keys
    new_pos: str = Map[pos[1]][pos[0]]
    match new_pos:
        case "W":
            return False
        case "D":
            return keys_collected == max_keys
        case "K":
            keys_collected += 1
            if keys_collected == max_keys:
                remove_door()
            return True
        case "E":
            game_over()
            return False
        case _:
            return True

def can_win() -> bool:
    old_map = load_game_map(level_path)
    for y in range(TILE_HEIGHT):
        for x in range(TILE_WIDTH):
            if old_map[y][x] == "D" and Map[y][x] == "P":
                return True
    return False

def remove_door() -> None:
    for y in range(TILE_HEIGHT):
        for x in range(TILE_WIDTH):
            if Map[y][x] == "D":
                Map[y][x] = " "

def calculate_kord(x: int, y: int) -> Tuple[int, int]:
    return x * TILE_SIZE, y * TILE_SIZE

def draw_map() -> None:
    for y in range(TILE_HEIGHT):
        for x in range(TILE_WIDTH):
            tile = Map[y][x]
            match tile:
                case "W":
                    screen.blit(wall_tile, (calculate_kord(x + offset[0], y + offset[1])))
                case "D":
                    screen.blit(door_tile, (calculate_kord(x + offset[0], y + offset[1])))
                case "E":
                    screen.blit(enemy_tile, (calculate_kord(x + offset[0], y + offset[1])))
                case "P":
                    screen.blit(player_tile, (calculate_kord(x + offset[0], y + offset[1])))
                case "K":
                    screen.blit(key_tile, (calculate_kord(x + offset[0], y + offset[1])))

def draw_bg() -> None:
    for y in range(TILE_HEIGHT):
        for x in range(TILE_WIDTH):
            screen.blit(floor_tile, (calculate_kord(x, y)))

def move_all_enemy() -> list[Tuple[int, int]]:
    global all_enemy
    all_new_enemy: list[Tuple[int, int]] = []
    for i in range(len(all_enemy)):
        all_new_enemy.append(move_a_enemy(all_enemy[i]))
    draw_map()
    return all_new_enemy

def move_a_enemy(pos: Tuple[int, int]) -> Tuple[int, int]:
    dx, dy = enemy_ai(pos)
    new_x = pos[0] + dx
    new_y = pos[1] + dy
    if can_enemy_move((new_x, new_y)):
        Map[pos[1]][pos[0]] = " "
        Map[new_y][new_x] = "E"
        return new_x, new_y
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    random.shuffle(directions)
    for rdx, rdy in directions:
        rand_x = pos[0] + rdx
        rand_y = pos[1] + rdy
        if can_enemy_move((rand_x, rand_y)):
            Map[pos[1]][pos[0]] = " "
            Map[rand_y][rand_x] = "E"
            return rand_x, rand_y
    return pos

def can_enemy_move(pos: Tuple[int, int]) -> bool:
    new_pos: str = Map[pos[1]][pos[0]]
    match new_pos:
        case "W":
            return False
        case "D":
            return False
        case "K":
            return False
        case "E":
            return False
        case "P":
            game_over()
            return True
        case _:
            return True

def enemy_ai(pos: Tuple[int, int]) -> Tuple[int, int]:
    global player_pos
    if player_pos[0] > pos[0]:
        return 1, 0
    elif player_pos[0] < pos[0]:
        return -1, 0
    if player_pos[1] > pos[1]:
        return 0, 1
    elif player_pos[1] < pos[1]:
        return 0, -1
    return 0, 0

def game_over() -> None:
    global state
    state = "game_over"

def removePlayer() -> None:
    Map[player_pos[1]][player_pos[0]] = " " if Map[player_pos[1]][player_pos[0]] == "P" else Map[player_pos[1]][player_pos[0]]
# endregion

# region Json logic
def load_game_map(json_path: str) -> list[list[str]]:
    with open(json_path, "r") as f:
        data = json.load(f)
    return [list(row) for row in data["map"]]

def get_game_name_and_description(json_path: str) -> tuple[str, str]:
    with open(json_path, "r") as f:
        data = json.load(f)
    return data["name"], data["des"]

def get_all_keys_in_map(json_path: str) -> int:
    with open(json_path, "r") as f:
        data = json.load(f)
    try:
        return data["max-keys"]
    except KeyError:
        map_data = data["map"]
        key_count = sum(row.count("K") for row in map_data)
        return key_count if key_count > 0 else 3
# endregion

# region Setup variables
level = 1
level_path = os.path.join(resource_path(f"assets/levels/lvl{level}.json"))
font = load_font("assets/font/nfpixels_font.ttf", 50)

# W = 'Wall', D = 'Door', E = 'Enemy', K = 'Key', P = 'Player'
Map: list[list[Any]] = load_game_map(level_path)

TILE_WIDTH: int = len(Map[0])
TILE_HEIGHT: int = len(Map)
TILE_SIZE: int = 50

max_keys = get_all_keys_in_map(level_path)
WIDTH: int = TILE_WIDTH * TILE_SIZE
HEIGHT: int = TILE_HEIGHT * TILE_SIZE
# endregion

# region Load Images
wall_tile = pygame.transform.scale(
    pygame.image.load(resource_path("assets/images/wall.png")), (TILE_SIZE, TILE_SIZE))
floor_tile = pygame.transform.scale(
    pygame.image.load(resource_path("assets/images/floor_tile1.png")), (TILE_SIZE, TILE_SIZE))
key_tile = pygame.transform.scale(
    pygame.image.load(resource_path("assets/images/key.png")), (TILE_SIZE, TILE_SIZE))
door_tile = pygame.transform.scale(
    pygame.image.load(resource_path("assets/images/door.png")), (TILE_SIZE, TILE_SIZE))
enemy_tile = pygame.transform.scale(
    pygame.image.load(resource_path("assets/images/enemy.png")), (TILE_SIZE, TILE_SIZE))
player_tile = pygame.transform.scale(
    pygame.image.load(resource_path("assets/images/Player.png")), (TILE_SIZE, TILE_SIZE))

icon = pygame.transform.scale(
    pygame.image.load(resource_path("assets/images/icon.png")), (64, 64))
# endregion

# Initialize window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DungeonRPG")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# Main variables
player_pos = get_player_pos()
keys_collected = 0
all_enemy = get_all_enemy_in_map()

enemy_move_internals = 0.6  # customizable speed
enemy_speed_timer = 0       # don't change
player_move_internals = 0.1 # customizable speed
player_speed_timer = 0      # don't change
offset: tuple[int, int] = (0, 0)

state = "playing"
spawn_animation()

# region Main game loop
running = True
while running:
    dt = clock.tick(60) / 1000
    enemy_speed_timer += dt
    player_speed_timer += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if state == "playing":
        if player_speed_timer >= player_move_internals:
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player_pos = move_player(0, -1)
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player_pos = move_player(0, 1)
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player_pos = move_player(-1, 0)
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player_pos = move_player(1, 0)
            player_speed_timer = 0

        if enemy_speed_timer >= enemy_move_internals:
            all_enemy = move_all_enemy()
            enemy_speed_timer = 0

    draw_bg()
    draw_map()

    if state == "game_over":
        removePlayer()
        draw_map()
        text = font.render("Game Over! Press R to Restart", True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        if keys[pygame.K_r]:
            Map = load_game_map(level_path)
            reset_game()
            state = "playing"

    elif state == "win":
        text = font.render("You Win!", True, (0, 255, 0))
        inftext = font.render("Press Enter to Continue", True, (0, 255, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        screen.blit(inftext, (WIDTH // 2 - inftext.get_width() // 2, HEIGHT // 2 + text.get_height()))
        if keys[pygame.K_RETURN]:
            level += 1
            level_path = resource_path(f"assets/levels/lvl{level}.json")
            Map = load_game_map(level_path)
            reset_game()
            spawn_animation()
            state = "playing"

    pygame.display.flip()
# endregion

pygame.quit()
sys.exit()