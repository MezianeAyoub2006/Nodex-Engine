import pygame 
from dataclasses import dataclass 

@dataclass
class PlayerKey:
    left:int 
    right:int 
    up:int 
    down:int 
    jump:int 
    drift:int 

WASD = PlayerKey(
    pygame.K_a,
    pygame.K_d,
    pygame.K_w,
    pygame.K_s,
    pygame.K_SPACE,
    pygame.K_l
)

ZQSD = PlayerKey(
    pygame.K_q,
    pygame.K_d,
    pygame.K_z,
    pygame.K_s,
    pygame.K_SPACE,
    pygame.K_l
)

ARROWS = PlayerKey(
    pygame.K_LEFT,
    pygame.K_RIGHT,
    pygame.K_UP,
    pygame.K_DOWN,
    pygame.K_SPACE,
    pygame.K_x
)