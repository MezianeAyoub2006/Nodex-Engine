import moderngl
import nodex

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .context import Context
    

class GlContext:
    def __init__(self, context : "Context"):
        self.context = context 
        self._gl_ctx = moderngl.create_context()
        self._gl_ctx.enable(moderngl.BLEND)
        self._gl_ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
        self._render_tex = self._gl_ctx.texture(self.context.window.internal_size, 4)
        self._render_tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self._render_fbo = self._gl_ctx.framebuffer(color_attachments=[self._render_tex])

    def init_shader_pass(self):
        self._blit_pass = nodex.ShaderPass(self.context)
        self._blit_pass.textures["tex"] = (self._render_tex, 0)

    def before_rendering(self):
        self._render_fbo.use()
        self._gl_ctx.viewport = (0, 0, *self.context.window.internal_size)
        self._gl_ctx.clear(0, 0, 0)

    def after_rendering(self):
        self._gl_ctx.screen.use()
        W, H = self.context.window.screen.get_size()
        self._gl_ctx.viewport = (0, 0, W, H)
        self._gl_ctx.clear(0, 0, 0)

        if self.context.window.fullscreen:
            self._gl_ctx.viewport = self.context.window.fullscreen_viewport()
    
        self._blit_pass.render()