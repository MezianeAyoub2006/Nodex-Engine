import moderngl
import nodex

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..context import Context
    
class GlContext:
    def __init__(self, context : "Context"):
        self.context = context 
        self.gl_ctx = moderngl.create_context()
        self.gl_ctx.enable(moderngl.BLEND)
        self.gl_ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
        self.render_tex = self.gl_ctx.texture(self.context.window.internal_size, 4)
        self.render_tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.render_fbo = self.gl_ctx.framebuffer(color_attachments=[self.render_tex])
        self.pp_tex_a = self.gl_ctx.texture(self.context.window.internal_size, 4)
        self.pp_tex_b = self.gl_ctx.texture(self.context.window.internal_size, 4)
        self.pp_tex_a.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.pp_tex_b.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.pp_fbo_a = self.gl_ctx.framebuffer(color_attachments=[self.pp_tex_a])
        self.pp_fbo_b = self.gl_ctx.framebuffer(color_attachments=[self.pp_tex_b])
        self.pp_library = {}   
        self.post_process = set()

    def init_shader_pass(self):
        self.blit_pass = nodex.ShaderPass(self.context)
        self.blit_pass.textures["tex"] = (self.render_tex, 0)

    def register_effect(self, name, frag):
        self.pp_library[name] = nodex.ShaderPass(self.context, frag)

    def apply_post_process(self):
        active = [self.pp_library[n] for n in self.post_process if n in self.pp_library]
        if not active:
            self.blit_pass.textures["tex"] = (self.render_tex, 0)
            return

        fbos = [self.pp_fbo_a, self.pp_fbo_b]
        texs = [self.pp_tex_a, self.pp_tex_b]

        src_tex = self.render_tex
        for i, shader_pass in enumerate(active):
            dst_fbo = fbos[i % 2]
            dst_fbo.use()
            self.gl_ctx.clear(0, 0, 0)
            shader_pass.textures["tex"] = (src_tex, 0)
            shader_pass.render()
            src_tex = texs[i % 2]

        self.blit_pass.textures["tex"] = (src_tex, 0)

    def after_rendering(self):
        self.apply_post_process()
        self.gl_ctx.screen.use()
        W, H = self.context.window.screen.get_size()
        self.gl_ctx.viewport = (0, 0, W, H)
        self.gl_ctx.clear(0, 0, 0)
        if self.context.window.fullscreen:
            self.gl_ctx.viewport = self.context.window.fullscreen_viewport()
        self.blit_pass.render()

    def set_uniform(self, name, uniform, value):
        if name in self.pp_library:
            self.pp_library[name].set_uniform(uniform, value)

    def before_rendering(self):
        self.render_fbo.use()
        self.gl_ctx.viewport = (0, 0, *self.context.window.internal_size)
        self.gl_ctx.clear(0, 0, 0)