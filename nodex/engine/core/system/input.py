import pygame 

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..context import Context


class Input:
    def __init__(self, context : "Context"):
        self.context = context 
        self.reset_mouse_pressed()
        self._handle_keyboard()

    
    def reset_mouse_pressed(self):
        self._mouse_pressed = [False, False]

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
        window_scale = self.context.window.window_scale
        offset = self.context.window.offset
        return (
            (scaled_mouse_pos[0] - offset[0]) / window_scale,
            (scaled_mouse_pos[1] - offset[1]) / window_scale
        )
        
    @property
    def scaled_mouse_position(self):
        return pygame.mouse.get_pos()

    @property
    def mouse_clicked(self):
        return pygame.mouse.get_pressed()
    
    @property
    def mouse_pressed(self):
        return self._mouse_pressed
    
    def mouse_set_visible(self, value):
        pygame.mouse.set_visible(value)