import pygame 
import sys 
import nodex

from .system import System
from .runtime import Runtime 
from .event_bus import EventBus
from .input import Input
from .window import Window
from .gl_context import GlContext 
from .assets_manager import AssetsManager
from .shaders_manager import ShaderManager

class Context:
    def __init__(self, resolution, window_scale = 1, vsync = True, loading_node = None, benchmark_fps_target = 60):
        pygame.init()
        self.shaders = ShaderManager(self)
        self._load_shaders()
        self.event_bus = EventBus()
        self.window = Window(self, resolution, window_scale, vsync)
        self._gl_context = GlContext(self)
        self._gl_context.init_shader_pass()
        self.runtime = Runtime(self)    
        self.system = System(self)
       
        self.scenes = nodex.engine.world.SceneManger(self)
        self.input = Input(self)
        self.assets = AssetsManager(self)
        self.sounds = nodex.engine.sounds.SoundManager(self)
        self.renderer = nodex.engine.Renderer(self)
        
        self.timer = 0
        self.loading_node = loading_node

    def _load_shader(self, name, file):
        self.shaders.load(name, f"nodex/engine/rendering/glsl/{file}.glsl")

    def _load_shaders(self):
        self._load_shader("_mode7", "modes/mode7")
        self._load_shader("_world", "modes/world")
        self._load_shader("_fragment", "passthrough/fragment")
        self._load_shader("_vertex", "passthrough/vertex")
    
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