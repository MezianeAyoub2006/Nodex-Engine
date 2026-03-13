import pygame
import moderngl 
import numpy as np
import nodex

class ShaderPass:
    def __init__(self, context : "nodex.Context", frag_prog:str = None, vert_prog:str = None):
        self.context = context
        self.textures = {}   
        self.uniforms = {}   
        self.shader_prog = context._gl_context.gl_ctx.program(
            vertex_shader = vert_prog or self.context.shaders.get("_vertex"),
            fragment_shader = frag_prog or self.context.shaders.get("_fragment")
        )
        self.vbo = context._gl_context.gl_ctx.buffer(nodex.make_quad(-1, -1, 1, 1).tobytes(), dynamic=True)
        self.vao = context._gl_context.gl_ctx.vertex_array(self.shader_prog, [(self.vbo, '2f 2f', 'in_pos', 'in_uv')])
        self.viewport = None  

    def next_slot(self) -> int:
        used = {slot for _, slot in self.textures.values()}
        slot = 0
        while slot in used:
            slot += 1
        return slot

    def set_viewport(self, ox:int, oy:int, sw:int, sh:int) -> None:
        self.viewport = (ox, oy, sw, sh)

    def dump_pygame_surf(self, name: str, surf: pygame.Surface, slot: int = None, filter: int = moderngl.NEAREST) -> None:
        data = pygame.image.tobytes(surf, "RGBA", True)
        if name in self.textures:
            tex, assigned_slot = self.textures[name]
            if tex.size == surf.get_size():
                tex.write(data)
                return
            else:
                tex.release()  
        tex = self.context._gl_context.gl_ctx.texture(surf.get_size(), 4)
        tex.filter = (filter, filter)
        tex.write(data)
        assigned_slot = slot if slot is not None else self.next_slot()
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
        self.update_quad()
        for name, (tex, slot) in self.textures.items():
            tex.use(slot)
            if name in self.shader_prog:
                self.shader_prog[name] = slot
        for name, value in self.uniforms.items():
            if name in self.shader_prog:
                self.shader_prog[name] = value
        self.vao.render()
        self.viewport = None 

    def update_quad(self) -> None:
        W, H = self.context.window.internal_size 

        if self.viewport is not None:
            ox, oy, sw, sh = self.viewport
        elif self.textures:
            tex, _ = next(iter(self.textures.values()))
            sw, sh = tex.size
            ox, oy = 0, 0
        else:
            x1, y1, x2, y2 = -1, -1, 1, 1
            self.vbo.write(nodex.make_quad(x1, y1, x2, y2).tobytes())
            return

        x1, y1, x2, y2 = nodex.pixels_to_ndc(ox, oy, sw, sh, W, H)
        self.vbo.write(nodex.make_quad(x1, y1, x2, y2).tobytes())