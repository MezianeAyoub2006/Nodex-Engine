import ctypes
import pygame
import numpy as np
import time

# Désactive le DPI scaling Windows — doit être appelé AVANT pygame.init()
if hasattr(ctypes, 'windll'):
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

pygame.init()

WIDTH, HEIGHT = 600, 600
N_OISEAUX = 4500
BOUNDS_MIN = 0.0
BOUNDS_MAX = 600.0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hello Some Shi")
clock = pygame.time.Clock()

base_tex = pygame.image.load("bird.png").convert_alpha()

scaled_tex = pygame.transform.scale(
    base_tex,
    (base_tex.get_width() * 2, base_tex.get_height() * 2)
)

ANGLE_STEPS = 360
rotated_cache = [
    pygame.transform.rotate(scaled_tex, angle)
    for angle in range(ANGLE_STEPS)
]

def get_rotated_surface(rotation_deg):
    idx = int(rotation_deg) % ANGLE_STEPS
    return rotated_cache[idx]

positions = np.random.uniform(0, 600, size=(N_OISEAUX, 2)).astype(np.float32)
velocities = np.random.uniform(-30, 30, size=(N_OISEAUX, 2)).astype(np.float32)

def update_birds(dt):
    global positions, velocities
    positions += velocities * dt
    below = positions < BOUNDS_MIN
    above = positions > BOUNDS_MAX
    positions[below] = BOUNDS_MIN
    positions[above] = BOUNDS_MAX
    velocities[below] *= -1
    velocities[above] *= -1

timer = 0
u_timer = 0
frames = 0
last_time = time.perf_counter()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = time.perf_counter()
    dt = now - last_time
    last_time = now

    u_timer += dt
    frames += 1

    update_birds(dt)

    screen.fill((0, 0, 0))

    rotation = u_timer * 30
    surf = get_rotated_surface(rotation)

    pos_list = positions.tolist()
    for i in range(N_OISEAUX):
        x, y = pos_list[i]
        rect = surf.get_rect(center=(x, y))
        screen.blit(surf, rect)

    pygame.display.flip()

    timer += dt
    if timer > 1:
        print(frames)
        frames = 0
        timer -= 1

pygame.quit()