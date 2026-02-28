import pygame
import nodex
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .sound import Sound



class SoundManager:
    def __init__(self, context:"nodex.Context"):
        self.context = context
        self.sounds:dict[str, Sound] = {}

    def load_sound(self, name:str, file:str):
        self.sounds[name] = Sound(self.context, pygame.mixer.Sound(file))

    def get_sound(self, name:str, copy:bool = True):
        if copy:
            return self.sounds.get(name).copy()
        else:
            return self.sounds.get(name)