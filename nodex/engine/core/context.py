import pygame 
import sys 
import nodex.engine

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
        self.gl_context = GlContext(self)
        self.gl_context.init_shader_pass()
        self.scene_manager = nodex.engine.world.SceneManger(self)
        self.input = Input(self)
        self.assets_manager = AssetsManager(self)
        self.sound_manager = nodex.engine.sound.SoundManager(self)
        self.timer = 0
        self.loading_node = loading_node

    def load_image(self, name, path, scale = (1, 1)):
        self.assets_manager.load_image(name, path, scale) 
    
    def load_spritesheet(self, name, path, tile_size, scale = (1, 1)):
        self.assets_manager.load_spritesheet(name, path, tile_size, scale)
    
    def get_image(self, name):
        return self.assets_manager.get_image(name)
    
    def get_spritesheet(self, name):
        return self.assets_manager.get_spritesheet(name)

    def load_sound(self, name, path):
        self.sound_manager.load_sound(name, path)

    def get_sound(self, name, copy = True):
        return self.sound_manager.get_sound(name, copy)

    def add_game_node(self, game_node, scene=None):
        self.scene_manager.add_game_node(game_node, scene)
    
    def switch_scene(self, scene):
        self.scene_manager.switch_scene(scene)

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