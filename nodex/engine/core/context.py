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

class Context:
    def __init__(self, resolution, window_scale = 1, vsync = True, loading_node = None):
        pygame.init()
        self.event_bus = EventBus()
        self.runtime = Runtime(self)    
        self.system = System(self)
        self.window = Window(self, resolution, window_scale, vsync)
        self._gl_context = GlContext(self)
        self._gl_context.init_shader_pass()
        self.scenes = nodex.engine.world.SceneManger(self)
        self.input = Input(self)
        self.assets = AssetsManager(self)
        self.sounds = nodex.engine.sounds.SoundManager(self)
        self.renderer = nodex.engine.Renderer(self)
        self.timer = 0
        self.loading_node = loading_node
    
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