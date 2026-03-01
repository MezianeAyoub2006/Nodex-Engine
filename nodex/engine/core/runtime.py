import pygame
import time

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .context import Context

class Runtime:
    def __init__(self, context : "Context"):
        self.context = context 
        self._clock = pygame.time.Clock()
        self._dt = 1

    def run(self):
        while True: 
            self.context.input._handle_keyboard()
            self.context.system.poll_events()
            self.context.scenes._update()
            self.context._gl_context.before_rendering() 
            self.context.renderer.render()
            self.context._gl_context.after_rendering()
            pygame.display.flip()
            self._dt = self._clock.tick(1000) / 1000
            self.context.timer += self._dt
            self.context.renderer.clear()
        
    @property 
    def dt(self):
        return self._dt 

    @property 
    def fps(self):
        return self._clock.get_fps()
    
