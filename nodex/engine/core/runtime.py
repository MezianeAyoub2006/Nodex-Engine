import pygame
import time
import nodex

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .context import Context

class Runtime:
    def __init__(self, context : "Context"):
        pygame.mixer.init()
        self.context = context 
        self.clock = pygame.time.Clock()
        self.lt = time.perf_counter() 
        self.dt = 1    
    
    def _delta_time(self):
        self.dt = (time.perf_counter() - self.lt)  
        self.lt = time.perf_counter()

    def poll_sys_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.context.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.context.window.toggle_fullscreen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.context.input._mouse_pressed[0] = True 
                if event.button == 3:
                    self.context.input._mouse_pressed[1] = True
                
    def run(self):
        while True: 
            self.context.input.reset_mouse_pressed()   
            self._delta_time()
            self.context.input._handle_keyboard()
            
            self.poll_sys_events()
            self.context.scenes.update()
            self.context._gl_context.before_rendering() 
            self.context.renderer.render()
            self.context._gl_context.after_rendering()
            self.context.overlay.render()
            
            pygame.display.flip() 
            self.clock.tick(1000) 
            self.context.timer += self.dt 
            self.context.renderer.clear()
            self.context.sounds.update()
             

    @property
    def fps(self):
        return self.clock.get_fps()
    

    
