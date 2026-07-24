import pygame 
import moderngl

from typing import Any, TYPE_CHECKING

from ..abstract.shader import AbstractShader 
from .helpers import load_shader
from .texture import PygameModernglTexture
if TYPE_CHECKING:
    from .renderer import PygameModernglRenderer

class PygameModernglShader(AbstractShader):

    _passthrough_shader = None

    def _next_slot(self) -> int:
        # returns an available GPU slot
        used = {slot for _, slot in self._textures.values()}
        slot = 0
        while slot in used:
            slot += 1
        return slot
    
    def _set_texture_raw(
        self,
        name: str,
        size: tuple[int, int],
        data: bytes,
        filter: int = moderngl.NEAREST
    ) -> None:
        # sets a texture from raw data, owned by this shader
        if name in self._textures:
            tex, assigned_slot = self._textures[name]
            if tex.size == size:
                tex.write(data)
                return
            tex.release()
            assigned_slot = self._next_slot()
        else:
            assigned_slot = self._next_slot()
        tex = self._gl.texture(size, 4)
        tex.filter = (filter, filter)
        tex.write(data)
        self._textures[name] = (tex, assigned_slot)
        self._owned_textures.add(name)

    def _dump_pygame_surf(self, name: str, surf: pygame.Surface, filter: int = moderngl.NEAREST) -> None:
        # sets a texture from a pygame surface
        data = pygame.image.tobytes(surf, "RGBA", True)
        self._set_texture_raw(name, surf.get_size(), data, filter)

    def _set_texture_gl(self, variable: str, source_tex: moderngl.Texture) -> None:
        # sets a borrowed moderngl texture (not owned by this shader)
        self._textures[variable] = (source_tex, self._next_slot())
        self._owned_textures.discard(variable)

    def _render(self):
        # renders the shader
        for name, (tex, slot) in self._textures.items():
            tex.use(slot)
            if name in self._shader_program:
                self._shader_program[name] = slot
        for name, value in self._uniforms.items():
            if name in self._shader_program:
                self._shader_program[name] = value
        self.vao.render()

    def __init__(self, renderer : "PygameModernglRenderer", fragment_shader: str = None, vertex_shader: str = None): 
        self._gl = renderer._gl 
        self._renderer = renderer
        self._textures: dict[str, tuple[moderngl.Texture, int]] = {}
        self._owned_textures: set[str] = set()
        self._uniforms: dict[str, Any] = {}
        self._shader_program = self._gl.program(
            vertex_shader = vertex_shader, 
            fragment_shader = fragment_shader 
        )
        # VBO is global to the renderer
        self.vao = renderer._gl.vertex_array(
            self._shader_program, 
            [(renderer._vbo, '2f 2f', 'in_pos', 'in_uv')]
        )
    
    @staticmethod
    def passthrough_shader(renderer: "PygameModernglRenderer") -> "PygameModernglShader": 
        if PygameModernglShader._passthrough_shader is None:
            PygameModernglShader._passthrough_shader = PygameModernglShader(
                renderer, 
                load_shader("shaders/passthrough_fragment.glsl"), 
                load_shader("shaders/passthrough_vertex.glsl")
            )
        return PygameModernglShader._passthrough_shader
        
    def set_uniform(self, variable: str, value) -> None:
        self._uniforms[variable] = value

    def set_texture(self, variable: str, texture: PygameModernglTexture) -> None:
        self._dump_pygame_surf(
            variable, 
            texture._internal, 
            moderngl.NEAREST 
        )

    def free(self):
        for name in self._owned_textures:
            tex, _ = self._textures[name]
            tex.release()
        self._textures.clear()
        self._owned_textures.clear()
        self.vao.release()
        self._shader_program.release()