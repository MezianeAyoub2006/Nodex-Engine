import pygame

class Camera3D:
    def __init__(self):
        self.position:pygame.Vector3 = pygame.Vector3(0, 0, 0) 
        self.rotation:float = 0
        self.horizon_height:float = 0.5
        self.offset:int = pygame.Vector2()

