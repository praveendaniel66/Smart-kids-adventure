"""
Smart Kids Adventure  -  Educational Game for Kids (3-8 years)
Desktop Windows build  |  Python + Pygame
"""

import sys
import os
import math
import random
import struct
import wave
import io

import pygame
from pygame import gfxdraw

from levels import LEVELS_PART1, LEVELS_PART2, POOL_PART3, get_random_levels, get_runner_level, get_panda_level_data

# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------
SCREEN_W, SCREEN_H = 900, 640
FPS = 60
PLAYER_SPEED = 5
OPTION_SIZE = 100          # width/height of answer bubble
BG_COLOR = (200, 230, 255) # light sky blue
JOYSTICK_DEADZONE = 0.3    # ignore small stick drift

# Colour palette -----------------------------------------------------------
WHITE       = (255, 255, 255)
BLACK       = (0, 0, 0)
GRAY        = (180, 180, 180)
DARK_GRAY   = (80, 80, 80)
SKY_TOP     = (135, 206, 250)
SKY_BOT     = (200, 230, 255)
GREEN_GRASS = (120, 200, 100)
GOLD        = (255, 200, 50)
RED         = (230, 70, 70)
GREEN       = (80, 200, 120)
BLUE        = (80, 140, 240)
PURPLE      = (160, 100, 220)
PINK        = (255, 150, 180)
ORANGE      = (255, 160, 60)
TEAL        = (60, 200, 200)

OPTION_COLORS = [
    (255, 120, 120),  # soft red
    (120, 200, 255),  # soft blue
    (120, 230, 140),  # soft green
    (255, 200, 100),  # soft orange
]

# Runner mode constants
RUNNER_LANE_COUNT = 3
RUNNER_LANE_WIDTH = 160
RUNNER_ITEM_H = 60
RUNNER_PLAYER_Y = SCREEN_H - 120
RUNNER_SPEEDS = {1: 2.0, 2: 2.5, 3: 3.0, 4: 3.5, 5: 4.0}
RUNNER_OBSTACLE_RATES = {1: 0.008, 2: 0.012, 3: 0.016, 4: 0.020, 5: 0.025}
RUNNER_DISTRACTOR_RATE = 0.006

# Panda mode constants
PANDA_SPEED = 7
PANDA_BASE_SIZE = 90
PANDA_FALL_SPEEDS = {
    1: 1.0, 2: 1.4, 3: 1.8, 4: 2.2, 5: 2.6,
    6: 3.0, 7: 3.4, 8: 3.8, 9: 4.2, 10: 4.6,
}
PANDA_MAX_HEARTS = 3
PANDA_LANE_COUNT = 4
PANDA_LANE_W = 180
PANDA_PLAYER_Y = SCREEN_H - 140
FOOD_NAMES = ["bamboo", "cookie", "honey", "fruit", "cake"]
STICKER_NAMES = ["Star", "Trophy", "Ribbon", "Sparkle", "Bullseye",
                 "Circus", "Palette", "Gamepad", "Music", "Crown"]
THEME_FOREST = 0
THEME_SNOW = 1
THEME_BEACH = 2
THEME_SPACE = 3
THEME_CANDY = 4
LEVEL_THEMES = {
    1: THEME_FOREST,  2: THEME_FOREST,
    3: THEME_SNOW,    4: THEME_SNOW,
    5: THEME_BEACH,   6: THEME_BEACH,
    7: THEME_SPACE,   8: THEME_SPACE,
    9: THEME_CANDY,  10: THEME_CANDY,
}
ACCESSORY_UNLOCKS = {2: "hat", 4: "sunglasses", 6: "bowtie", 8: "crown", 10: "cape"}

# Per-category accent colors used in the HUD badge
CATEGORY_COLORS = {
    "Colors":   (200,  60, 180),   # vivid magenta
    "Animals":  ( 50, 170,  70),   # fresh green
    "Numbers":  ( 50, 120, 230),   # royal blue
    "Fruits":   (240, 120,  30),   # warm orange
    "Shapes":   (130,  60, 220),   # deep purple
    "Letters":  ( 40, 190, 190),   # teal
}

# Animal-to-Image File Mapping (STRICT)
ANIMAL_IMAGE_MAPPING = {
    "CAT": "assets/animals/cat.png", "DOG": "assets/animals/dog.png", 
    "FISH": "assets/animals/fish.png", "BIRD": "assets/animals/bird.png",
    "FROG": "assets/animals/frog.png", "BEAR": "assets/animals/bear.png", 
    "LION": "assets/animals/lion.png", "DUCK": "assets/animals/duck.png",
    "PIG": "assets/animals/pig.png", "COW": "assets/animals/cow.png", 
    "FOX": "assets/animals/fox.png", "WOLF": "assets/animals/wolf.png",
    "DEER": "assets/animals/deer.png", "ANT": "assets/animals/ant.png", 
    "BEE": "assets/animals/bee.png"
}

# Sticker emoji-like symbols drawn procedurally (one per level)
STICKER_EMOJIS = ["⭐", "🏆", "🎀", "✨", "🎯", "🎪", "🎨", "🎮", "🎵", "👑"]

# Funny wrong-answer messages
WRONG_MESSAGES = [
    "Oops! That tickled!",
    "Haha NOPE!",
    "Bananas! Try again!",
    "Silly goose!",
    "Whoopsie daisy!",
    "Nice try, buddy!",
    "Wiggle wiggle... WRONG!",
    "Oh no, spaghetti!",
    "Boing! Not that one!",
    "Uh oh, stinky!",
    "Oops-a-doodle!",
    "Nah nah nah!",
    "Try again, superstar!",
    "Almost! But nope!",
    "Wobbly wobbly WRONG!",
]

# ---------------------------------------------------------------------------
# HELPER  -  procedural asset creation
# ---------------------------------------------------------------------------

def make_gradient_bg(w: int, h: int) -> pygame.Surface:
    """Create a vertical gradient background sky with grass."""
    surf = pygame.Surface((w, h))
    grass_h = 80
    for y in range(h - grass_h):
        t = y / (h - grass_h)
        r = int(SKY_TOP[0] + (SKY_BOT[0] - SKY_TOP[0]) * t)
        g = int(SKY_TOP[1] + (SKY_BOT[1] - SKY_TOP[1]) * t)
        b = int(SKY_TOP[2] + (SKY_BOT[2] - SKY_TOP[2]) * t)
        pygame.draw.line(surf, (r, g, b), (0, y), (w, y))
    # grass
    pygame.draw.rect(surf, GREEN_GRASS, (0, h - grass_h, w, grass_h))
    # small clouds
    for cx, cy in [(150, 80), (400, 50), (700, 90), (250, 130)]:
        _draw_cloud(surf, cx, cy)
    return surf


def _draw_cloud(surf: pygame.Surface, cx: int, cy: int):
    col = (255, 255, 255, 180)
    tmp = pygame.Surface((120, 60), pygame.SRCALPHA)
    pygame.draw.ellipse(tmp, col, (20, 15, 50, 35))
    pygame.draw.ellipse(tmp, col, (0, 25, 45, 30))
    pygame.draw.ellipse(tmp, col, (45, 10, 55, 40))
    pygame.draw.ellipse(tmp, col, (70, 20, 50, 35))
    surf.blit(tmp, (cx - 60, cy - 30))


