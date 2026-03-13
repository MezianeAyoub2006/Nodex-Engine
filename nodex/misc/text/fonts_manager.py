import pygame
import nodex

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...engine.core.context import Context

class FontsManager:
    def __init__(self, context):
        self.context = context 
        self._fonts:dict[str, pygame.font.Font] = {}

    def load_font(self, name, path, sizes):
        if any(k.startswith(name) for k in self._fonts):
            raise KeyError(f"\"{name}\" font already exist")
        for i in sizes:
            self._fonts[f"{name}{i}"] = pygame.font.Font(path, i) 

    def load_sys_font(self, name, sys_name, sizes):
        if any(k.startswith(name) for k in self._fonts):
            raise KeyError(f"\"{name}\" font already exist")
        for i in sizes:
            self._fonts[f"{name}{i}"] = pygame.font.SysFont(sys_name, i)
            self._fonts[f"{name}{i}bold"] = pygame.font.SysFont(sys_name, i, True)
    
    def render(self, font, text, color = (0, 0, 0)):
        return self._fonts[font].render(text, False, color) 
    
