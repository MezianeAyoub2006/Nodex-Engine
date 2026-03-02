import pygame

class Camera3D:
    # even tho it's called Camera3D, it's actually used for mode 7
    def __init__(self):
        self.position:pygame.Vector3 = pygame.Vector3(0, 0, 0) 
        self.rotation:float = 0
        self.horizon_height:float = 0.5

