import pygame 
import sys 
import nodex.engine

from .system import System
from .runtime import Runtime 
from .event_bus import EventBus
from .input import Input
from .window import Window
from .gl_context import GlContext 
from .sounds import SoundLoader
from .mixer import Mixer, DynamicMixer

class Context:
    def __init__(self, resolution, window_scale = 1, vsync = True):
        pygame.init()
        self.event_bus = EventBus()
        self.runtime = Runtime(self)
        self.system = System(self)
        self.window = Window(self, resolution, window_scale, vsync)
        self.gl_context = GlContext(self)
        self.gl_context.init_shader_pass()
        self.scene_manager = nodex.engine.SceneManger(self)
        self.input = Input(self)
        self.sound_loader = SoundLoader(self)
        self.mixer = Mixer(self, 16, 1)
        self.dynamic_mixer = DynamicMixer(self, self.mixer, 320)
        self.timer = 0

    def add_game_node(self, game_node, scene=None):
        self.scene_manager.add_game_node(game_node, scene)

    def run(self):
        self.runtime.run()
    
    def quit(self):
        pygame.quit()
        sys.exit()

    def toggle_fullscreen(self):
        self.window.toggle_fullscreen()

    def set_caption(self, caption):
        pygame.display.set_caption(caption)

    @property 
    def active_keys(self):
        return self.input.active_keys 
    
    @property 
    def released_keys(self): 
        return self.input.released_keys 
    
    @property 
    def pressed_keys(self):
        return self.input.pressed_keys

    @property 
    def dt(self):
        return self.runtime.dt 
    
    @property 
    def fps(self):
        return self.runtime.fps
    
    @property 
    def internal_size(self):
        return self.window.internal_size
    
    @property
    def mouse_position(self):
        return self.input.mouse_position 
    
    @property 
    def window_scale(self):
        return self.window.window_scale