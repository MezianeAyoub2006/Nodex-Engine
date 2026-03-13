import pygame 
import sys 
import nodex

from .runtime import Runtime 
from .system.input import Input
from .system.window import Window
from .system.gl_context import GlContext 
from ..ressources.assets_manager import AssetsManager
from ..ressources.shaders_manager import ShaderManager
from ..rendering.pipeline import PostProcess
from ...misc.text.fonts_manager import FontsManager

class Context:
    def __init__(self, resolution, window_scale = 1, vsync = True):
        pygame.init()
        self.shaders = ShaderManager(self)
        self._load_shaders()
        self.window = Window(self, resolution, window_scale, vsync)
        self.window.set_caption(f"IceSkater FX")
        pygame.display.set_icon(pygame.image.load("logo.png").convert_alpha())
        self._gl_context = GlContext(self)
        self._gl_context.init_shader_pass()
        self.runtime = Runtime(self)    
        self.scenes = nodex.engine.world.SceneManager(self)
        self.input = Input(self)
        self.assets = AssetsManager(self)
        self.fonts = FontsManager(self)
        self.sounds = nodex.engine.sounds.SoundManager(self)
        self.renderer = nodex.engine.Renderer(self)
        self.post_process = PostProcess(self)
        self.overlay = nodex.engine.Renderer(self)
        self.overlay.add_viewport("transition", nodex.ViewportType.PYGAME, order = float("inf"))
        self.globals = {}
        self.timer = 0
        

    def _load_shader(self, name, file):
        self.shaders.load(name, f"nodex/engine/rendering/glsl/{file}.glsl")

    def _load_shaders(self):
        self._load_shader("_mode7", "modes/mode7")
        self._load_shader("_world", "modes/world")
        self._load_shader("_fragment", "passthrough/fragment")
        self._load_shader("_vertex", "passthrough/vertex")
        self._load_shader("_outline", "effects/outline")
        self._load_shader("_blur", "effects/blur")
        self._load_shader("_pixel", "effects/pixel")
    
    def run(self):
        self.runtime.run()
    
    def quit(self):
        pygame.quit()
        sys.exit()

    @property 
    def dt(self):
        return self.runtime.dt 
    
    @property 
    def fps(self):
        return self.runtime.fps