import pygame 

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .context import Context

class Input:
    def __init__(self, context : "Context"):
        self.context = context 
        self._handle_keyboard()

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
    
    @property 
    def mouse_position(self):
        scaled_mouse_pos = self.scaled_mouse_position 
        window_scale = self.context.window_scale
        print(scaled_mouse_pos, window_scale)
        return (
            scaled_mouse_pos[0] / window_scale, 
            scaled_mouse_pos[1] / window_scale 
        )
    
    @property
    def scaled_mouse_position(self):
        return pygame.mouse.get_pos()