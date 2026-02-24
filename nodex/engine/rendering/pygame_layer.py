from .shader_pass import ShaderPass 

import pygame
import moderngl

class PygameLayer(ShaderPass):
    """ 
    Small abstraction over ShaderPass, used to handle pygame graphics.
    """
    def __init__(self, context, frag_prog = None):
        self._surf = pygame.Surface(context.internal_size, pygame.SRCALPHA)
        super().__init__(context, frag_prog)
        tex = context.gl_context._gl_ctx.texture(context.internal_size, 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.textures["tex"] = (tex, 0)

    def blit(self, surface, position):
        self._surf.blit(surface, position)

    def render(self):
        tex, _ = self.textures["tex"]
        tex.write(pygame.image.tobytes(self._surf, "RGBA", True))
        self._surf.fill((0, 0, 0, 0))
        super().render()