def make_player_surface(size: int = 64) -> pygame.Surface:
    """Draw a cute round character programmatically."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    r = size // 2 - 4

    # Body circle  (bright blue)
    pygame.draw.circle(surf, (80, 160, 255), (cx, cy), r)
    pygame.draw.circle(surf, (50, 120, 220), (cx, cy), r, 3)

    # Rosy cheeks
    pygame.draw.circle(surf, (255, 180, 180), (cx - r // 2, cy + 4), 6)
    pygame.draw.circle(surf, (255, 180, 180), (cx + r // 2, cy + 4), 6)

    # Eyes  (white + black pupil)
    for ex in (cx - 9, cx + 9):
        pygame.draw.circle(surf, WHITE, (ex, cy - 6), 7)
        pygame.draw.circle(surf, BLACK, (ex, cy - 5), 4)
        pygame.draw.circle(surf, WHITE, (ex - 1, cy - 7), 2)  # glint

    # Smile
    pygame.draw.arc(surf, (40, 40, 40), (cx - 10, cy - 2, 20, 16), 3.4, 6.0, 2)

    # Tiny cape  (red triangle on back)
    cape_pts = [(cx, cy + r - 6), (cx - 14, cy + r + 8), (cx + 14, cy + r + 8)]
    pygame.draw.polygon(surf, (230, 60, 60), cape_pts)

    return surf


def make_star_surface(size: int = 40) -> pygame.Surface:
    """Draw a gold star."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    points = []
    for i in range(10):
        angle = math.radians(-90 + i * 36)
        rad = (size // 2 - 2) if i % 2 == 0 else (size // 4)
        points.append((cx + rad * math.cos(angle), cy + rad * math.sin(angle)))
    pygame.draw.polygon(surf, GOLD, points)
    pygame.draw.polygon(surf, (200, 160, 30), points, 2)
    return surf


def make_panda_surface(size=90, growth=0, expression="happy", accessories=None, ticks=0.0):
    """Draw a super cute chubby baby panda procedurally."""
    scale = 1.0 + growth * 0.025
    sz = int(size * scale)
    pad = 40
    total = sz + pad * 2
    surf = pygame.Surface((total, total + 30), pygame.SRCALPHA)
    cx = total // 2
    cy = total // 2 - 5
    r = sz // 2

    # Dancing wobble
    dance_off = 0
    if expression == "dancing":
        dance_off = int(math.sin(ticks * 8) * 6)
        cy += abs(int(math.sin(ticks * 6) * 8))

    # --- CAPE accessory (behind body) ---
    if accessories and "cape" in accessories:
        cape_pts = [(cx - r + 5, cy + 10), (cx + r - 5, cy + 10),
                    (cx + r + 10, cy + r + 40), (cx - r - 10, cy + r + 40)]
        pygame.draw.polygon(surf, (220, 40, 40), cape_pts)
        pygame.draw.polygon(surf, (180, 30, 30), cape_pts, 3)

    # --- EARS ---
    ear_r = max(8, int(r * 0.35))
    ear_ox = int(r * 0.68)
    ear_oy = int(r * 0.65)
    pygame.draw.circle(surf, BLACK, (cx - ear_ox + dance_off, cy - ear_oy), ear_r)
    pygame.draw.circle(surf, (50, 50, 50), (cx - ear_ox + dance_off, cy - ear_oy), ear_r - 3)
    pygame.draw.circle(surf, BLACK, (cx + ear_ox + dance_off, cy - ear_oy), ear_r)
    pygame.draw.circle(surf, (50, 50, 50), (cx + ear_ox + dance_off, cy - ear_oy), ear_r - 3)

    # --- HEAD ---
    pygame.draw.circle(surf, (252, 252, 252), (cx + dance_off, cy), r)
    pygame.draw.circle(surf, (245, 245, 245), (cx + dance_off, cy), r - 2)

    # --- BODY ---
    body_w = int(r * 1.6)
    body_h = int(r * 1.1)
    body_cy = cy + int(r * 0.75)
    body_rect = (cx - body_w // 2 + dance_off, body_cy, body_w, body_h)
    pygame.draw.ellipse(surf, (250, 250, 250), body_rect)
    # Tummy
    tw = int(body_w * 0.55)
    th = int(body_h * 0.7)
    pygame.draw.ellipse(surf, (235, 230, 220), (cx - tw // 2 + dance_off, body_cy + 5, tw, th))

    # --- ARMS (black paws) ---
    paw_r = max(6, int(r * 0.22))
    pygame.draw.circle(surf, BLACK, (cx - int(r * 0.85) + dance_off, body_cy + 15), paw_r)
    pygame.draw.circle(surf, BLACK, (cx + int(r * 0.85) + dance_off, body_cy + 15), paw_r)

    # --- FEET ---
    foot_r = max(7, int(r * 0.2))
    pygame.draw.ellipse(surf, BLACK, (cx - int(r * 0.5) + dance_off - foot_r,
                                       body_cy + body_h - foot_r, foot_r * 2, int(foot_r * 1.3)))
    pygame.draw.ellipse(surf, BLACK, (cx + int(r * 0.5) + dance_off - foot_r,
                                       body_cy + body_h - foot_r, foot_r * 2, int(foot_r * 1.3)))

    # --- EYE PATCHES ---
    pw = max(12, int(r * 0.38))
    ph = max(10, int(r * 0.32))
    left_ex = cx - int(r * 0.35) + dance_off
    right_ex = cx + int(r * 0.35) + dance_off
    eye_y = cy - int(r * 0.1)
    pygame.draw.ellipse(surf, BLACK, (left_ex - pw // 2, eye_y - ph // 2, pw, ph))
    pygame.draw.ellipse(surf, BLACK, (right_ex - pw // 2, eye_y - ph // 2, pw, ph))

    # --- EYES ---
    er = max(5, int(r * 0.14))
    if expression == "sad":
        # Droopy sad eyes
        pygame.draw.circle(surf, WHITE, (left_ex, eye_y + 1), er)
        pygame.draw.circle(surf, WHITE, (right_ex, eye_y + 1), er)
        pygame.draw.circle(surf, (30, 30, 30), (left_ex, eye_y + 2), int(er * 0.5))
        pygame.draw.circle(surf, (30, 30, 30), (right_ex, eye_y + 2), int(er * 0.5))
        # Tear
        tear_y = eye_y + er + 3
        pygame.draw.circle(surf, (100, 180, 255), (left_ex + 3, tear_y), 3)
    elif expression == "chewing":
        # Squinty happy eyes
        pygame.draw.arc(surf, WHITE, (left_ex - er, eye_y - er // 2, er * 2, er), 0.3, 2.8, 3)
        pygame.draw.arc(surf, WHITE, (right_ex - er, eye_y - er // 2, er * 2, er), 0.3, 2.8, 3)
    else:
        # Big shiny eyes
        pygame.draw.circle(surf, WHITE, (left_ex, eye_y), er)
        pygame.draw.circle(surf, WHITE, (right_ex, eye_y), er)
        pr = max(2, int(er * 0.55))
        pygame.draw.circle(surf, (20, 20, 20), (left_ex, eye_y), pr)
        pygame.draw.circle(surf, (20, 20, 20), (right_ex, eye_y), pr)
        # Glints
        gr = max(1, int(er * 0.3))
        pygame.draw.circle(surf, WHITE, (left_ex - 2, eye_y - 2), gr)
        pygame.draw.circle(surf, WHITE, (right_ex - 2, eye_y - 2), gr)

    # --- NOSE ---
    nose_y = cy + int(r * 0.15)
    pygame.draw.ellipse(surf, (40, 40, 40), (cx - 5 + dance_off, nose_y, 10, 7))

    # --- MOUTH ---
    mouth_y = nose_y + 9
    if expression == "chewing":
        # Chomping mouth
        open_h = int(6 + abs(math.sin(ticks * 10)) * 8)
        pygame.draw.ellipse(surf, (200, 80, 80), (cx - 8 + dance_off, mouth_y, 16, open_h))
        pygame.draw.ellipse(surf, (160, 50, 50), (cx - 5 + dance_off, mouth_y + 2, 10, max(2, open_h - 4)))
    elif expression == "sad":
        pygame.draw.arc(surf, (40, 40, 40), (cx - 8 + dance_off, mouth_y + 4, 16, 10), 0.3, 2.8, 2)
    elif expression == "dancing":
        pygame.draw.ellipse(surf, (200, 90, 90), (cx - 10 + dance_off, mouth_y - 2, 20, 14))
        pygame.draw.arc(surf, (40, 40, 40), (cx - 10 + dance_off, mouth_y, 20, 10), 3.4, 6.0, 2)
    else:
        pygame.draw.arc(surf, (40, 40, 40), (cx - 8 + dance_off, mouth_y, 16, 10), 3.4, 6.0, 2)

    # --- ROSY CHEEKS ---
    cr = max(4, int(r * 0.12))
    cheek_s = pygame.Surface((cr * 2, cr * 2), pygame.SRCALPHA)
    pygame.draw.circle(cheek_s, (255, 170, 180, 100), (cr, cr), cr)
    surf.blit(cheek_s, (cx - int(r * 0.55) + dance_off - cr, cy + int(r * 0.2) - cr))
    surf.blit(cheek_s, (cx + int(r * 0.55) + dance_off - cr, cy + int(r * 0.2) - cr))

    # --- ACCESSORIES ---
    if accessories:
        if "hat" in accessories:
            pts = [(cx + dance_off, cy - r - 22), (cx - 16 + dance_off, cy - r + 4),
                   (cx + 16 + dance_off, cy - r + 4)]
            pygame.draw.polygon(surf, (230, 50, 50), pts)
            pygame.draw.polygon(surf, (200, 40, 40), pts, 2)
            pygame.draw.circle(surf, GOLD, (cx + dance_off, cy - r - 22), 4)
        if "sunglasses" in accessories:
            gy = eye_y - 2
            pygame.draw.rect(surf, (30, 30, 30), (left_ex - er - 2 , gy - er + 1, er * 2 + 4, er * 2 - 2), border_radius=4)
            pygame.draw.rect(surf, (30, 30, 30), (right_ex - er - 2, gy - er + 1, er * 2 + 4, er * 2 - 2), border_radius=4)
            pygame.draw.line(surf, (30, 30, 30), (left_ex + er + 2, gy), (right_ex - er - 2, gy), 2)
        if "bowtie" in accessories:
            bt_y = cy + int(r * 0.45)
            pts_l = [(cx + dance_off, bt_y), (cx - 14 + dance_off, bt_y - 7), (cx - 14 + dance_off, bt_y + 7)]
            pts_r = [(cx + dance_off, bt_y), (cx + 14 + dance_off, bt_y - 7), (cx + 14 + dance_off, bt_y + 7)]
            pygame.draw.polygon(surf, (60, 60, 200), pts_l)
            pygame.draw.polygon(surf, (60, 60, 200), pts_r)
            pygame.draw.circle(surf, (80, 80, 220), (cx + dance_off, bt_y), 4)
        if "crown" in accessories:
            cw, ch = 30, 18
            crown_y = cy - r - 14
            pts = [(cx - cw // 2 + dance_off, crown_y + ch), (cx - cw // 2 + dance_off, crown_y + 5),
                   (cx - cw // 4 + dance_off, crown_y + ch - 5), (cx + dance_off, crown_y),
                   (cx + cw // 4 + dance_off, crown_y + ch - 5), (cx + cw // 2 + dance_off, crown_y + 5),
                   (cx + cw // 2 + dance_off, crown_y + ch)]
            pygame.draw.polygon(surf, GOLD, pts)
            pygame.draw.polygon(surf, (200, 160, 30), pts, 2)
    return surf


def make_food_surface(food_type, size=36):
    """Draw a simple food item."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    r = size // 2 - 2
    if food_type == "bamboo":
        pygame.draw.rect(surf, (80, 180, 80), (cx - 4, 2, 8, size - 4), border_radius=3)
        pygame.draw.rect(surf, (60, 150, 60), (cx - 4, 2, 8, size - 4), 2, border_radius=3)
        for yy in range(6, size - 4, 8):
            pygame.draw.line(surf, (60, 140, 60), (cx - 4, yy), (cx + 4, yy), 1)
        pygame.draw.ellipse(surf, (100, 200, 80), (cx - 2, 0, 12, 8))
    elif food_type == "cookie":
        pygame.draw.circle(surf, (200, 160, 80), (cx, cy), r)
        pygame.draw.circle(surf, (180, 140, 60), (cx, cy), r, 2)
        for dx, dy in [(-5, -4), (4, -6), (-3, 5), (6, 3), (0, 0)]:
            pygame.draw.circle(surf, (100, 60, 30), (cx + dx, cy + dy), 3)
    elif food_type == "honey":
        pygame.draw.circle(surf, (240, 190, 50), (cx, cy), r)
        pygame.draw.circle(surf, (220, 170, 40), (cx, cy), r, 2)
        pygame.draw.circle(surf, (255, 220, 100), (cx - 3, cy - 3), r // 3)
    elif food_type == "fruit":
        pygame.draw.circle(surf, (220, 50, 50), (cx, cy + 2), r - 1)
        pygame.draw.circle(surf, (200, 40, 40), (cx, cy + 2), r - 1, 2)
        pygame.draw.circle(surf, (255, 100, 100), (cx - 3, cy - 2), r // 3)
        pygame.draw.line(surf, (100, 60, 30), (cx, cy - r + 4), (cx + 2, cy - r - 2), 2)
        pygame.draw.ellipse(surf, (80, 180, 60), (cx, cy - r - 2, 8, 5))
    else:  # cake
        pygame.draw.rect(surf, (240, 200, 160), (cx - r, cy - 2, r * 2, r + 4), border_radius=4)
        pygame.draw.rect(surf, (255, 120, 150), (cx - r, cy - 5, r * 2, 6), border_radius=3)
        pygame.draw.rect(surf, (220, 180, 140), (cx - r, cy - 2, r * 2, r + 4), 2, border_radius=4)
        pygame.draw.rect(surf, (255, 80, 80), (cx - 1, cy - 12, 2, 10))
        pygame.draw.circle(surf, (255, 200, 50), (cx, cy - 13), 3)
    return surf


def make_themed_bg(w, h, theme):
    """Create a themed background surface."""
    surf = pygame.Surface((w, h))
    if theme == THEME_FOREST:
        for y in range(h):
            t = y / h
            c = (int(100 + 60 * t), int(190 - 40 * t), int(120 + 40 * t))
            pygame.draw.line(surf, c, (0, y), (w, y))
        pygame.draw.rect(surf, (80, 160, 60), (0, h - 80, w, 80))
        # Trees
        for tx in range(50, w, 160):
            pygame.draw.rect(surf, (120, 80, 40), (tx - 8, h - 150, 16, 80))
            pygame.draw.polygon(surf, (40, 140, 50),
                                [(tx, h - 200), (tx - 40, h - 130), (tx + 40, h - 130)])
            pygame.draw.polygon(surf, (50, 160, 60),
                                [(tx, h - 230), (tx - 30, h - 170), (tx + 30, h - 170)])
    elif theme == THEME_SNOW:
        for y in range(h):
            t = y / h
            c = (int(180 + 50 * t), int(200 + 40 * t), int(230 + 20 * t))
            pygame.draw.line(surf, c, (0, y), (w, y))
        pygame.draw.rect(surf, (240, 245, 255), (0, h - 80, w, 80))
        # Snow mounds
        for sx in range(0, w + 80, 120):
            pygame.draw.circle(surf, (245, 248, 255), (sx, h - 65), 55)
        # Snowman
        pygame.draw.circle(surf, WHITE, (w - 100, h - 130), 22)
        pygame.draw.circle(surf, WHITE, (w - 100, h - 100), 28)
    elif theme == THEME_BEACH:
        for y in range(h):
            t = y / h
            c = (int(100 + 120 * t), int(180 + 50 * t), int(240 - 60 * t))
            pygame.draw.line(surf, c, (0, y), (w, y))
        pygame.draw.rect(surf, (230, 210, 160), (0, h - 80, w, 80))
        # Waves
        for wx in range(0, w + 40, 60):
            pygame.draw.arc(surf, (80, 180, 240), (wx, h - 100, 60, 30), 0, math.pi, 3)
        # Sun
        pygame.draw.circle(surf, (255, 220, 60), (w - 80, 60), 40)
    elif theme == THEME_SPACE:
        surf.fill((15, 10, 40))
        for _ in range(80):
            sx = random.randint(0, w)
            sy = random.randint(0, h - 80)
            sr = random.choice([1, 1, 1, 2])
            pygame.draw.circle(surf, (200 + random.randint(0, 55), 200 + random.randint(0, 55), 255), (sx, sy), sr)
        pygame.draw.circle(surf, (100, 60, 140), (150, 120), 30)
        pygame.draw.circle(surf, (120, 80, 160), (147, 115), 30)
        pygame.draw.circle(surf, (200, 140, 60), (w - 120, 180), 20)
        pygame.draw.rect(surf, (30, 20, 60), (0, h - 80, w, 80))
    else:  # THEME_CANDY
        for y in range(h):
            t = y / h
            c = (int(255 - 40 * t), int(150 + 60 * t), int(200 + 30 * t))
            pygame.draw.line(surf, c, (0, y), (w, y))
        pygame.draw.rect(surf, (255, 200, 220), (0, h - 80, w, 80))
        # Lollipops
        for lx in range(80, w, 200):
            pygame.draw.rect(surf, WHITE, (lx - 3, h - 160, 6, 90))
            pygame.draw.circle(surf, (255, 100, 150), (lx, h - 175), 22)
            pygame.draw.circle(surf, (255, 200, 100), (lx, h - 175), 14)
            pygame.draw.circle(surf, (100, 200, 255), (lx, h - 175), 7)
    # Clouds on all themes
    for cpos in [(120, 50), (380, 35), (650, 55), (820, 70)]:
        _draw_cloud(surf, cpos[0], cpos[1])
    return surf


# ---------------------------------------------------------------------------
# SOUND synthesis helpers  (simple WAV in memory)
# ---------------------------------------------------------------------------

def _synth_wav(freq: float, duration: float, volume: float = 0.35,
               sample_rate: int = 22050, wave_type: str = "sine") -> bytes:
    """Generate a short WAV in memory."""
    n_samples = int(sample_rate * duration)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        frames = bytearray()
        for i in range(n_samples):
            t = i / sample_rate
            # Envelope  -  fade in/out
            env = min(1.0, i / (sample_rate * 0.02)) * min(1.0, (n_samples - i) / (sample_rate * 0.05))
            if wave_type == "sine":
                val = math.sin(2 * math.pi * freq * t)
            elif wave_type == "square":
                val = 1.0 if math.sin(2 * math.pi * freq * t) >= 0 else -1.0
            else:
                val = math.sin(2 * math.pi * freq * t)
            sample = int(val * volume * env * 32767)
            sample = max(-32768, min(32767, sample))
            frames += struct.pack("<h", sample)
        wf.writeframes(bytes(frames))
    buf.seek(0)
    return buf.read()


def _make_correct_sound() -> pygame.mixer.Sound:
    """Happy ascending tone."""
    sr = 22050
    dur = 0.35
    n = int(sr * dur)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
        frames = bytearray()
        for i in range(n):
            t = i / sr
            env = min(1.0, i / (sr * 0.01)) * min(1.0, (n - i) / (sr * 0.08))
            freq = 523 + 400 * (t / dur)  # slide up
            val = math.sin(2 * math.pi * freq * t)
            frames += struct.pack("<h", int(val * 0.3 * env * 32767))
        wf.writeframes(bytes(frames))
    buf.seek(0)
    return pygame.mixer.Sound(buf)


def _make_wrong_sound() -> pygame.mixer.Sound:
    """Buzzy low tone."""
    data = _synth_wav(180, 0.25, 0.25, wave_type="square")
    return pygame.mixer.Sound(io.BytesIO(data))


def _make_win_sound() -> pygame.mixer.Sound:
    """Fanfare: three ascending notes."""
    sr = 22050
    notes = [523, 659, 784]
    note_dur = 0.18
    gap = 0.06
    total = len(notes) * (note_dur + gap)
    n_total = int(sr * total)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
        frames = bytearray()
        for i in range(n_total):
            t = i / sr
            idx = int(t / (note_dur + gap))
            local_t = t - idx * (note_dur + gap)
            if idx < len(notes) and local_t < note_dur:
                env = min(1.0, local_t / 0.01) * min(1.0, (note_dur - local_t) / 0.04)
                val = math.sin(2 * math.pi * notes[idx] * local_t)
                frames += struct.pack("<h", int(val * 0.35 * env * 32767))
            else:
                frames += struct.pack("<h", 0)
        wf.writeframes(bytes(frames))
    buf.seek(0)
    return pygame.mixer.Sound(buf)


def _make_click_sound() -> pygame.mixer.Sound:
    data = _synth_wav(800, 0.06, 0.2)
    return pygame.mixer.Sound(io.BytesIO(data))


def _make_bgm_loop() -> pygame.mixer.Sound:
    """Create a simple looping background melody."""
    sr = 22050
    melody_notes = [
        (392, 0.3), (440, 0.3), (494, 0.3), (523, 0.6),
        (494, 0.3), (440, 0.3), (392, 0.6),
        (330, 0.3), (349, 0.3), (392, 0.3), (440, 0.6),
        (392, 0.3), (349, 0.3), (330, 0.6),
    ]
    total_dur = sum(d for _, d in melody_notes) + 0.05 * len(melody_notes)
    n_total = int(sr * total_dur)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
        frames = bytearray()
        cursor = 0.0
        note_idx = 0
        for i in range(n_total):
            t = i / sr
            # find current note
            while note_idx < len(melody_notes):
                freq, nd = melody_notes[note_idx]
                if t < cursor + nd:
                    break
                cursor += nd + 0.05
                note_idx += 1
            if note_idx < len(melody_notes):
                freq, nd = melody_notes[note_idx]
                lt = t - cursor
                env = min(1.0, lt / 0.01) * min(1.0, (nd - lt) / 0.06)
                val = math.sin(2 * math.pi * freq * lt) * 0.12 * env
                # add soft harmonic
                val += math.sin(2 * math.pi * freq * 2 * lt) * 0.03 * env
                frames += struct.pack("<h", int(val * 32767))
            else:
                frames += struct.pack("<h", 0)
        wf.writeframes(bytes(frames))
    buf.seek(0)
    return pygame.mixer.Sound(buf)

def _make_bujiku_sound() -> pygame.mixer.Sound:
    """Bouncy 'bujiku bujiku' sound."""
    sr = 22050
    dur = 0.35
    n = int(sr * dur)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
        frames = bytearray()
        for i in range(n):
            t = i / sr
            env = min(1.0, i / (sr * 0.01)) * min(1.0, (n - i) / (sr * 0.05))
            freq = 300 + 200 * math.sin(t * 25)
            val = math.sin(2 * math.pi * freq * t) * 0.25 * env
            frames += struct.pack("<h", int(val * 32767))
        wf.writeframes(bytes(frames))
    buf.seek(0)
    return pygame.mixer.Sound(buf)


def _make_nomnom_sound() -> pygame.mixer.Sound:
    """Crunchy 'nom nom' eating sound."""
    sr = 22050
    dur = 0.3
    n = int(sr * dur)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
        frames = bytearray()
        for i in range(n):
            t = i / sr
            env = min(1.0, i / (sr * 0.005)) * min(1.0, (n - i) / (sr * 0.03))
            # Crunchy rapid modulation
            freq = 400 + 150 * math.sin(t * 60)
            val = math.sin(2 * math.pi * freq * t)
            val += 0.3 * math.sin(2 * math.pi * freq * 3 * t)
            val *= 0.2 * env
            frames += struct.pack("<h", max(-32768, min(32767, int(val * 32767))))
        wf.writeframes(bytes(frames))
    buf.seek(0)
    return pygame.mixer.Sound(buf)


# ---------------------------------------------------------------------------
# PARTICLES  -  sparkle/confetti
# ---------------------------------------------------------------------------

class Particle:
    __slots__ = ("x", "y", "vx", "vy", "color", "life", "size")

    def __init__(self, x, y, color=None):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, -1)
        self.color = color or random.choice([GOLD, RED, GREEN, BLUE, PINK, ORANGE, PURPLE])
        self.life = random.randint(20, 50)
        self.size = random.randint(3, 7)

    def update(self):
        self.x += self.vx
        self.vy += 0.12  # gravity
        self.y += self.vy
        self.life -= 1

    def draw(self, surf):
        if self.life > 0:
            alpha = max(0, min(255, int(255 * self.life / 30)))
            s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, alpha), (self.size, self.size), self.size)
            surf.blit(s, (int(self.x - self.size), int(self.y - self.size)))


# ---------------------------------------------------------------------------
# ANIMATED OPTION BUBBLE
# ---------------------------------------------------------------------------

class OptionBubble:
    def __init__(self, text: str, is_correct: bool, x: int, y: int, color: tuple, font: pygame.font.Font):
        self.text = text
        self.is_correct = is_correct
        self.base_x = x
        self.base_y = y
        self.x = float(x)
        self.y = float(y)
        self.color = color
        self.font = font
        self.size = OPTION_SIZE
        self.bob_offset = random.uniform(0, math.pi * 2)
        self.bob_speed = random.uniform(1.5, 2.5)
        self.rect = pygame.Rect(x, y, self.size, self.size)

    def update(self, ticks: float):
        self.y = self.base_y + math.sin(ticks * self.bob_speed + self.bob_offset) * 6
        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, surf: pygame.Surface):
        # rounded rect bubble
        r = self.rect.inflate(4, 4)
        pygame.draw.rect(surf, self.color, r, border_radius=18)
        # lighter inner
        inner = self.rect.inflate(-6, -6)
        lighter = tuple(min(255, c + 40) for c in self.color)
        pygame.draw.rect(surf, lighter, inner, border_radius=14)
        # border
        pygame.draw.rect(surf, DARK_GRAY, r, 3, border_radius=18)
        # text
        txt_surf = self.font.render(self.text, True, WHITE)
        tx = self.rect.centerx - txt_surf.get_width() // 2
        ty = self.rect.centery - txt_surf.get_height() // 2
        # shadow
        shadow = self.font.render(self.text, True, (0, 0, 0, 80))
        surf.blit(shadow, (tx + 2, ty + 2))
        surf.blit(txt_surf, (tx, ty))


# ---------------------------------------------------------------------------
# PLAYER
# ---------------------------------------------------------------------------

class Player:
    def __init__(self, sprite: pygame.Surface, x: int, y: int):
        self.sprite = sprite
        self.x = float(x)
        self.y = float(y)
        self.w = sprite.get_width()
        self.h = sprite.get_height()
        self.rect = pygame.Rect(x, y, self.w, self.h)
        self.speed = PLAYER_SPEED

    def update(self, keys, joystick=None):
        dx, dy = 0, 0

        # Keyboard input
        if keys[pygame.K_LEFT]:  dx -= self.speed
        if keys[pygame.K_RIGHT]: dx += self.speed
        if keys[pygame.K_UP]:    dy -= self.speed
        if keys[pygame.K_DOWN]:  dy += self.speed

        # Joystick / Gamepad input  (overrides if stick is pushed)
        if joystick is not None:
            try:
                axis_x = joystick.get_axis(0)  # left stick horizontal
                axis_y = joystick.get_axis(1)  # left stick vertical
                if abs(axis_x) > JOYSTICK_DEADZONE:
                    dx = axis_x * self.speed
                if abs(axis_y) > JOYSTICK_DEADZONE:
                    dy = axis_y * self.speed

                # D-pad / hat support
                if joystick.get_numhats() > 0:
                    hat_x, hat_y = joystick.get_hat(0)
                    if hat_x != 0:
                        dx = hat_x * self.speed
                    if hat_y != 0:
                        dy = -hat_y * self.speed  # hat Y is inverted
            except pygame.error:
                pass

        self.x = max(0, min(SCREEN_W - self.w, self.x + dx))
        self.y = max(80, min(SCREEN_H - self.h - 10, self.y + dy))
        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, surf: pygame.Surface):
        surf.blit(self.sprite, (int(self.x), int(self.y)))


# ---------------------------------------------------------------------------
# RUNNER ITEM  (word bubble or obstacle that scrolls down)
# ---------------------------------------------------------------------------

class RunnerItem:
    """A word or obstacle in the runner mode."""
    # Types
    TARGET = 0
    DISTRACTOR = 1
    OBSTACLE = 2

    def __init__(self, text: str, lane: int, y: float, item_type: int, font: pygame.font.Font):
        self.text = text
        self.lane = lane          # 0, 1, or 2
        self.y = y
        self.item_type = item_type
        self.font = font
        self.alive = True
        self.collected = False

        # visual sizing
        lane_left = (SCREEN_W - RUNNER_LANE_COUNT * RUNNER_LANE_WIDTH) // 2
        self.x = lane_left + lane * RUNNER_LANE_WIDTH + RUNNER_LANE_WIDTH // 2
        self.w = RUNNER_LANE_WIDTH - 20
        self.h = RUNNER_ITEM_H
        self.rect = pygame.Rect(self.x - self.w // 2, int(self.y), self.w, self.h)

    def update(self, speed: float):
        self.y += speed
        self.rect.topleft = (self.x - self.w // 2, int(self.y))

    def draw(self, surf: pygame.Surface, ticks: float):
        if not self.alive:
            return
        r = self.rect.copy()

        if self.item_type == RunnerItem.TARGET:
            # Green glowing bubble
            color = (60, 200, 100)
            lighter = (100, 230, 140)
            border_col = (40, 160, 70)
        elif self.item_type == RunnerItem.DISTRACTOR:
            # Orange/amber bubble
            color = (220, 160, 60)
            lighter = (240, 200, 100)
            border_col = (180, 120, 30)
        else:
            # Obstacle = spiky red block
            color = (200, 50, 50)
            lighter = (230, 80, 80)
            border_col = (150, 30, 30)

        # Draw rounded rect
        pygame.draw.rect(surf, color, r, border_radius=14)
        inner = r.inflate(-6, -6)
        pygame.draw.rect(surf, lighter, inner, border_radius=11)
        pygame.draw.rect(surf, border_col, r, 3, border_radius=14)

        if self.item_type == RunnerItem.OBSTACLE:
            # Draw X pattern on obstacle
            cx, cy = r.center
            sz = 14
            for dx, dy in [(-sz, -sz), (sz, sz), (-sz, sz), (sz, -sz)]:
                pygame.draw.line(surf, WHITE, (cx, cy), (cx + dx, cy + dy), 3)
            # Skull-like dots
            pygame.draw.circle(surf, WHITE, (cx - 8, cy - 4), 4)
            pygame.draw.circle(surf, WHITE, (cx + 8, cy - 4), 4)
            pygame.draw.circle(surf, border_col, (cx - 8, cy - 4), 2)
            pygame.draw.circle(surf, border_col, (cx + 8, cy - 4), 2)
        else:
            # Draw text on word bubble
            txt = self.font.render(self.text, True, WHITE)
            shadow = self.font.render(self.text, True, (0, 0, 0))
            tx = r.centerx - txt.get_width() // 2
            ty = r.centery - txt.get_height() // 2
            surf.blit(shadow, (tx + 1, ty + 1))
            surf.blit(txt, (tx, ty))

            # Small star icon for target words
            if self.item_type == RunnerItem.TARGET:
                bob = math.sin(ticks * 4 + self.lane) * 3
                pygame.draw.circle(surf, GOLD, (r.right - 12, r.top + 12 + int(bob)), 5)


# ---------------------------------------------------------------------------
# FALLING ANSWER  (Panda catch mode)
# ---------------------------------------------------------------------------

def make_word_image_surface(word, category, size=100):
    """Factory to create a procedural image or load from file for a given word."""
    # --- PHASE 1: STRICT ANIMAL LOADING ---
    if category == "Animals":
        img_path = ANIMAL_IMAGE_MAPPING.get(word)
        if img_path and os.path.exists(img_path):
            try:
                # Load with alpha, no generic background circle
                loaded_img = pygame.image.load(img_path).convert_alpha()
                return pygame.transform.smoothscale(loaded_img, (size, size))
            except Exception as e:
                print(f"[ERROR] Failed to load animal sprite '{img_path}': {e}")
        else:
            print(f"[ERROR] Animal asset MAPPING MISSING or FILE NOT FOUND: {word} -> {img_path}")
        
        # ERROR FALLBACK: Draw a 'Missing Asset' box instead of a generic circle
        err_surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(err_surf, (255, 0, 0, 100), (5, 5, size-10, size-10), border_radius=10)
        pygame.draw.rect(err_surf, (255, 0, 0), (5, 5, size-10, size-10), 3, border_radius=10)
        pygame.draw.line(err_surf, (255, 0, 0), (10, 10), (size-10, size-10), 2)
        pygame.draw.line(err_surf, (255, 0, 0), (size-10, 10), (10, size-10), 2)
        
        # Draw the word text so game is still playable while debugging missing assets
        try:
            temp_font = pygame.font.SysFont("Arial", 16, bold=True)
            txt = temp_font.render(word, True, (255, 0, 0))
            err_surf.blit(txt, (size//2 - txt.get_width()//2, size - 20))
        except: pass
        return err_surf

    # --- PHASE 2: Procedural drawing (Fallback for non-animal categories) ---
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    r = size // 2 - 5

    # Background circle/blob for all images to make them consistent
    pygame.draw.circle(surf, (255, 255, 255, 140), (cx, cy), r + 2)
    
    if category == "Colors":
        color_map = {
            "RED": (230, 70, 70), "BLUE": (80, 140, 240), "GREEN": (80, 200, 120),
            "YELLOW": (255, 230, 50), "PINK": (255, 150, 180), "ORANGE": (255, 160, 60),
            "PURPLE": (160, 100, 220), "WHITE": (250, 250, 250), "BLACK": (30, 30, 30),
            "BROWN": (130, 80, 40), "GRAY": (150, 150, 150), "GOLD": (255, 215, 0)
        }
        col = color_map.get(word, (200, 200, 200))
        # Draw a 'paint splash'
        for i in range(8):
            ang = i * (math.pi / 4)
            dist = r * 0.7
            pygame.draw.circle(surf, col, (cx + int(math.cos(ang)*dist), cy + int(math.sin(ang)*dist)), r // 2)
        pygame.draw.circle(surf, col, (cx, cy), int(r * 0.8))

    elif category == "Animals":
        # Draw a simplified animal face
        pygame.draw.circle(surf, (240, 230, 210), (cx, cy), r) # face base
        if word == "LION":
            # Mane
            pygame.draw.circle(surf, (220, 120, 30), (cx, cy), r + 4, 8)
            pygame.draw.circle(surf, (40, 40, 40), (cx - 15, cy - 8), 5) # eyes
            pygame.draw.circle(surf, (40, 40, 40), (cx + 15, cy - 8), 5)
            pygame.draw.polygon(surf, (40, 40, 40), [(cx, cy+5), (cx-5, cy-2), (cx+5, cy-2)]) # nose
        elif word == "CAT":
            # Ears
            pygame.draw.polygon(surf, (240, 230, 210), [(cx-25, cy-20), (cx-35, cy-40), (cx-15, cy-25)])
            pygame.draw.polygon(surf, (240, 230, 210), [(cx+25, cy-20), (cx+35, cy-40), (cx+15, cy-25)])
            pygame.draw.circle(surf, (40, 40, 40), (cx - 15, cy - 5), 4)
            pygame.draw.circle(surf, (40, 40, 40), (cx + 15, cy - 5), 4)
        elif word == "DOG":
            # Floppy ears
            pygame.draw.ellipse(surf, (130, 80, 40), (cx-r-2, cy-10, 20, 40))
            pygame.draw.ellipse(surf, (130, 80, 40), (cx+r-18, cy-10, 20, 40))
            pygame.draw.circle(surf, (40, 40, 40), (cx - 12, cy - 5), 5)
            pygame.draw.circle(surf, (40, 40, 40), (cx + 12, cy - 5), 5)
        elif word == "FISH":
            pygame.draw.circle(surf, (80, 180, 240), (cx, cy), r-5)
            pygame.draw.polygon(surf, (80, 180, 240), [(cx-r, cy), (cx-r-10, cy-15), (cx-r-10, cy+15)]) # tail
            pygame.draw.circle(surf, WHITE, (cx + 15, cy - 5), 5)
        elif word == "BIRD":
            pygame.draw.circle(surf, (255, 200, 50), (cx, cy), r-5)
            pygame.draw.polygon(surf, (255, 100, 50), [(cx+15, cy), (cx+25, cy-5), (cx+25, cy+5)]) # beak
            pygame.draw.circle(surf, (40, 40, 40), (cx + 5, cy - 5), 4)
        elif word == "FROG":
            pygame.draw.circle(surf, (100, 220, 80), (cx, cy), r-5)
            pygame.draw.circle(surf, (100, 220, 80), (cx-15, cy-r+10), 10) # eyes bump
            pygame.draw.circle(surf, (100, 220, 80), (cx+15, cy-r+10), 10)
            pygame.draw.circle(surf, (40, 40, 40), (cx-15, cy-r+10), 4)
            pygame.draw.circle(surf, (40, 40, 40), (cx+15, cy-r+10), 4)
        else:
            # Generic cute face for others
            pygame.draw.circle(surf, (40, 40, 40), (cx - 15, cy - 5), 4)
            pygame.draw.circle(surf, (40, 40, 40), (cx + 15, cy - 5), 4)
            pygame.draw.arc(surf, (40, 40, 40), (cx - 10, cy, 20, 15), 3.4, 6.0, 2)

    elif category == "Fruits":
        if word == "APPLE":
            pygame.draw.circle(surf, (220, 50, 50), (cx, cy + 5), r - 5)
            pygame.draw.rect(surf, (100, 60, 30), (cx - 3, cy - r, 6, 15)) # stem
        elif word == "BANANA":
            pygame.draw.arc(surf, (255, 230, 50), (cx - r, cy - r, size, size), 0.5, 2.5, 15)
        elif word == "GRAPE":
            for ox, oy in [(-10, -5), (10, -5), (0, 10), (-5, 5), (5, 5)]:
                pygame.draw.circle(surf, (160, 80, 200), (cx + ox, cy + oy), 12)
        else:
            pygame.draw.circle(surf, (255, 180, 50), (cx, cy + 5), r - 5) # Generic orange-ish

    elif category == "Numbers" or category == "Letters":
        # Draw inside a colorful block
        pygame.draw.rect(surf, random.choice(OPTION_COLORS), (5, 5, size-10, size-10), border_radius=15)
        pygame.draw.rect(surf, (0, 0, 0, 40), (5, 5, size-10, size-10), 3, border_radius=15)
        font = pygame.font.SysFont("Arial", 50, bold=True)
        txt = font.render(word, True, WHITE)
        surf.blit(txt, (cx - txt.get_width()//2, cy - txt.get_height()//2))

    elif category == "Shapes":
        # Draw the actual shape
        col = random.choice(OPTION_COLORS)
        if word == "CIRCLE": pygame.draw.circle(surf, col, (cx, cy), r)
        elif word == "SQUARE": pygame.draw.rect(surf, col, (cx-r, cy-r, r*2, r*2), border_radius=10)
        elif word == "STAR":
            stars_pts = []
            for i in range(10):
                ang = math.radians(-90 + i * 36)
                dist = r if i % 2 == 0 else r // 2
                stars_pts.append((cx + dist * math.cos(ang), cy + dist * math.sin(ang)))
            pygame.draw.polygon(surf, col, stars_pts)
        elif word == "HEART":
            pygame.draw.circle(surf, col, (cx - r//2, cy - r//4), r//2)
            pygame.draw.circle(surf, col, (cx + r//2, cy - r//4), r//2)
            pygame.draw.polygon(surf, col, [(cx - r, cy), (cx + r, cy), (cx, cy + r)])
        else:
             pygame.draw.circle(surf, col, (cx, cy), r)

    return surf


class FallingAnswer:
    """A visual learning item falling from the sky (image-based)."""
    def __init__(self, text, is_correct, x, y, color, font, speed, category):
        self.text = text
        self.is_correct = is_correct
        self.x = float(x)
        self.y = float(y)
        self.color = color
        self.font = font
        self.speed = speed
        self.category = category
        self.alive = True
        self.rect = pygame.Rect(int(x) - 50, int(y) - 50, 100, 100)
        self.bob_off = random.random() * 10
        self.hidden = False
        
        # Create the visual learning image
        self.image = make_word_image_surface(text, category, 100)

    def update(self):
        self.y += self.speed
        self.rect.center = (int(self.x), int(self.y))

    def draw(self, surf, ticks):
        r = self.rect.copy()
        bob = int(math.sin(ticks * 3 + self.bob_off) * 5)
        r.y += bob
        
        # Draw the pre-rendered image
        scaled_img = self.image
        if self.hidden:
            # Pulsing hidden effect
            alpha = 140 + int(math.sin(ticks * 5) * 60)
            scaled_img = self.image.copy()
            scaled_img.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
        
        surf.blit(scaled_img, r.topleft)


class FoodFlyAnim:
    """Animates a food item flying to the panda's mouth."""
    def __init__(self, sx, sy, tx, ty, food_type):
        self.sx, self.sy = float(sx), float(sy)
        self.tx, self.ty = float(tx), float(ty)
        self.food_type = food_type
        self.food_surf = make_food_surface(food_type, 40)
        self.t = 0.0  # 0..1 progress
        self.done = False

    def update(self):
        self.t += 0.04
        if self.t >= 1.0:
            self.t = 1.0
            self.done = True

    def draw(self, surf):
        # Ease-in-out
        ease = self.t * self.t * (3 - 2 * self.t)
        x = self.sx + (self.tx - self.sx) * ease
        y = self.sy + (self.ty - self.sy) * ease - math.sin(ease * math.pi) * 80
        # Scale down as it approaches mouth
        scale = 1.0 - ease * 0.4
        sz = max(8, int(40 * scale))
        scaled = pygame.transform.smoothscale(self.food_surf, (sz, sz))
        surf.blit(scaled, (int(x) - sz // 2, int(y) - sz // 2))


# ---------------------------------------------------------------------------
# GAME CLASS
# ---------------------------------------------------------------------------

class Game:
    # States
    MENU = 0
    PART_SELECT = 1
    PLAYING = 2
    LEVEL_TRANSITION = 3
    CELEBRATION = 4
    RUNNER_PLAYING = 5
    RUNNER_LEVEL_COMPLETE = 6
    RUNNER_GAME_OVER = 7
    PANDA_PLAYING = 8
    PANDA_LEVEL_COMPLETE = 9
    PANDA_GAME_OVER = 10

    # Part definitions
    PARTS = [
        {"name": "Part 1:  General Knowledge", "levels": LEVELS_PART1, "color": (80, 160, 255)},
        {"name": "Part 2:  Python Programming", "levels": LEVELS_PART2, "color": (100, 200, 120)},
        {"name": "Part 3:  Catch the Word", "levels": POOL_PART3, "color": (230, 130, 60)},
    ]

    def __init__(self):
        pygame.init()
        pygame.mixer.init(22050, -16, 1, 512)
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Smart Kids Adventure")
        self.clock = pygame.time.Clock()

        # Fonts
        self.font_big   = pygame.font.SysFont("Arial", 42, bold=True)
        self.font_med   = pygame.font.SysFont("Arial", 30, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 22, bold=True)
        self.font_option = pygame.font.SysFont("Arial", 26, bold=True)
        self.font_title = pygame.font.SysFont("Arial", 56, bold=True)
        self.font_huge  = pygame.font.SysFont("Arial", 68, bold=True)

        # Assets
        self.bg = make_gradient_bg(SCREEN_W, SCREEN_H)
        self.player_sprite = make_player_surface(64)
        self.star_img = make_star_surface(36)

        # Sounds
        self.snd_correct = _make_correct_sound()
        self.snd_wrong   = _make_wrong_sound()
        self.snd_win     = _make_win_sound()
        self.snd_click   = _make_click_sound()
        self.snd_bgm     = _make_bgm_loop()
        self.snd_bujiku  = _make_bujiku_sound()
        self.snd_nomnom  = _make_nomnom_sound()

        # State
        self.state = self.MENU
        self.level_idx = 0
        self.score = 0
        self.stars = 0
        self.shake_timer = 0
        self.shake_offset = (0, 0)
        self.transition_timer = 0
        self.particles: list[Particle] = []
        self.ticks = 0.0

        # Funny wrong-answer popup
        self.wrong_msg = ""
        self.wrong_msg_timer = 0       # frames remaining to show
        self.wrong_msg_color = RED

        # Part selection
        self.selected_part = 0      # index into PARTS
        self.current_levels = LEVELS_PART1

        # Player
        self.player = Player(self.player_sprite, SCREEN_W // 2 - 32, SCREEN_H - 140)

        # Options
        self.options: list[OptionBubble] = []

        # BGM
        self.bgm_channel = None

        # ---- Runner mode state ----
        self.runner_lane = 1               # 0=left, 1=center, 2=right
        self.runner_target_lane = 1        # for smooth animation
        self.runner_lane_anim = 0.0        # animation progress 0..1
        self.runner_items: list[RunnerItem] = []
        self.runner_targets: list[str] = []
        self.runner_collected: list[str] = []
        self.runner_level = 1
        self.runner_speed = 2.0
        self.runner_scroll_y = 0.0         # background scroll offset
        self.runner_spawn_timer = 0.0
        self.runner_score = 0
        self.runner_transition_timer = 0
        self.runner_total_levels = 5
        self.runner_joy_moved = False     # debounce flag for joystick axis

        # ---- Panda mode state ----
        self.panda_x = float(SCREEN_W // 2)
        self.panda_hearts = PANDA_MAX_HEARTS
        self.panda_combo = 0
        self.panda_max_combo = 0
        self.panda_growth = 0          # how much the panda has grown
        self.panda_expression = "happy"
        self.panda_expression_timer = 0
        self.panda_accessories: list[str] = []
        self.panda_falling: list[FallingAnswer] = []
        self.panda_food_anims: list[FoodFlyAnim] = []
        self.panda_level = 1
        self.panda_total_levels = 10
        self.panda_score = 0
        self.panda_transition_timer = 0
        self.panda_current_levels: list = []
        self.panda_q_idx = 0
        self.panda_level_correct_count = 0  # how many caught in current level
        self.panda_spawn_queue = []         # sequential words to spawn
        self.panda_spawn_delay_timer = 0    # delay after catch/miss
        self.panda_theme_bg: pygame.Surface | None = None
        self.panda_powerup = None      # None, "slowmo", "double"
        self.panda_powerup_timer = 0
        self.panda_y_offset = 0.0      # for jumping
        self.panda_vy = 0.0
        self.panda_run_frame = 0.0     # for running animation
        self.panda_clouds: list[list] = [[x, random.randint(20, 100), random.uniform(0.3, 0.8)]
                                          for x in range(0, SCREEN_W + 200, 220)]
        # Category-based level data for panda game
        self.panda_level_data: dict = {}        # from get_panda_level_data()
        self.panda_correct_requeue: bool = False  # True if correct word must be re-inserted next round
        # Visual feedback extras
        self.panda_score_popups: list = []      # [(text, x, y, life, color), ...]
        self.panda_wrong_flash_timer: int = 0   # frames to flash red
        self.panda_heart_pulse: int = 0         # frames to pulse hearts on loss
        self.panda_distractors_spawned: int = 0 # To guarantee correct word spawning
        self.panda_last_caught_word: str = ""   # To avoid immediate re-spawn distractors

        # Joystick / Gamepad
        self.joystick = None
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Joystick connected: {self.joystick.get_name()}")

    # ----- level loading ---------------------------------------------------

    def _load_level(self):
        self.options.clear()
        lvl = self.current_levels[self.level_idx]
        positions = self._random_positions(len(lvl["options"]))
        for i, opt_text in enumerate(lvl["options"]):
            color = OPTION_COLORS[i % len(OPTION_COLORS)]
            is_correct = (opt_text == lvl["correct"])
            bub = OptionBubble(opt_text, is_correct, positions[i][0], positions[i][1], color, self.font_option)
            self.options.append(bub)
        # Reset player position  (bottom center)
        self.player.x = SCREEN_W // 2 - 32
        self.player.y = SCREEN_H - 140

    @staticmethod
    def _random_positions(count: int) -> list[tuple[int, int]]:
        """Generate non-overlapping positions in the play area."""
        margin = 60
        play_top = 120
        play_bot = SCREEN_H - 180
        play_left = margin
        play_right = SCREEN_W - margin - OPTION_SIZE
        positions = []
        for _ in range(count):
            for _attempt in range(200):
                x = random.randint(play_left, play_right)
                y = random.randint(play_top, play_bot)
                ok = True
                for px, py in positions:
                    if abs(x - px) < OPTION_SIZE + 20 and abs(y - py) < OPTION_SIZE + 20:
                        ok = False
                        break
                if ok:
                    positions.append((x, y))
                    break
            else:
                positions.append((random.randint(play_left, play_right),
                                  random.randint(play_top, play_bot)))
        return positions

    # ----- main loop -------------------------------------------------------

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            self.ticks += dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    self._handle_keydown(event.key)
                # Joystick button press  (button 0 = A/X, button 1 = B/O)
                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button in (0, 1):
                        self._handle_keydown(pygame.K_RETURN)
                # Joystick hat (D-pad) for runner lane switching
                elif event.type == pygame.JOYHATMOTION:
                    if self.state == self.RUNNER_PLAYING:
                        hat_x, hat_y = event.value
                        if hat_x < 0:
                            self._handle_keydown(pygame.K_LEFT)
                        elif hat_x > 0:
                            self._handle_keydown(pygame.K_RIGHT)
                    elif self.state == self.PART_SELECT:
                        hat_x, hat_y = event.value
                        if hat_y > 0:
                            self._handle_keydown(pygame.K_UP)
                        elif hat_y < 0:
                            self._handle_keydown(pygame.K_DOWN)
                # Joystick axis for runner lane switching (with debounce)
                elif event.type == pygame.JOYAXISMOTION:
                    if self.state == self.RUNNER_PLAYING and event.axis == 0:
                        if event.value < -0.5 and not self.runner_joy_moved:
                            self.runner_joy_moved = True
                            self._handle_keydown(pygame.K_LEFT)
                        elif event.value > 0.5 and not self.runner_joy_moved:
                            self.runner_joy_moved = True
                            self._handle_keydown(pygame.K_RIGHT)
                        elif abs(event.value) < 0.3:
                            self.runner_joy_moved = False  # stick returned to center
                # Hot-plug: joystick connected
                elif event.type == pygame.JOYDEVICEADDED:
                    if self.joystick is None:
                        pygame.joystick.init()
                        if pygame.joystick.get_count() > 0:
                            self.joystick = pygame.joystick.Joystick(0)
                            self.joystick.init()
                            print(f"Joystick connected: {self.joystick.get_name()}")
                elif event.type == pygame.JOYDEVICEREMOVED:
                    self.joystick = None
                    print("Joystick disconnected")

            keys = pygame.key.get_pressed()
            self._update(keys, dt)
            self._draw()
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    # ----- event handling --------------------------------------------------

    def _handle_keydown(self, key):
        if self.state == self.MENU:
            if key in (pygame.K_RETURN, pygame.K_SPACE):
                self.snd_click.play()
                self.state = self.PART_SELECT
                self.selected_part = 0

        elif self.state == self.PART_SELECT:
            if key == pygame.K_UP:
                self.snd_click.play()
                self.selected_part = (self.selected_part - 1) % len(self.PARTS)
            elif key == pygame.K_DOWN:
                self.snd_click.play()
                self.selected_part = (self.selected_part + 1) % len(self.PARTS)
            elif key in (pygame.K_RETURN, pygame.K_SPACE):
                self.snd_click.play()
                if self.selected_part == 0:
                    # Part 1 — Panda mode
                    self._start_panda()
                elif self.selected_part == 2:
                    # Part 3 — Runner mode
                    self._start_runner()
                else:
                    self.current_levels = get_random_levels(self.selected_part)
                    self.state = self.PLAYING
                    self.level_idx = 0
                    self.score = 0
                    self.stars = 0
                    self._load_level()
                    self._start_bgm()
            elif key == pygame.K_ESCAPE:
                self.state = self.MENU

        elif self.state == self.CELEBRATION:
            if key in (pygame.K_RETURN, pygame.K_SPACE):
                self.state = self.MENU
                self._stop_bgm()

        elif self.state == self.RUNNER_PLAYING:
            if key == pygame.K_LEFT:
                if self.runner_lane > 0:
                    self.snd_click.play()
                    self.runner_lane -= 1
            elif key == pygame.K_RIGHT:
                if self.runner_lane < RUNNER_LANE_COUNT - 1:
                    self.snd_click.play()
                    self.runner_lane += 1

        elif self.state == self.RUNNER_GAME_OVER:
            if key in (pygame.K_RETURN, pygame.K_SPACE):
                self.snd_click.play()
                self._start_runner_level()  # retry same level
            elif key == pygame.K_ESCAPE:
                self.state = self.MENU
                self._stop_bgm()

        elif self.state == self.RUNNER_LEVEL_COMPLETE:
            if key in (pygame.K_RETURN, pygame.K_SPACE):
                self.snd_click.play()
                if self.runner_level >= self.runner_total_levels:
                    # All levels done — celebration!
                    self.state = self.CELEBRATION
                    self.score = self.runner_score
                    self.stars = self.runner_level
                    self.snd_win.play()
                    self._stop_bgm()
                    for _ in range(120):
                        self.particles.append(Particle(SCREEN_W // 2, SCREEN_H // 2))
                else:
                    self.runner_level += 1
                    self._start_runner_level()

        elif self.state == self.PANDA_PLAYING:
            if key == pygame.K_LEFT:
                self.snd_bujiku.play()
            elif key == pygame.K_RIGHT:
                self.snd_bujiku.play()

        elif self.state == self.PANDA_GAME_OVER:
            if key in (pygame.K_RETURN, pygame.K_SPACE):
                self.snd_click.play()
                self._start_panda()  # restart game
            elif key == pygame.K_ESCAPE:
                self.state = self.MENU
                self._stop_bgm()

        elif self.state == self.PANDA_LEVEL_COMPLETE:
            if key in (pygame.K_RETURN, pygame.K_SPACE):
                self.snd_click.play()
                if self.panda_level >= self.panda_total_levels:
                    self.state = self.CELEBRATION
                    self.score = self.panda_score
                    self.stars = self.panda_level
                    self.snd_win.play()
                    self._stop_bgm()
                    for _ in range(120):
                        self.particles.append(Particle(SCREEN_W // 2, SCREEN_H // 2))
                else:
                    self.panda_level += 1
                    self._start_panda_level()

    # ----- update ----------------------------------------------------------

    def _update(self, keys, dt):
        # particles always update
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.life > 0]

        # Funny message timer  (always ticks, even between states)
        if self.wrong_msg_timer > 0:
            self.wrong_msg_timer -= 1

        if self.state == self.PLAYING:
            self.player.update(keys, self.joystick)
            for opt in self.options:
                opt.update(self.ticks)

            # shake decay
            if self.shake_timer > 0:
                self.shake_timer -= 1
                self.shake_offset = (random.randint(-4, 4), random.randint(-4, 4))
            else:
                self.shake_offset = (0, 0)

            # collision
            for opt in self.options:
                if self.player.rect.colliderect(opt.rect):
                    if opt.is_correct:
                        self._on_correct(opt)
                    else:
                        self._on_wrong()
                    break

        elif self.state == self.LEVEL_TRANSITION:
            self.transition_timer -= 1
            if self.transition_timer <= 0:
                if self.level_idx >= len(self.current_levels):
                    self.state = self.CELEBRATION
                    self.snd_win.play()
                    self._stop_bgm()
                    # explosion of particles
                    for _ in range(120):
                        self.particles.append(Particle(SCREEN_W // 2, SCREEN_H // 2))
                else:
                    self.state = self.PLAYING
                    self._load_level()

        elif self.state == self.RUNNER_PLAYING:
            self._update_runner(dt)

        elif self.state == self.RUNNER_LEVEL_COMPLETE:
            self.runner_transition_timer -= 1
            # continuous sparkles
            if random.random() < 0.15:
                self.particles.append(Particle(random.randint(0, SCREEN_W), -10))

        elif self.state == self.CELEBRATION:
            # continuous confetti
            if random.random() < 0.3:
                self.particles.append(Particle(random.randint(0, SCREEN_W), -10))

        elif self.state == self.PANDA_PLAYING:
            self._update_panda(dt)

        elif self.state == self.PANDA_LEVEL_COMPLETE:
            self.panda_transition_timer -= 1
            if random.random() < 0.2:
                self.particles.append(Particle(random.randint(0, SCREEN_W), -10))

    def _on_correct(self, opt: OptionBubble):
        self.snd_correct.play()
        self.score += 10
        self.stars += 1
        # particles at option
        for _ in range(20):
            self.particles.append(Particle(opt.rect.centerx, opt.rect.centery))
        self.level_idx += 1
        self.state = self.LEVEL_TRANSITION
        self.transition_timer = 50  # ~0.8s

    def _on_wrong(self):
        if self.shake_timer <= 0:
            self.snd_wrong.play()
            self.shake_timer = 15
            # Push player back slightly
            self.player.y = min(SCREEN_H - self.player.h - 10, self.player.y + 30)
            # Pick a random funny message
            self.wrong_msg = random.choice(WRONG_MESSAGES)
            self.wrong_msg_timer = 80   # ~1.3 seconds at 60fps
            self.wrong_msg_color = random.choice([
                (230, 70, 70), (220, 120, 50), (200, 60, 180),
                (180, 80, 220), (60, 160, 200), (200, 50, 100),
            ])

    # ----- drawing ---------------------------------------------------------

    def _draw(self):
        ox, oy = self.shake_offset
        self.screen.blit(self.bg, (ox, oy))

        if self.state == self.MENU:
            self._draw_menu()
        elif self.state == self.PART_SELECT:
            self._draw_part_select()
        elif self.state == self.PLAYING:
            self._draw_gameplay()
        elif self.state == self.LEVEL_TRANSITION:
            self._draw_transition()
        elif self.state == self.RUNNER_PLAYING:
            self._draw_runner()
        elif self.state == self.RUNNER_LEVEL_COMPLETE:
            self._draw_runner_level_complete()
        elif self.state == self.RUNNER_GAME_OVER:
            self._draw_runner_game_over()
        elif self.state == self.CELEBRATION:
            self._draw_celebration()
        elif self.state == self.PANDA_PLAYING:
            self._draw_panda()
        elif self.state == self.PANDA_LEVEL_COMPLETE:
            self._draw_panda_level_complete()
        elif self.state == self.PANDA_GAME_OVER:
            self._draw_panda_game_over()

        # particles on top
        for p in self.particles:
            p.draw(self.screen)

        # Funny wrong-answer popup  (drawn on top of everything)
        if self.wrong_msg_timer > 0:
            self._draw_wrong_popup()

    def _draw_wrong_popup(self):
        """Draw a big funny popup when wrong answer is touched."""
        # Animation progress  (1.0 = just appeared, 0.0 = about to disappear)
        t = self.wrong_msg_timer / 80.0

        # Bouncy scale: pop in then settle
        if t > 0.85:
            scale = 1.0 + 0.4 * math.sin((1.0 - t) / 0.15 * math.pi)
        else:
            scale = 1.0

        # Wobble rotation simulation via horizontal offset
        wobble_x = int(math.sin(self.ticks * 12) * 6 * t)

        # Font size
        font_size = max(16, int(48 * scale))
        font = pygame.font.SysFont("Arial", font_size, bold=True)

        # Render text
        txt = font.render(self.wrong_msg, True, WHITE)
        tw, th = txt.get_size()

        # Background bubble
        pad_x, pad_y = 36, 24
        bw, bh = tw + pad_x * 2, th + pad_y * 2
        bx = SCREEN_W // 2 - bw // 2 + wobble_x
        by = SCREEN_H // 2 - bh // 2 - 40

        alpha = max(0, min(255, int(255 * min(1.0, t * 3))))
        bubble = pygame.Surface((bw, bh), pygame.SRCALPHA)
        col = (*self.wrong_msg_color, alpha)
        pygame.draw.rect(bubble, col, (0, 0, bw, bh), border_radius=22)
        # lighter inner
        inner_col = tuple(min(255, c + 50) for c in self.wrong_msg_color) + (alpha,)
        pygame.draw.rect(bubble, inner_col, (6, 6, bw - 12, bh - 12), border_radius=18)
        # border
        pygame.draw.rect(bubble, (255, 255, 255, alpha), (0, 0, bw, bh), 4, border_radius=22)
        self.screen.blit(bubble, (bx, by))

        # Text  (centered in bubble)
        txt.set_alpha(alpha)
        self.screen.blit(txt, (bx + pad_x, by + pad_y))

        # Funny face emoji below the bubble
        face_font = pygame.font.SysFont("Segoe UI Emoji", 40)
        faces = ["😜", "🙈", "😂", "🤪", "😅", "🫣", "😬", "🤭"]
        face_char = faces[hash(self.wrong_msg) % len(faces)]
        face_surf = face_font.render(face_char, True, WHITE)
        face_surf.set_alpha(alpha)
        self.screen.blit(face_surf, (SCREEN_W // 2 - face_surf.get_width() // 2 + wobble_x,
                                      by + bh + 8))

    def _draw_menu(self):
        # Title
        title = self.font_title.render("Smart Kids Adventure", True, (50, 80, 160))
        shadow = self.font_title.render("Smart Kids Adventure", True, (30, 50, 100))
        tx = SCREEN_W // 2 - title.get_width() // 2
        self.screen.blit(shadow, (tx + 3, 123))
        self.screen.blit(title, (tx, 120))

        # Subtitle
        sub = self.font_med.render("A fun learning game for kids!", True, (100, 100, 140))
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 200))

        # Character
        big_char = pygame.transform.smoothscale(self.player_sprite, (128, 128))
        self.screen.blit(big_char, (SCREEN_W // 2 - 64, 260))

        # Stars decoration
        for i in range(5):
            x = SCREEN_W // 2 - 100 + i * 50
            bob = math.sin(self.ticks * 2 + i) * 5
            self.screen.blit(self.star_img, (x, 410 + bob))

        # Prompt
        pulse = int(180 + 75 * math.sin(self.ticks * 3))
        prompt = self.font_med.render("Press ENTER or SPACE to Start!", True, (pulse, 80, 80))
        self.screen.blit(prompt, (SCREEN_W // 2 - prompt.get_width() // 2, 480))

        # controls hint
        hint = self.font_small.render("Arrow Keys / Joystick to move  |  ESC to quit", True, DARK_GRAY)
        self.screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, 540))

    def _draw_part_select(self):
        """Draw the Part selection screen."""
        # Title
        title = self.font_title.render("Choose a Part", True, (50, 80, 160))
        shadow = self.font_title.render("Choose a Part", True, (30, 50, 100))
        tx = SCREEN_W // 2 - title.get_width() // 2
        self.screen.blit(shadow, (tx + 3, 83))
        self.screen.blit(title, (tx, 80))

        # Part buttons
        for i, part in enumerate(self.PARTS):
            y = 220 + i * 120
            is_selected = (i == self.selected_part)

            # Box
            box_w, box_h = 500, 90
            bx = SCREEN_W // 2 - box_w // 2
            box_rect = pygame.Rect(bx, y, box_w, box_h)

            if is_selected:
                # Glowing border
                glow = pygame.Rect(bx - 4, y - 4, box_w + 8, box_h + 8)
                pulse_alpha = int(180 + 75 * math.sin(self.ticks * 4))
                glow_col = (*part["color"], pulse_alpha)
                gs = pygame.Surface((box_w + 8, box_h + 8), pygame.SRCALPHA)
                pygame.draw.rect(gs, glow_col, (0, 0, box_w + 8, box_h + 8), border_radius=18)
                self.screen.blit(gs, (bx - 4, y - 4))
                bg_col = part["color"]
            else:
                bg_col = GRAY

            pygame.draw.rect(self.screen, bg_col, box_rect, border_radius=14)
            lighter = tuple(min(255, c + 50) for c in bg_col)
            pygame.draw.rect(self.screen, lighter, box_rect.inflate(-8, -8), border_radius=12)
            pygame.draw.rect(self.screen, DARK_GRAY, box_rect, 3, border_radius=14)

            # Part name
            name_surf = self.font_med.render(part["name"], True, WHITE if is_selected else DARK_GRAY)
            self.screen.blit(name_surf, (box_rect.centerx - name_surf.get_width() // 2,
                                          box_rect.y + 12))
            # Level count
            count_txt = f"{len(part['levels'])} Levels"
            count_surf = self.font_small.render(count_txt, True, WHITE if is_selected else DARK_GRAY)
            self.screen.blit(count_surf, (box_rect.centerx - count_surf.get_width() // 2,
                                           box_rect.y + 52))

            # Arrow indicator
            if is_selected:
                arrow = self.font_med.render("▶", True, WHITE)
                self.screen.blit(arrow, (bx - 40, y + 25))

        # Hint
        hint = self.font_small.render("↑↓  to select  |  ENTER to play  |  ESC back", True, DARK_GRAY)
        self.screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, SCREEN_H - 60))

    def _draw_gameplay(self):
        lvl = self.current_levels[self.level_idx]

        # HUD bar
        hud_rect = pygame.Rect(0, 0, SCREEN_W, 80)
        hud_surf = pygame.Surface((SCREEN_W, 80), pygame.SRCALPHA)
        pygame.draw.rect(hud_surf, (255, 255, 255, 180), hud_rect, border_radius=0)
        self.screen.blit(hud_surf, (0, 0))

        # Part label + Level number
        part_label = self.PARTS[self.selected_part]["name"]
        lvl_txt = self.font_small.render(f"{part_label}  —  Level {self.level_idx + 1} / {len(self.current_levels)}", True, DARK_GRAY)
        self.screen.blit(lvl_txt, (20, 10))

        # Question
        q_txt = self.font_big.render(lvl["question"], True, (50, 50, 120))
        q_shadow = self.font_big.render(lvl["question"], True, (30, 30, 80))
        qx = SCREEN_W // 2 - q_txt.get_width() // 2
        self.screen.blit(q_shadow, (qx + 2, 34))
        self.screen.blit(q_txt, (qx, 32))

        # Score + Stars
        score_txt = self.font_med.render(f"Score: {self.score}", True, (60, 60, 60))
        self.screen.blit(score_txt, (SCREEN_W - score_txt.get_width() - 80, 10))
        # stars
        for i in range(self.stars):
            sx = SCREEN_W - 70 + (i % 5) * 0  # stack on same pos
            # draw small stars next to score
        star_row_x = SCREEN_W - 60
        star_row_y = 48
        for i in range(min(self.stars, 10)):
            tiny_star = pygame.transform.smoothscale(self.star_img, (22, 22))
            self.screen.blit(tiny_star, (star_row_x - i * 24, star_row_y))

        # Options
        for opt in self.options:
            opt.draw(self.screen)

        # Player
        self.player.draw(self.screen)

        # Instruction
        inst = self.font_small.render("Move to the correct answer!", True, (100, 100, 100))
        self.screen.blit(inst, (SCREEN_W // 2 - inst.get_width() // 2, SCREEN_H - 40))

    def _draw_transition(self):
        # "Correct!" text
        pulse = 1.0 + 0.15 * math.sin(self.ticks * 8)
        size = int(52 * pulse)
        font = pygame.font.SysFont("Arial", size, bold=True)
        txt = font.render("Correct! ★", True, GOLD)
        shadow = font.render("Correct! ★", True, (160, 120, 0))
        cx = SCREEN_W // 2 - txt.get_width() // 2
        cy = SCREEN_H // 2 - txt.get_height() // 2
        self.screen.blit(shadow, (cx + 3, cy + 3))
        self.screen.blit(txt, (cx, cy))

        # Score
        sc = self.font_med.render(f"Score: {self.score}", True, DARK_GRAY)
        self.screen.blit(sc, (SCREEN_W // 2 - sc.get_width() // 2, cy + 70))

    def _draw_celebration(self):
        # Big congrats
        line1 = self.font_huge.render("Congratulations!", True, GOLD)
        shadow1 = self.font_huge.render("Congratulations!", True, (180, 140, 0))
        x1 = SCREEN_W // 2 - line1.get_width() // 2
        self.screen.blit(shadow1, (x1 + 3, 103))
        self.screen.blit(line1, (x1, 100))

        line2 = self.font_title.render("You Won!", True, (80, 160, 80))
        x2 = SCREEN_W // 2 - line2.get_width() // 2
        self.screen.blit(line2, (x2, 190))

        # Big character
        big_char = pygame.transform.smoothscale(self.player_sprite, (160, 160))
        self.screen.blit(big_char, (SCREEN_W // 2 - 80, 260))

        # Stars earned
        earned = self.font_med.render(f"Stars Earned: {self.stars}  |  Score: {self.score}", True, DARK_GRAY)
        self.screen.blit(earned, (SCREEN_W // 2 - earned.get_width() // 2, 440))

        # twinkling stars
        for i in range(self.stars):
            angle = self.ticks * 2 + i * 0.8
            sx = SCREEN_W // 2 + int(math.cos(angle) * (100 + i * 15))
            sy = 350 + int(math.sin(angle) * 30)
            self.screen.blit(self.star_img, (sx - 18, sy - 18))

        # Prompt
        pulse = int(180 + 75 * math.sin(self.ticks * 3))
        prompt = self.font_med.render("Press ENTER to Play Again!", True, (pulse, 60, 60))
        self.screen.blit(prompt, (SCREEN_W // 2 - prompt.get_width() // 2, 520))

    # ----- BGM control -----------------------------------------------------

    def _start_bgm(self):
        if self.bgm_channel is None or not self.bgm_channel.get_busy():
            self.bgm_channel = self.snd_bgm.play(loops=-1)
            if self.bgm_channel:
                self.bgm_channel.set_volume(0.25)

    def _stop_bgm(self):
        if self.bgm_channel:
            self.bgm_channel.stop()
            self.bgm_channel = None

    # ===================================================================
    # RUNNER MODE  — Subway-surfer style  "Catch the Word"
    # ===================================================================

    def _start_runner(self):
        """Initialize the runner mode from Part Select."""
        self.runner_level = 1
        self.runner_score = 0
        self._start_runner_level()
        self._start_bgm()

    def _start_runner_level(self):
        """Set up a single runner level."""
        self.state = self.RUNNER_PLAYING
        self.runner_lane = 1
        self.runner_target_lane = 1
        self.runner_items.clear()
        self.runner_targets = get_runner_level(self.runner_level)
        self.runner_collected = []
        self.runner_speed = RUNNER_SPEEDS.get(self.runner_level, 3.0)
        self.runner_scroll_y = 0.0
        self.runner_spawn_timer = 0.0
        self.shake_timer = 0
        self.shake_offset = (0, 0)
        self.wrong_msg_timer = 0
        # Pre-schedule all target words so they definitely appear
        self._runner_schedule_targets()

    def _runner_schedule_targets(self):
        """Pre-spawn target words at staggered positions above the screen."""
        spacing = 220  # vertical gap between scheduled items
        start_y = -300
        available_lanes = list(range(RUNNER_LANE_COUNT))
        for i, word in enumerate(self.runner_targets):
            lane = random.choice(available_lanes)
            y = start_y - i * spacing
            item = RunnerItem(word, lane, y, RunnerItem.TARGET, self.font_option)
            self.runner_items.append(item)

    def _update_runner(self, dt):
        """Tick the runner gameplay."""
        # Scroll background
        self.runner_scroll_y += self.runner_speed
        if self.runner_scroll_y >= 40:
            self.runner_scroll_y -= 40

        # Move existing items down
        for item in self.runner_items:
            item.update(self.runner_speed)

        # Randomly spawn obstacles and distractors
        obs_rate = RUNNER_OBSTACLE_RATES.get(self.runner_level, 0.015)
        if random.random() < obs_rate:
            lane = random.randint(0, RUNNER_LANE_COUNT - 1)
            # Don't spawn on top of another item that's close
            ok = True
            for it in self.runner_items:
                if it.lane == lane and it.y < 0 and it.y > -100:
                    ok = False
                    break
            if ok:
                item = RunnerItem("X", lane, -RUNNER_ITEM_H - 20, RunnerItem.OBSTACLE, self.font_option)
                self.runner_items.append(item)

        if random.random() < RUNNER_DISTRACTOR_RATE:
            lane = random.randint(0, RUNNER_LANE_COUNT - 1)
            # Pick a word NOT in target list
            non_targets = [w for w in POOL_PART3 if w not in self.runner_targets]
            if non_targets:
                word = random.choice(non_targets)
                ok = True
                for it in self.runner_items:
                    if it.lane == lane and it.y < 0 and it.y > -100:
                        ok = False
                        break
                if ok:
                    item = RunnerItem(word, lane, -RUNNER_ITEM_H - 20, RunnerItem.DISTRACTOR, self.font_option)
                    self.runner_items.append(item)

        # Player rect for collision
        lane_left = (SCREEN_W - RUNNER_LANE_COUNT * RUNNER_LANE_WIDTH) // 2
        player_cx = lane_left + self.runner_lane * RUNNER_LANE_WIDTH + RUNNER_LANE_WIDTH // 2
        player_rect = pygame.Rect(player_cx - 30, RUNNER_PLAYER_Y, 60, 60)

        # Check collisions
        for item in self.runner_items:
            if not item.alive:
                continue
            if player_rect.colliderect(item.rect):
                if item.item_type == RunnerItem.OBSTACLE:
                    # GAME OVER
                    item.alive = False
                    self.snd_wrong.play()
                    self.state = self.RUNNER_GAME_OVER
                    self.shake_timer = 20
                    for _ in range(30):
                        self.particles.append(Particle(player_cx, RUNNER_PLAYER_Y))
                    return
                elif item.item_type == RunnerItem.TARGET:
                    # Collected target word!
                    item.alive = False
                    self.snd_correct.play()
                    self.runner_collected.append(item.text)
                    self.runner_score += 10
                    for _ in range(15):
                        self.particles.append(Particle(item.rect.centerx, item.rect.centery))
                elif item.item_type == RunnerItem.DISTRACTOR:
                    # Wrong word — just shake, no game over
                    item.alive = False
                    self.snd_wrong.play()
                    self.shake_timer = 10
                    self.wrong_msg = random.choice(WRONG_MESSAGES)
                    self.wrong_msg_timer = 60
                    self.wrong_msg_color = random.choice([
                        (230, 70, 70), (220, 120, 50), (200, 60, 180),
                    ])

        # Remove items that fell off screen
        self.runner_items = [it for it in self.runner_items if it.y < SCREEN_H + 50 and it.alive]

        # Check win condition: all targets collected
        if len(self.runner_collected) >= len(self.runner_targets):
            self.state = self.RUNNER_LEVEL_COMPLETE
            self.runner_transition_timer = 90
            self.snd_win.play()
            for _ in range(40):
                self.particles.append(Particle(SCREEN_W // 2, SCREEN_H // 2))

        # Shake decay
        if self.shake_timer > 0:
            self.shake_timer -= 1
            self.shake_offset = (random.randint(-4, 4), random.randint(-4, 4))
        else:
            self.shake_offset = (0, 0)

    # ----- Runner drawing ---------------------------------------------------

    def _draw_runner_road(self):
        """Draw the 3-lane road / track background."""
        lane_left = (SCREEN_W - RUNNER_LANE_COUNT * RUNNER_LANE_WIDTH) // 2
        total_w = RUNNER_LANE_COUNT * RUNNER_LANE_WIDTH

        # Dark road surface
        road_rect = pygame.Rect(lane_left - 10, 0, total_w + 20, SCREEN_H)
        pygame.draw.rect(self.screen, (60, 60, 70), road_rect, border_radius=0)

        # Lane dividers (dashed white lines, scrolling)
        for i in range(1, RUNNER_LANE_COUNT):
            x = lane_left + i * RUNNER_LANE_WIDTH
            dash_len = 30
            gap_len = 20
            offset = int(self.runner_scroll_y) % (dash_len + gap_len)
            y = -offset
            while y < SCREEN_H:
                y1 = max(0, y)
                y2 = min(SCREEN_H, y + dash_len)
                if y2 > y1:
                    pygame.draw.line(self.screen, (200, 200, 200), (x, y1), (x, y2), 3)
                y += dash_len + gap_len

        # Side stripes (orange/white alternating)
        stripe_h = 40
        stripe_offset = int(self.runner_scroll_y) % (stripe_h * 2)
        for side_x in [lane_left - 10, lane_left + total_w]:
            y = -stripe_offset
            idx = 0
            while y < SCREEN_H:
                col = (255, 160, 40) if idx % 2 == 0 else WHITE
                r = pygame.Rect(side_x, y, 10, stripe_h)
                pygame.draw.rect(self.screen, col, r)
                y += stripe_h
                idx += 1

    def _draw_runner_player(self):
        """Draw the player character in its lane."""
        lane_left = (SCREEN_W - RUNNER_LANE_COUNT * RUNNER_LANE_WIDTH) // 2
        player_cx = lane_left + self.runner_lane * RUNNER_LANE_WIDTH + RUNNER_LANE_WIDTH // 2

        # Draw the player sprite centered in the lane
        px = player_cx - self.player_sprite.get_width() // 2
        py = RUNNER_PLAYER_Y
        # Shadow
        shadow = pygame.Surface((60, 16), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 60), (0, 0, 60, 16))
        self.screen.blit(shadow, (player_cx - 30, py + 58))
        # Character
        big_char = pygame.transform.smoothscale(self.player_sprite, (60, 60))
        self.screen.blit(big_char, (px, py))

    def _draw_runner(self):
        """Draw the full runner gameplay screen."""
        # Road
        self._draw_runner_road()

        # Items
        for item in self.runner_items:
            item.draw(self.screen, self.ticks)

        # Player
        self._draw_runner_player()

        # HUD bar at top
        hud = pygame.Surface((SCREEN_W, 90), pygame.SRCALPHA)
        pygame.draw.rect(hud, (0, 0, 0, 160), (0, 0, SCREEN_W, 90))
        self.screen.blit(hud, (0, 0))

        # Level label
        lvl_txt = self.font_small.render(
            f"Part 3: Catch the Word  —  Level {self.runner_level} / {self.runner_total_levels}",
            True, WHITE)
        self.screen.blit(lvl_txt, (20, 8))

        # Score
        score_txt = self.font_small.render(f"Score: {self.runner_score}", True, GOLD)
        self.screen.blit(score_txt, (SCREEN_W - score_txt.get_width() - 20, 8))

        # Target words panel
        panel_txt = self.font_small.render("Catch these words:", True, (200, 200, 255))
        self.screen.blit(panel_txt, (20, 38))
        x_off = 20
        for i, word in enumerate(self.runner_targets):
            caught = word in self.runner_collected
            if caught:
                col = (100, 255, 100)
                prefix = "✓ "
            else:
                col = (255, 200, 100)
                prefix = ""
            w_surf = self.font_small.render(prefix + word, True, col)
            self.screen.blit(w_surf, (x_off, 62))
            x_off += w_surf.get_width() + 18

        # Controls hint at bottom
        hint = self.font_small.render("← →  to switch lanes  |  Catch the GREEN words!", True, (180, 180, 180))
        self.screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, SCREEN_H - 30))

    def _draw_runner_level_complete(self):
        """Draw the level-complete interstitial."""
        self._draw_runner_road()

        # Overlay
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 0, 0, 120), (0, 0, SCREEN_W, SCREEN_H))
        self.screen.blit(overlay, (0, 0))

        # Text
        pulse = 1.0 + 0.1 * math.sin(self.ticks * 6)
        size = int(56 * pulse)
        font = pygame.font.SysFont("Arial", size, bold=True)
        txt = font.render(f"Level {self.runner_level} Complete!", True, GOLD)
        shadow = font.render(f"Level {self.runner_level} Complete!", True, (120, 90, 0))
        cx = SCREEN_W // 2 - txt.get_width() // 2
        cy = SCREEN_H // 2 - 80
        self.screen.blit(shadow, (cx + 3, cy + 3))
        self.screen.blit(txt, (cx, cy))

        # Score
        sc = self.font_med.render(f"Score: {self.runner_score}", True, WHITE)
        self.screen.blit(sc, (SCREEN_W // 2 - sc.get_width() // 2, cy + 80))

        # Stars for completed levels
        for i in range(self.runner_level):
            sx = SCREEN_W // 2 - (self.runner_level * 22) + i * 44
            self.screen.blit(self.star_img, (sx, cy + 130))

        # Prompt
        p = int(180 + 75 * math.sin(self.ticks * 3))
        if self.runner_level >= self.runner_total_levels:
            prompt_txt = "All levels done! Press ENTER!"
        else:
            prompt_txt = "Press ENTER for next level!"
        prompt = self.font_med.render(prompt_txt, True, (p, 255, p))
        self.screen.blit(prompt, (SCREEN_W // 2 - prompt.get_width() // 2, cy + 190))

    def _draw_runner_game_over(self):
        """Draw the game-over screen for runner mode."""
        self._draw_runner_road()

        # Dark overlay
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 0, 0, 180), (0, 0, SCREEN_W, SCREEN_H))
        self.screen.blit(overlay, (0, 0))

        # CRASH!
        crash_font = pygame.font.SysFont("Arial", 72, bold=True)
        txt = crash_font.render("CRASH!", True, RED)
        shadow = crash_font.render("CRASH!", True, (100, 20, 20))
        cx = SCREEN_W // 2 - txt.get_width() // 2
        cy = SCREEN_H // 2 - 100
        wobble = int(math.sin(self.ticks * 10) * 5)
        self.screen.blit(shadow, (cx + 3, cy + 3 + wobble))
        self.screen.blit(txt, (cx, cy + wobble))

        # Sub-text
        sub = self.font_med.render("You hit an obstacle!", True, (255, 180, 180))
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, cy + 90))

        # Character (sad tilt)
        big_char = pygame.transform.smoothscale(self.player_sprite, (80, 80))
        rotated = pygame.transform.rotate(big_char, 20)
        self.screen.blit(rotated, (SCREEN_W // 2 - 40, cy + 150))

        # Prompt
        p = int(180 + 75 * math.sin(self.ticks * 3))
        prompt = self.font_med.render("ENTER = Retry  |  ESC = Menu", True, (p, p, 255))
        self.screen.blit(prompt, (SCREEN_W // 2 - prompt.get_width() // 2, cy + 260))

    # ===================================================================
    # PANDA MODE Logic
    # ===================================================================

    def _start_panda(self):
        self.panda_level = 1
        self.panda_score = 0
        self.panda_hearts = PANDA_MAX_HEARTS
        self.panda_growth = 0
        self.panda_combo = 0
        self.panda_level_correct_count = 0
        self.panda_y_offset = 0.0
        self.panda_vy = 0.0
        self.panda_run_frame = 0.0
        self.panda_accessories = []
        self.panda_powerup = None
        self.panda_powerup_timer = 0
        self._start_panda_level()
        self._start_bgm()

    def _start_panda_level(self):
        self.state = self.PANDA_PLAYING
        # HARD RESET level data
        self.panda_falling.clear()
        self.panda_food_anims.clear()
        self.particles.clear()  # clear previous level's sparkles

        self.panda_q_idx = 0
        self.panda_level_correct_count = 0
        self.panda_spawn_queue.clear()
        self.panda_spawn_delay_timer = 60 # Start first spawn after 1 second
        self.panda_transition_timer = 0
        self.panda_expression = "happy"
        self.panda_expression_timer = 0
        self.panda_y_offset = 0.0
        self.panda_vy = 0.0
        self.panda_combo = 0  # reset combo per level for fresh start
        self.panda_powerup = None
        self.panda_powerup_timer = 0
        self.shake_timer = 0
        self.panda_correct_requeue = False
        self.panda_distractors_spawned = 0 # Reset counter for guaranteed spawning
        self.panda_last_caught_word = ""   # Reset last caught word tracking

        # Load category-specific level data (no more cross-category mixing!)
        self.panda_level_data = get_panda_level_data(self.panda_level)

        # Set theme
        theme = LEVEL_THEMES.get(self.panda_level, THEME_FOREST)
        self.panda_theme_bg = make_themed_bg(SCREEN_W, SCREEN_H, theme)

        # Unlock accessories
        if self.panda_level in ACCESSORY_UNLOCKS:
            acc = ACCESSORY_UNLOCKS[self.panda_level]
            if acc not in self.panda_accessories:
                self.panda_accessories.append(acc)

    def _update_panda(self, dt):
        # Update clouds (faster for running feel)
        for c in self.panda_clouds:
            c[0] += c[2] * 2.0
            if c[0] > SCREEN_W + 100: c[0] = -120

        # Automatic running frame
        self.panda_run_frame += dt * 10
        
        # Move Panda
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_LEFT]: dx -= PANDA_SPEED
        if keys[pygame.K_RIGHT]: dx += PANDA_SPEED
        
        # Jump
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.panda_y_offset == 0:
            self.panda_vy = -12.0
            self.snd_click.play()

        # Update jump physics
        self.panda_y_offset += self.panda_vy
        if self.panda_y_offset < 0:
            self.panda_vy += 0.6 # gravity
        else:
            self.panda_y_offset = 0
            self.panda_vy = 0
        
        if self.joystick:
            jx = self.joystick.get_axis(0)
            if abs(jx) > JOYSTICK_DEADZONE: dx = jx * PANDA_SPEED

        self.panda_x = max(60, min(SCREEN_W - 60, self.panda_x + dx))

        # Controlled Controlled Spawn System (Fixed 2 second interval = 120 frames)
        if self.panda_spawn_delay_timer > 0:
            self.panda_spawn_delay_timer -= 1

        requiredCorrect = self.panda_level # e.g. Level 1 = 1, Level 2 = 2
        can_spawn = (self.panda_level_correct_count < requiredCorrect)

        # Level 1 Spawning: Only ONE word on screen at a time
        max_active = 1 if self.panda_level == 1 else 3

        if can_spawn and self.panda_spawn_delay_timer <= 0:
            # Check if screen is clear for Level 1 or if there's room for other levels
            if len(self.panda_falling) < max_active:
                level_data = self.panda_level_data
                correct_word = level_data["correct"]
                distractors = level_data["distractors"]

                # Decide if we spawn the correct word or a distractor
                # Guaranteed to appear at least once every three spawns
                force_correct = (self.panda_distractors_spawned >= 2)
                # Randomness: if forced or 33% chance normally
                is_correct = force_correct or (random.random() < 0.4)

                if is_correct:
                    word_text = correct_word
                    self.panda_distractors_spawned = 0 # Reset
                else:
                    # RECENT EXCLUSION: Don't spawn the same distractor twice in a row
                    available = [d for d in distractors if d != self.panda_last_caught_word]
                    if not available: available = distractors # fallback if only 1 exists
                    word_text = random.choice(available)
                    self.panda_distractors_spawned += 1

                # Spawn it with visual category data
                lane_x = random.randint(150, SCREEN_W - 150)
                speed = PANDA_FALL_SPEEDS.get(self.panda_level, 1.0)
                if self.panda_powerup == "slowmo": speed *= 0.5

                fa = FallingAnswer(word_text, is_correct, lane_x, -100,
                                   random.choice(OPTION_COLORS), self.font_option, speed, level_data["category"])
                self.panda_falling.append(fa)

                # Reset fixed 2-second timer (120 frames at 60fps)
                self.panda_spawn_delay_timer = 120

        # Update falling items
        py = PANDA_PLAYER_Y + self.panda_y_offset
        panda_rect = pygame.Rect(self.panda_x - 45, py, 90, 90)

        remaining_falling = []
        for fa in self.panda_falling:
            fa.update()

            # Ground collision
            if fa.y > SCREEN_H:
                fa.alive = False
                continue

            # Catching logic
            if fa.rect.colliderect(panda_rect):
                # RECORD and DESTROY immediately
                self.panda_last_caught_word = fa.text
                
                # REINFORCEMENT POPUP: Show the word text to bridge image and text knowledge
                popup_col = GOLD if fa.is_correct else RED
                self.panda_score_popups.append((fa.text, fa.x, fa.y - 20, 50, popup_col))
                
                if fa.is_correct:
                    self._on_panda_correct(fa) # Score + increment count
                    # INSTANTLY check if currentCorrect >= requiredCorrect
                    if self.panda_level_correct_count >= requiredCorrect:
                        # Stop spawning, clear screen, complete level
                        self.panda_falling.clear()
                        self.state = self.PANDA_LEVEL_COMPLETE
                        self.snd_win.play()
                        return # Stop further updates this frame
                else:
                    self._on_panda_wrong()
                
                # Enforce 2-second delay after ANY catch before next spawn
                self.panda_spawn_delay_timer = 120
                fa.alive = False # Mark for immediate list removal
                continue

            remaining_falling.append(fa)
        # Final destruction: remove all caught/offscreen objects from the active list
        self.panda_falling = remaining_falling
        
        # Update food animations
        for fa in self.panda_food_anims:
            fa.update()
            if fa.done:
                self.snd_nomnom.play()
                self.panda_expression = "chewing"
                self.panda_expression_timer = 40
        self.panda_food_anims = [fa for fa in self.panda_food_anims if not fa.done]

        # Update powerup timer
        if self.panda_powerup_timer > 0:
            self.panda_powerup_timer -= 1
        else:
            self.panda_powerup = None

        # Expression timer
        if self.panda_expression_timer > 0:
            self.panda_expression_timer -= 1
        elif self.panda_expression != "happy":
            self.panda_expression = "happy"

        # Score popups float upward and fade
        self.panda_score_popups = [
            (txt, x, y - 1.2, life - 1, col)
            for txt, x, y, life, col in self.panda_score_popups
            if life > 0
        ]

        # Wrong-flash & heart-pulse timers tick down
        if self.panda_wrong_flash_timer > 0:
            self.panda_wrong_flash_timer -= 1
        if self.panda_heart_pulse > 0:
            self.panda_heart_pulse -= 1

    def _on_panda_correct(self, fa):
        self.snd_correct.play()
        pts = 10 * (2 if self.panda_powerup == "double" else 1)
        self.panda_score += pts
        self.panda_growth += 1
        self.panda_combo += 1
        self.panda_level_correct_count += 1
        if self.panda_combo > self.panda_max_combo:
            self.panda_max_combo = self.panda_combo

        # Score popup at catch position
        popup_col = GOLD if self.panda_powerup != "double" else (255, 80, 255)
        popup_txt = f"+{pts}" + (" x2!" if self.panda_powerup == "double" else "")
        self.panda_score_popups.append((popup_txt, fa.x, fa.y, 55, popup_col))

        # Big combo popup
        if self.panda_combo >= 3:
            self.panda_score_popups.append(
                (f"COMBO x{self.panda_combo}! 🔥", SCREEN_W // 2, SCREEN_H // 2 - 60, 70, ORANGE))

        # Food animation
        food = random.choice(FOOD_NAMES)
        anim = FoodFlyAnim(fa.x, fa.y, self.panda_x, PANDA_PLAYER_Y + self.panda_y_offset + 20, food)
        self.panda_food_anims.append(anim)

        # Rainbow sparkle burst at catch position
        colors = [GOLD, PINK, GREEN, BLUE, ORANGE, PURPLE, (255, 255, 100)]
        for i in range(28):
            self.particles.append(Particle(fa.x, fa.y, colors[i % len(colors)]))

        # Powerup every 3 combos
        if self.panda_combo % 3 == 0:
            self.panda_powerup = random.choice(["slowmo", "double"])
            self.panda_powerup_timer = 300  # 5 seconds
            self.panda_score_popups.append(
                (f"POWER-UP: {self.panda_powerup.upper()}!",
                 SCREEN_W // 2, SCREEN_H // 2, 90, GREEN))

    def _on_panda_wrong(self):
        self.snd_wrong.play()
        self.panda_hearts -= 1
        self.panda_combo = 0
        self.panda_expression = "sad"
        self.panda_expression_timer = 60
        self.shake_timer = 20
        self.panda_wrong_flash_timer = 25   # red flash overlay
        self.panda_heart_pulse = 18         # pulse animation on hearts
        # Sad sparkles
        for _ in range(10):
            self.particles.append(Particle(int(self.panda_x), PANDA_PLAYER_Y, (180, 180, 200)))
        if self.panda_hearts <= 0:
            self.state = self.PANDA_GAME_OVER

    def _draw_panda(self):
        self.screen.blit(self.panda_theme_bg, (0, 0))

        # Wrong-answer red flash overlay
        if self.panda_wrong_flash_timer > 0:
            alpha = int(min(160, self.panda_wrong_flash_timer * 9))
            flash = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            flash.fill((220, 30, 30, alpha))
            self.screen.blit(flash, (0, 0))

        # Animated clouds
        for cx, cy, sp in self.panda_clouds:
            _draw_cloud(self.screen, int(cx), cy)

        # Falling items
        for fa in self.panda_falling:
            fa.draw(self.screen, self.ticks)

        # Food anims
        for fa in self.panda_food_anims:
            fa.draw(self.screen)

        # Score popups (floating text)
        for txt, x, y, life, col in self.panda_score_popups:
            alpha = max(0, min(255, int(life * 5)))
            popup_font = self.font_med
            ps = popup_font.render(txt, True, col)
            ps.set_alpha(alpha)
            self.screen.blit(ps, (int(x) - ps.get_width() // 2, int(y)))

        # Panda
        expr = self.panda_expression
        if self.panda_level == 10:
            expr = "dancing"
        p_surf = make_panda_surface(PANDA_BASE_SIZE, self.panda_growth, expr,
                                    self.panda_accessories, self.ticks)

        run_angle = math.sin(self.panda_run_frame) * 4
        jump_scale = 1.0
        if self.panda_y_offset < 0:
            run_angle = 0
            jump_scale = 1.05

        if run_angle != 0 or jump_scale != 1.0:
            orig_sz = p_surf.get_size()
            p_surf = pygame.transform.rotozoom(p_surf, run_angle, jump_scale)
            new_sz = p_surf.get_size()
            px = int(self.panda_x - new_sz[0] // 2)
            py = int(PANDA_PLAYER_Y + self.panda_y_offset + (orig_sz[1] - new_sz[1]) // 2)
        else:
            px = int(self.panda_x - p_surf.get_width() // 2)
            py = int(PANDA_PLAYER_Y + self.panda_y_offset)

        ox, oy = 0, 0
        if self.shake_timer > 0:
            ox = random.randint(-5, 5)
            self.shake_timer -= 1
        self.screen.blit(p_surf, (px + ox, py))

        # HUD drawn last so it's always on top
        self._draw_panda_hud()

    def _draw_panda_hud(self):
        """Richly styled HUD: hearts + category badge + instruction + progress dots + score."""
        HUD_H = 128

        # Semi-transparent dark panel
        hud_surf = pygame.Surface((SCREEN_W, HUD_H), pygame.SRCALPHA)
        pygame.draw.rect(hud_surf, (20, 10, 40, 200), (0, 0, SCREEN_W, HUD_H), border_radius=0)
        # Thin glowing bottom border
        cat_col = CATEGORY_COLORS.get(
            self.panda_level_data.get("category", ""), (180, 180, 255))
        pygame.draw.line(hud_surf, cat_col, (0, HUD_H - 3), (SCREEN_W, HUD_H - 3), 3)
        self.screen.blit(hud_surf, (0, 0))

        # ── HEARTS (left side) ──────────────────────────────────────────────
        for i in range(PANDA_MAX_HEARTS):
            filled = i < self.panda_hearts
            pulse  = self.panda_heart_pulse > 0 and not filled
            hx = 28 + i * 44
            hy = 24
            r  = 16 + (4 if pulse else 0)
            col = RED if filled else (60, 30, 60)
            # heart shape: two overlapping circles + triangle
            pygame.draw.circle(self.screen, col, (hx - 6, hy), r - 4)
            pygame.draw.circle(self.screen, col, (hx + 6, hy), r - 4)
            pts = [(hx - r + 4, hy + 2), (hx + r - 4, hy + 2), (hx, hy + r + 4)]
            pygame.draw.polygon(self.screen, col, pts)
            if filled:
                pygame.draw.circle(self.screen, (255, 180, 180), (hx - 7, hy - 4), 4)

        # ── LEVEL label (left side, below hearts) ──────────────────────────
        lvl_surf = self.font_small.render(
            f"Level {self.panda_level} / {self.panda_total_levels}", True, (200, 200, 255))
        self.screen.blit(lvl_surf, (14, 52))

        # ── SCORE (right side, top) ─────────────────────────────────────────
        score_surf = self.font_med.render(f"⭐ {self.panda_score}", True, GOLD)
        self.screen.blit(score_surf, (SCREEN_W - score_surf.get_width() - 16, 8))

        # ── CATEGORY badge ─────────────────────────────────────────────────
        if self.panda_level_data:
            cat_name    = self.panda_level_data.get("category", "")
            instruction = self.panda_level_data.get("instruction", "")
            cat_col     = CATEGORY_COLORS.get(cat_name, (160, 160, 255))

            # Category pill badge (centred, top row)
            badge_text  = f"  {cat_name.upper()}  "
            badge_surf  = self.font_small.render(badge_text, True, WHITE)
            bw, bh      = badge_surf.get_width() + 14, badge_surf.get_height() + 8
            bx          = SCREEN_W // 2 - bw // 2
            by          = 6
            badge_bg    = pygame.Surface((bw, bh), pygame.SRCALPHA)
            pygame.draw.rect(badge_bg, (*cat_col, 220), (0, 0, bw, bh), border_radius=12)
            self.screen.blit(badge_bg, (bx, by))
            self.screen.blit(badge_surf, (bx + 7, by + 4))

            # ── Big instruction text (centred, below badge) ─────────────────
            pulse_offset = int(math.sin(self.ticks * 4) * 2)
            instr_surf   = self.font_big.render(instruction, True, cat_col)
            instr_shadow = self.font_big.render(instruction, True, (0, 0, 0))
            ix = SCREEN_W // 2 - instr_surf.get_width() // 2
            iy = 36 + pulse_offset
            self.screen.blit(instr_shadow, (ix + 2, iy + 2))
            self.screen.blit(instr_surf,   (ix, iy))

        # ── Progress dots (right side, centred vertically) ─────────────────
        target     = self.panda_level + 2
        dot_r      = 9
        dot_gap    = dot_r * 2 + 8
        dots_total_w = target * dot_gap
        dx_start   = SCREEN_W - dots_total_w - 16
        dy         = 60
        for i in range(target):
            filled = i < self.panda_level_correct_count
            dx = dx_start + i * dot_gap + dot_r
            col = GREEN if filled else (60, 60, 80)
            pygame.draw.circle(self.screen, col, (dx, dy), dot_r)
            if filled:
                pygame.draw.circle(self.screen, (180, 255, 180), (dx - 3, dy - 3), 3)
            pygame.draw.circle(self.screen, WHITE, (dx, dy), dot_r, 2)
        prog_lbl = self.font_small.render("Progress", True, (160, 160, 200))
        self.screen.blit(prog_lbl, (dx_start, dy + dot_r + 4))

        # ── Combo ribbon ────────────────────────────────────────────────────
        if self.panda_combo >= 2:
            combo_col = ORANGE if self.panda_combo < 5 else (255, 50, 50)
            glow = int(180 + 75 * math.sin(self.ticks * 6))
            combo_surf = self.font_small.render(
                f"🔥 COMBO x{self.panda_combo}!", True, (glow, min(255, glow + 80), 50))
            self.screen.blit(combo_surf, (16, 78))

        # ── Powerup pill ────────────────────────────────────────────────────
        if self.panda_powerup:
            secs_left = self.panda_powerup_timer // 60 + 1
            pu_text   = f"✨ {self.panda_powerup.upper()}  {secs_left}s"
            pu_surf   = self.font_small.render(pu_text, True, WHITE)
            pw, ph    = pu_surf.get_width() + 16, pu_surf.get_height() + 8
            pux, puy  = 16, 98
            pu_bg     = pygame.Surface((pw, ph), pygame.SRCALPHA)
            pu_alpha  = int(160 + 60 * math.sin(self.ticks * 8))
            pygame.draw.rect(pu_bg, (40, 200, 120, pu_alpha), (0, 0, pw, ph), border_radius=10)
            self.screen.blit(pu_bg, (pux, puy))
            self.screen.blit(pu_surf, (pux + 8, puy + 4))

    def _draw_panda_level_complete(self):
        """Celebratory level-complete screen with sticker, panda, and stars."""
        self._draw_panda()  # draw game world beneath overlay

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        self.screen.blit(overlay, (0, 0))

        # Coloured burst banner
        banner_h = 100
        banner_y = SCREEN_H // 2 - banner_h // 2 - 60
        cat_col  = CATEGORY_COLORS.get(
            self.panda_level_data.get("category", ""), (200, 200, 255))
        pygame.draw.rect(self.screen, cat_col, (0, banner_y, SCREEN_W, banner_h),
                         border_radius=0)
        lighter = tuple(min(255, c + 60) for c in cat_col)
        pygame.draw.rect(self.screen, lighter, (0, banner_y, SCREEN_W, banner_h // 2))

        # "Level Complete!" text (pulsing)
        pulse = 1.0 + 0.08 * math.sin(self.ticks * 6)
        lc_font = pygame.font.SysFont("Arial", int(58 * pulse), bold=True)
        lc_txt  = lc_font.render(f"Level {self.panda_level}  Complete! 🎉", True, WHITE)
        lc_shd  = lc_font.render(f"Level {self.panda_level}  Complete! 🎉", True, (40, 40, 40))
        cx = SCREEN_W // 2 - lc_txt.get_width() // 2
        cy = banner_y + 20
        self.screen.blit(lc_shd, (cx + 3, cy + 3))
        self.screen.blit(lc_txt, (cx, cy))

        # Sticker emoji (large)
        emoji_idx   = (self.panda_level - 1) % len(STICKER_EMOJIS)
        sticker_chr = STICKER_EMOJIS[emoji_idx]
        sticker_name = STICKER_NAMES[emoji_idx]
        em_font  = pygame.font.SysFont("Segoe UI Emoji", 80)
        em_surf  = em_font.render(sticker_chr, True, WHITE)
        bob = int(math.sin(self.ticks * 3) * 7)
        em_x = SCREEN_W // 2 - em_surf.get_width() // 2
        em_y = banner_y + banner_h + 20 + bob
        self.screen.blit(em_surf, (em_x, em_y))

        # Sticker name
        stk_surf = self.font_med.render(
            f"You earned the  {sticker_name}  Sticker!", True, GOLD)
        self.screen.blit(stk_surf,
                         (SCREEN_W // 2 - stk_surf.get_width() // 2, em_y + 90))

        # Accessory unlock notification
        if self.panda_level in ACCESSORY_UNLOCKS:
            acc = ACCESSORY_UNLOCKS[self.panda_level]
            acc_surf = self.font_small.render(
                f"🎁  Unlocked accessory:  {acc.upper()}!", True, (255, 220, 80))
            self.screen.blit(acc_surf,
                             (SCREEN_W // 2 - acc_surf.get_width() // 2, em_y + 130))

        # Stars row
        star_y = em_y + 170
        for i in range(self.panda_level):
            angle = self.ticks * 1.5 + i * 0.5
            sx = SCREEN_W // 2 - (self.panda_level * 26) // 2 + i * 26
            sy = star_y + int(math.sin(angle) * 5)
            # Draw a small 5-point star procedurally
            r_outer, r_inner = 14, 6
            star_pts = []
            for k in range(10):
                a = math.radians(-90 + k * 36)
                r = r_outer if k % 2 == 0 else r_inner
                star_pts.append((sx + r * math.cos(a), sy + r * math.sin(a)))
            pygame.draw.polygon(self.screen, GOLD, star_pts)
            pygame.draw.polygon(self.screen, (200, 140, 0), star_pts, 2)

        # Score & best combo
        info = self.font_small.render(
            f"Score: {self.panda_score}   Best Combo: x{self.panda_max_combo}",
            True, (200, 220, 255))
        self.screen.blit(info, (SCREEN_W // 2 - info.get_width() // 2, star_y + 38))

        # Prompt
        p = int(180 + 75 * math.sin(self.ticks * 3))
        if self.panda_level >= self.panda_total_levels:
            prompt_str = "All Levels Done!  Press SPACE!"
        else:
            prompt_str = "Press SPACE  for the Next Level!"
        prompt = self.font_med.render(prompt_str, True, (p, 255, p))
        self.screen.blit(prompt,
                         (SCREEN_W // 2 - prompt.get_width() // 2, star_y + 68))

    def _draw_panda_game_over(self):
        """Sad game-over screen with animated panda and retry prompt."""
        self._draw_panda()

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Wobbling "Game Over" text
        wobble = int(math.sin(self.ticks * 8) * 6)
        go_font = pygame.font.SysFont("Arial", 72, bold=True)
        go_txt  = go_font.render("Game Over!", True, RED)
        go_shd  = go_font.render("Game Over!", True, (80, 0, 0))
        gx = SCREEN_W // 2 - go_txt.get_width() // 2
        gy = 140 + wobble
        self.screen.blit(go_shd, (gx + 4, gy + 4))
        self.screen.blit(go_txt, (gx, gy))

        # Sad panda (big)
        sad_surf = make_panda_surface(PANDA_BASE_SIZE + 20, self.panda_growth,
                                      "sad", self.panda_accessories, self.ticks)
        tilt     = pygame.transform.rotate(sad_surf, 15)
        self.screen.blit(tilt, (SCREEN_W // 2 - tilt.get_width() // 2, 240))

        # Sub-message
        sub = self.font_med.render("Don't give up — the panda believes in you! 🐼",
                                   True, (255, 200, 200))
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 430))

        # Score
        sc_surf = self.font_med.render(f"Score: {self.panda_score}", True, GOLD)
        self.screen.blit(sc_surf, (SCREEN_W // 2 - sc_surf.get_width() // 2, 470))

        # Prompt
        p = int(180 + 75 * math.sin(self.ticks * 3))
        prompt = self.font_med.render("SPACE = Try Again   |   ESC = Menu",
                                      True, (p, p, 255))
        self.screen.blit(prompt, (SCREEN_W // 2 - prompt.get_width() // 2, 520))


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    game = Game()
    game.run()
