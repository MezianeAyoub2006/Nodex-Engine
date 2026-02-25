import pygame
import time

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .context import Context


class Runtime:
    def __init__(self, context : "Context"):
        self.context = context 
        self._clock = pygame.time.Clock()
        self._lt = time.perf_counter() 
        self._dt = 1
    
    def _delta_time(self):
        self._dt = (time.perf_counter() - self._lt)  
        self._lt = time.perf_counter()

    def run(self):
        while True: 
            self.context.input._handle_keyboard()
            self._delta_time()
            self.context.system.poll_events()
            self.context.gl_context.before_rendering() 
            self.context.scene_manager.update()
            self.context.gl_context.after_rendering()
            pygame.display.flip() 
            self._clock.tick(1000) 
            self.context.timer += self.dt 
        

    @property 
    def dt(self):
        return self._dt 

    @property 
    def fps(self):
        return self._clock.get_fps()
    
