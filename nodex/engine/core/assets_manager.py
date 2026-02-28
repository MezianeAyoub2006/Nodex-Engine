import pygame

from typing import TYPE_CHECKING 
if TYPE_CHECKING:
    from .context import Context

class AssetsManager:
    def __init__(self, context : "Context"):
        self.context = context 
        self._assets = {}
        self._spritesheets = {}

    def register_surface(self, name, surface):
        self._assets[name] = surface 

    def _load_image(self, path, scale=(1, 1)):
        try:
            surface = pygame.image.load(path).convert_alpha()
        except:
            raise FileNotFoundError(f"'{path}' file not found")
        
        if scale == (1, 1):
            return surface
        w, h = surface.get_size()
        return pygame.transform.scale(surface, (w * scale[0], h * scale[1]))
                
    def load_image(self, name, path, scale = (1, 1)):
        self.register_surface(name, self._load_image(path, scale))
    
    def load_spritesheet(self, name, path, tile_size, scale = (1, 1)):
        spritesheet_surface = self._load_image(path, scale) 
        spritesheet_size = spritesheet_surface.get_size() 
        spritesheet = {}
        for x in range(int(spritesheet_size[0] // tile_size[0])):
            for y in range(int(spritesheet_size[1] // tile_size[1])):
                spritesheet[(x, y)] = spritesheet_surface.subsurface((
                    x * tile_size[0],
                    y * tile_size[1],
                    tile_size[0],
                    tile_size[1]
                ))
        self._spritesheets[name] = spritesheet
        
    def get_image(self, name):
        if name in self._assets:
            return self._assets[name]
        else:
            raise KeyError(f"'{name}' image don't exist")
    
    def get_spritesheet(self, name):
        if name in self._spritesheets:
            return self._spritesheets[name]
        else:
            raise KeyError(f"'{name}' spritesheet don't exist")
        


