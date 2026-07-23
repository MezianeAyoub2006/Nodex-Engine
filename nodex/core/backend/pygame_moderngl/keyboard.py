import pygame

from ..abstract.keyboard import AbstractKeyboard
from .convert_keyboard import key_to_pygame, pygame_to_key
from ..states.key import Key

class PygameKeyboard(AbstractKeyboard):   
    def __init__(self): 
        self._pressed = {}
        self._released = {}
        self._active = {}

    def _listen(self):
        self._active = pygame.key.get_pressed()
        self._pressed = pygame.key.get_just_pressed() 
        self._released = pygame.key.get_just_released()
    
    def is_pressed(self, key: Key):
        return self._pressed[key_to_pygame(key)]

    def is_active(self, key: Key):
        return self._active[key_to_pygame(key)]

    def is_released(self, key: Key):
        return self._released[key_to_pygame(key)]

    @property
    def active(self) -> list[Key]: 
        return [pygame_to_key(key) for key in self._active if self._active[key]] 

    @property 
    def pressed(self) -> list[Key]:
        return [pygame_to_key(key) for key in self._pressed if self._pressed[key]]

    @property 
    def released(self) -> list[Key]:
        return [pygame_to_key(key) for key in self._released if self._released[key]]
     

