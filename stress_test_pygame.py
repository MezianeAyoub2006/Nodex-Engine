import pygame
import time
import random

import ctypes
if hasattr(ctypes, 'windll'):
    ctypes.windll.user32.SetProcessDPIAware()


pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("HellAAA")
clock = pygame.time.Clock()

tex = pygame.image.load("bird.png").convert_alpha()

def draw_tex(surface, x, y):
    screen.blit(surface, (x, y))

class Bird:
    def __init__(self):
        self.x = random.randint(0, 600)
        self.y = random.randint(0, 600)
        self.dx = 0
        while (abs(self.dx) < 30):
            self.dx = random.randint(-100, 100)
        self.dy = 0
        while (abs(self.dy) < 30):
            self.dy = random.randint(-100, 100)

    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
        if self.x < 0 or self.x > 570 or self.y < 0 or self.y > 580:
            self.x = 300
            self.y = 300

        draw_tex(tex, self.x, self.y)


BIRDS = [Bird() for i in range(8000)]

t = time.perf_counter()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick() / 1000.0

    screen.fill((0, 0, 0))
    for bird in BIRDS:
        bird.update(dt)
    pygame.display.flip()

    if time.perf_counter() - t > 0.5:
        t = time.perf_counter()
        print(clock.get_fps())

pygame.quit()