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

    def _handle_keyboard(self):
        self._active_keys = pygame.key.get_pressed() 
        self._pressed_keys = pygame.key.get_just_pressed()
        self._released_keys = pygame.key.get_just_released() 

    @property 
    def active_keys(self):
        return self._active_keys 

    @property
    def pressed_keys(self):
        return self._pressed_keys 
    
    @property 
    def released_keys(self):
        return self._released_keys

    def run(self):
        while True: 
            self._handle_keyboard()
            self.context.system.poll_events()
            self.context.gl_context.before_rendering() 
            self.context.scene_manager.update()
            self.context.gl_context.after_rendering()
            pygame.display.flip()
            self._dt = self._clock.tick(1000) / 10000
            self.context.timer += 1000 * self._dt
        

    @property 
    def dt(self):
        return self._dt 

    @property 
    def fps(self):
        return self._clock.get_fps()
    
