import moderngl
import pygame

from ....math import Rectangle 
from ..abstract import AbstractRenderer
from .window import PygameModernglWindow
from .shader import PygameModernglShader
from .texture import PygameModernglTexture
from .helpers import make_quad, load_shader

def convert_color(color: tuple[int, int, int, int]):
    # convert Nodex format colors, to moderngl/GPU format 
    # (from 0-255 int to 0-1 float)
    return (
        color[0] / 255, 
        color[1] / 255,
        color[2] / 255,
        color[3] / 255 
    )

class PygameModernglRenderer(AbstractRenderer):
    
    GPU_BACK = True

    def __init__(self, window: PygameModernglWindow):
        self._window = window
        self._gl = moderngl.create_context()
        self._gl.enable(moderngl.BLEND)
        self._gl.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA

        self.render_tex = self._gl.texture(self._window.virtual_size, 4)

        # NEAREST_NEIGHBOR scaling method
        self.render_tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.render_fbo = self._gl.framebuffer(color_attachments=[self.render_tex])

        # we render centered textures.
        self._vbo = self._gl.buffer(make_quad(-0.5, -0.5, 0.5, 0.5).tobytes())

        # we change nothing from the final texture which is processed using 
        # ping pong, but at the end, the passthrough shader is applied 
        self._blit_shader = PygameModernglShader(
            self,
            load_shader("shaders/passthrough_fragment.glsl"),
            load_shader("shaders/passthrough_vertex.glsl")
        )


        # used to handle transformations such as scale, tint, ..
        self._transform_shader = PygameModernglShader(
            self, 
            load_shader("shaders/transform_fragment.glsl"),
            load_shader("shaders/transform_vertex.glsl") 
        )

        # ping pong setup
        self.pp_tex_a = self._gl.texture(self._window.virtual_size, 4)
        self.pp_tex_b = self._gl.texture(self._window.virtual_size, 4)
        self.pp_tex_a.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.pp_tex_b.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.pp_fbo_a = self._gl.framebuffer(color_attachments=[self.pp_tex_a])
        self.pp_fbo_b = self._gl.framebuffer(color_attachments=[self.pp_tex_b])

        # post processing data
        self.pp_library: dict[str, PygameModernglShader] = {}
        self.post_process: list[str] = []

    def before_frame(self):
        self.render_fbo.use()
        # everything is rendered based of the virtual size
        self._gl.viewport = (0, 0, *self._window.virtual_size)
        self._gl.clear(0, 0, 0)

    # applies post processing into the render texture, and returns the final processed texture
    def _apply_post_process(self) -> moderngl.Texture: 
        # we take every active post processing effect
        active = [self.pp_library[n] for n in self.post_process if n in self.pp_library]
        if not active:
            return self.render_tex

        fbos = [self.pp_fbo_a, self.pp_fbo_b]
        texs = [self.pp_tex_a, self.pp_tex_b]

        # we get the rendering texture
        src_tex = self.render_tex

        # ping pong rendering 
        for i, shader in enumerate(active):
            fbos[i % 2].use()
            self._gl.clear()
            shader._set_texture_gl("tex", src_tex)
            shader._render()
            src_tex = texs[i % 2]

        # we get the processed rendering texture
        return src_tex

    def after_frame(self):
        final_tex = self._apply_post_process()
        self._gl.screen.use()

        # render everything based on the real window size  
        self._gl.viewport = (0, 0, *self._window.size)
        self._gl.clear(0, 0, 0)
        if self._window.fullscreen:
            self._gl.viewport = self._window._fullscreen_viewport()

        # we render the processed texture 
        self._blit_shader._set_texture_gl("tex", final_tex)
        self._blit_shader._render()
        pygame.display.flip() 

    def draw_texture(self,
            texture: PygameModernglTexture,
            position: tuple[int, int],
            rotation: float = None,
            scale: tuple[float, float] = None,
            flip: tuple[bool, bool] = None,
            tint: tuple[int, int, int, int] = None,
            shader: PygameModernglShader = None
        ):
            # if no shader is specified, we use our transform shader 
            active_shader = shader or self._transform_shader

            # we set every uniform 
            active_shader.set_texture("tex", texture)
            active_shader.set_uniform("u_resolution", self._window.virtual_size)
            if tint:
                active_shader.set_uniform("u_tint", convert_color(tint))
            else:
                active_shader.set_uniform("u_tint", (1.0, 1.0, 1.0, 1.0))
            active_shader.set_uniform("u_position", position)
            active_shader.set_uniform("u_rotation", rotation or 0.0)
            tex_w, tex_h = texture.size
            final_scale = (
                tex_w * (scale[0] if scale else 1.0),
                tex_h * (scale[1] if scale else 1.0)
            )
            active_shader.set_uniform("u_scale", final_scale)
            flip = flip or (False, False)
            active_shader.set_uniform("u_flip", (
                -1.0 if flip[0] else 1.0,
                -1.0 if flip[1] else 1.0
            ))
            active_shader._render()

    def fill(self, color) -> None:
        self._gl.clear(*convert_color(color))

    def draw_rectangle(self, rectangle: Rectangle, color, filled : bool = False, shader: PygameModernglShader = None):
        tex = PygameModernglTexture.blank((
            rectangle.width, 
            rectangle.height 
        ))
        tex.fill(color) 
        self.draw_texture(tex, (
            rectangle.x,
            rectangle.y 
        ))
        pass

    def register_effect(self, effect_name: str, shader: PygameModernglShader) -> None:
        self.pp_library[effect_name] = shader

    def activate_effect(self, effect_name: str) -> None:
        if effect_name not in self.post_process:
            self.post_process.append(effect_name)

    def deactivate_effect(self, effect_name: str) -> None:
        if effect_name in self.post_process:
            self.post_process.remove(effect_name)

    def is_effect_active(self, effect_name: str) -> bool:
        return effect_name in self.post_process

    def active_effects(self) -> list[str]:
        return list(self.post_process)

    def clear_effects(self) -> None:
        self.post_process.clear()

    def set_effect_uniform(self, effect_name: str, uniform: str, value) -> None:
        if effect_name in self.pp_library:
            self.pp_library[effect_name].set_uniform(uniform, value)

    def release(self) -> None:
        self.render_tex.release()
        self.render_fbo.release()
        self.pp_tex_a.release()
        self.pp_tex_b.release()
        self.pp_fbo_a.release()
        self.pp_fbo_b.release()
        self._vbo.release()
        self._blit_shader.free()
        self._transform_shader.free()
        for shader in self.pp_library.values():
            shader.free()
        self._gl.release()  