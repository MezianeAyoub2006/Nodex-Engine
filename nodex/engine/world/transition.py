import pygame 
import math 
import nodex 

def bump(t):
    return math.sin(t * math.pi)

class Transition:
    def __init__(self, context : "nodex.Context"):
        self.context = context
        self.timer = 0
        self.duration = 0
        self.done = True
        self.scene = None
        self.callback = lambda: None
        self.callback_settings = ()
        self.effects = None

    def start(self, scene, duration, effects = ("circle",), callback=lambda: None, callback_settings=()):
        self.timer = duration
        self.duration = duration
        self.done = False
        self.scene = scene
        self.callback = callback
        self.callback_settings = callback_settings
        self.effects = effects

    def update(self):
        if self.done:
            return
        if self.timer > 0:
            self.timer -= self.context.dt
            if self.effects:
                self.handle_effect()
        if self.timer < 0:
            self.done = True

    def handle_effect(self):
        if "circle" in self.effects:
            self.circle_effect()
        if "fade" in self.effects:
            self.fade_effect()
        if "wave" in self.effects:
            self.wave_effect()
        
    def circle_effect(self):
        window_size = self.context.window.internal_size
        surface = pygame.Surface(window_size, pygame.SRCALPHA)
        t = self.timer / self.duration
        pygame.draw.circle(surface, nodex.Color.BLACK, (window_size[0] / 2, window_size[1] / 2), bump(t) * window_size[0])
        self.context.overlay.draw("transition", surface)
    
    def fade_effect(self):
        t = self.timer / self.duration
        surface = pygame.Surface(self.context.window.internal_size, pygame.SRCALPHA)
        surface.fill((0, 0, 0)) 
        surface.set_alpha(bump(t) * 255)
        self.context.overlay.draw("transition", surface)

    def wave_effect(self):
        t = self.timer / self.duration 
        self.context.post_process.enable_effect("fx")
        self.context.post_process.set_uniform("fx", "amplitude", bump(t) * 0.075) 
        self.context.post_process.set_uniform("fx", "time", self.context.timer)


    @property
    def progress(self):
        t = 1.0 - (self.timer / self.duration)
        return t * t * (3 - 2 * t)

    @property
    def halfway(self):
        return self.timer <= self.duration / 2
