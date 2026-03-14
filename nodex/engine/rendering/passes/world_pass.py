from .pygame_pass import PygamePass
from ..cameras.camera2D import Camera2D
import nodex

class WorldPass(PygamePass):
    def __init__(self, context : "nodex.Context", frag_prog=None): 
        self.context = context
        self.camera = Camera2D()
        super().__init__(context, frag_prog, self.context.shaders.get("_world"))
    
    def draw(self, surf, position):
        self.blit(surf, (position[0] - self.camera.position.x, position[1] - self.camera.position.y))
    
    def render(self):
        self.set_uniform("rotation", self.camera.rotation)
        self.set_uniform("zoom", self.camera.zoom)
        super().render()