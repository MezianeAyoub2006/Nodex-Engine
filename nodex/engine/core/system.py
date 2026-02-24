import pygame 

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .context import Context

class System:
    def __init__(self, context : "Context"):
        self.context = context 
    
    def poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.context.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.context.toggle_fullscreen()
                