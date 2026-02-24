import pygame 
import sys 
import nodex.engine

from .system import System
from .runtime import Runtime 
from .event_bus import EventBus

class Context:
    def __init__(self, resolution, window_scale = 1, vsync = True):
        pygame.init()
        self.event_bus = EventBus()
        self.runtime = Runtime(self)
        self.system = System(self)
        self.window = nodex.engine.Window(self, resolution, window_scale, vsync)
        self.gl_context = nodex.engine.GlContext(self)
        self.gl_context.init_shader_pass()
        self.scene_manager = nodex.engine.SceneManger(self)

    def add_game_node(self, game_node, scene=None):
        self.scene_manager.add_game_node(game_node, scene)

    def run(self):
        self.runtime.run()
    
    def quit(self):
        pygame.quit()
        sys.exit()

    def toggle_fullscreen(self):
        self.window.toggle_fullscreen()

    @property 
    def dt(self):
        return self.runtime.dt 
    
    @property 
    def fps(self):
        return self.runtime.fps
    
    @property 
    def internal_size(self):
        return self.window.internal_size