import pygame 

from typing import Any

from ....math import Rectangle 
from ..abstract.texture import AbstractTexture

# pygame.Surface wrapper 
class PygameModernglTexture(AbstractTexture):
    
    INJECTION_TYPE = pygame.Surface
    _internal: pygame.Surface
    
    @staticmethod
    def blank(size: tuple[int, int]) -> "PygameModernglTexture":
        tex = PygameModernglTexture.__new__(PygameModernglTexture)
        tex._internal = pygame.Surface(size, pygame.SRCALPHA)
        tex._internal.fill((0, 0, 0, 0))
        return tex
    
    @staticmethod
    def inject(internal: Any) -> "PygameModernglTexture":
        tex = PygameModernglTexture.__new__(PygameModernglTexture)
        tex._internal = internal
        return tex

    def __init__(self, path: str) -> None:
        self._internal = pygame.image.load(path).convert_alpha() 

    def fill(self, color: tuple[int, int, int, int]) -> None:
        self._internal.fill(color)

    def blit(self, texture: "PygameModernglTexture", position: tuple[int, int]) -> None:
        self._internal.blit(texture._internal, position) 

    def copy(self, region: Rectangle = None) -> "PygameModernglTexture":
        src = self._internal.subsurface(region) if region else self._internal
        tex = PygameModernglTexture.__new__(PygameModernglTexture)
        tex._internal = src.copy()  
        return tex

    def view(self, region: Rectangle) -> "PygameModernglTexture":
        tex = PygameModernglTexture.__new__(PygameModernglTexture)
        tex._internal = self._internal.subsurface(region)  
        return tex
    
    def free(self) -> None:
        pass 

    @property
    def size(self) -> tuple[int, int]:
        return self._internal.get_size()
    
    
        