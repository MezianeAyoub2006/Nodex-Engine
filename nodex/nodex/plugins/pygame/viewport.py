import pygame

from ...core import Context, settings
from ...math import Rectangle 
VP_Z_OFFSET = 100

class PygameViewport:
    def __init__(self, context: Context, shader_name: str, order: float, region: Rectangle = None):
        self.context = context 
        self.shader_name = shader_name
        self.order = order
     
        if not region:
            region = Rectangle(0, 0, *self.context.window.virtual_size)
            
        self.region = region

    def _draw(self):
        self.context.graphics.draw(self.surface, settings.texture((
            self.region.x,
            self.region.y
        )), VP_Z_OFFSET + self.order)
        
    def render(self):
        if self.shader_name:
            with self.context.shaders.apply(self.shader_name):
                self._draw()
                return 
        self._draw()
        self.surface.fill((0, 0, 0, 0))
    
    def reset_surface(self):
        self.surface = pygame.Surface((
            self.region.width,
            self.region.height
        ), pygame.SRCALPHA)
        self.clear_surface()

    @property 
    def region(self) -> Rectangle:
        return self._region

    @region.setter
    def region(self, value: Rectangle):
        self._region = value
        self._region.x += value.width / 2
        self._region.y += value.height / 2
        self.reset_surface()
    
    def clear_surface(self):
        self.surface.fill((0, 0, 0, 0))

        