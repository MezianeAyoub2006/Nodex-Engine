
import pygame

class Camera2D:
    def __init__(self):
        self.position:pygame.Vector2 = pygame.Vector2(0, 0) 
        self.offset:pygame.Vector2 = pygame.Vector2(0, 0)
        self.rotation:float = 0
        self.zoom:float = 1.4

