import pygame
import moderngl 
import numpy as np
import nodex.engine

def make_quad(x1:int, y1:int, x2:int, y2:int) -> np.ndarray:
    return np.array([
        x1, y1,  0.0, 0.0,
        x2, y1,  1.0, 0.0,
        x1, y2,  0.0, 1.0,
        x2, y1,  1.0, 0.0,
        x2, y2,  1.0, 1.0,
        x1, y2,  0.0, 1.0,
    ], dtype='f4')

def pixels_to_ndc(ox:int, oy:int, sw:int, sh:int, W:int, H:int) -> tuple:
    x1 = (ox / W) * 2 - 1
    y1 = 1 - ((oy + sh) / H) * 2
    x2 = ((ox + sw) / W) * 2 - 1
    y2 = 1 - (oy / H) * 2
    return x1, y1, x2, y2

class ShaderPass:
    def __init__(self, context : "nodex.engine.Context", frag_prog:str = None, vert_prog:str = None):
        self.context = context
        self.textures = {}   
        self.uniforms = {}   
        self.shader_prog = context._gl_context._gl_ctx.program(
            vertex_shader = vert_prog or self.context.shaders.get("_vertex"),
            fragment_shader = frag_prog or self.context.shaders.get("_fragment")
        )
        self._vbo = context._gl_context._gl_ctx.buffer(make_quad(-1, -1, 1, 1).tobytes(), dynamic=True)
        self._vao = context._gl_context._gl_ctx.vertex_array(self.shader_prog, [(self._vbo, '2f 2f', 'in_pos', 'in_uv')])
        self._viewport = None  

    def _next_slot(self) -> int:
        used = {slot for _, slot in self.textures.values()}
        slot = 0
        while slot in used:
            slot += 1
        return slot

    def set_viewport(self, ox:int, oy:int, sw:int, sh:int) -> None:
        self._viewport = (ox, oy, sw, sh)

    def dump_pygame_surf(self, name: str, surf: pygame.Surface, slot: int = None, filter: int = moderngl.NEAREST) -> None:
        data = pygame.image.tobytes(surf, "RGBA", True)
        if name in self.textures:
            tex, assigned_slot = self.textures[name]
            if tex.size == surf.get_size():
                tex.write(data)
                return
            else:
                tex.release()  
        tex = self.context._gl_context._gl_ctx.texture(surf.get_size(), 4)
        tex.filter = (filter, filter)
        tex.write(data)
        assigned_slot = slot if slot is not None else self._next_slot()
        self.textures[name] = (tex, assigned_slot)

    def load_texture(self, name:str, path:str, slot:int = None, filter:int = moderngl.NEAREST) -> None:
        self.dump_pygame_surf(
            name, 
            pygame.image.load(path).convert_alpha(), 
            slot, 
            filter
        )

    def set_uniform(self, name:str, value:int) -> None:
        self.uniforms[name] = value

    def render(self) -> None:
        self._update_quad()
        for name, (tex, slot) in self.textures.items():
            tex.use(slot)
            self.shader_prog[name] = slot
        for name, value in self.uniforms.items():
            if name in self.shader_prog:
                self.shader_prog[name] = value
        self._vao.render()
        self._viewport = None 

    def _update_quad(self) -> None:
        W, H = self.context.window.internal_size 

        if self._viewport is not None:
            ox, oy, sw, sh = self._viewport
        elif self.textures:
            tex, _ = next(iter(self.textures.values()))
            sw, sh = tex.size
            ox, oy = 0, 0
        else:
            x1, y1, x2, y2 = -1, -1, 1, 1
            self._vbo.write(make_quad(x1, y1, x2, y2).tobytes())
            return

        x1, y1, x2, y2 = pixels_to_ndc(ox, oy, sw, sh, W, H)
        self._vbo.write(make_quad(x1, y1, x2, y2).tobytes())