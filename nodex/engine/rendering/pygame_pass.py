from .shader_pass import ShaderPass 

import pygame
import moderngl


class PygamePass(ShaderPass):
    """ 
    Small abstraction over ShaderPass, used to handle pygame graphics.
    """

   
    def __init__(self, context, frag_prog = None, vert_prog = None):
        self._surf = pygame.Surface(context.window.internal_size, pygame.SRCALPHA)
        super().__init__(context, frag_prog, vert_prog)      
        self.set_tex(0)

    def set_tex(self, slot):
        tex = self.context._gl_context._gl_ctx.texture(self.context.window.internal_size, 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.textures["tex"] = (tex, slot)

 

    def blit(self, surface, position):
        self._surf.blit(surface, position)

    def render(self):
        tex, _ = self.textures["tex"]
        tex.write(pygame.image.tobytes(self._surf, "RGBA", True))
        self._surf.fill((0, 0, 0, 0))
        ShaderPass.render(self)