import pygame
import nodex

from .viewport_type import ViewportType 
from .shader_pass import ShaderPass
from .pygame_pass import PygamePass 
from .world_pass import WorldPass
from .mode7_pass import Mode7Pass

class Viewport:
    TASK_DISPATCH_TABLE = None
    def __init__(self, context : "nodex.Context", order, type : ViewportType, frag_prog = None, vert_prog = None, extra_data = None):
        self.context = context  
        self.type = type
        self.init_pass(frag_prog, vert_prog, extra_data) 
        self.tasks = []   
        self.order = order

    def add_task(self, task):
        self.tasks.append(task)

    def init_pass(self, frag_prog, vert_prog, extra_data):
        if self.type == ViewportType.BASIC:
            self._pass = ShaderPass(self.context, frag_prog, vert_prog) 
        elif self.type == ViewportType.PYGAME:
            self._pass = PygamePass(self.context, frag_prog, vert_prog)
        elif self.type == ViewportType.WORLD:
            self._pass = WorldPass(self.context, frag_prog)
        elif self.type == ViewportType.MODE7:
            self._pass = Mode7Pass(self.context, extra_data)

    
    def dispatch_tasks(self):
        for task in self.tasks:
            Viewport.TASK_DISPATCH_TABLE[type(task["content"])](self, task)
    
    def handle_pygame_rect(self, task):
        rect = task["content"]
        surface = pygame.Surface((rect.w, rect.h)) 
        surface.fill(task["color"]) 
        task["position"] = (rect.x, rect.y) 
        self.handle_pygame_surf(task | {"content": surface})
     
    def handle_pygame_surf(self, task):
        surface = task["content"] 
        if self.type == ViewportType.BASIC:
            self._pass.dump_pygame_surf(task["name"], surface, task["slot"])
        if self.type == ViewportType.PYGAME or self.type == ViewportType.MODE7:
            self._pass.blit(surface, task["position"])

        if self.type == ViewportType.WORLD:
            self._pass.draw(surface, task["position"])
        if self.type == ViewportType.MODE7:
            self._pass.blit(surface, task["position"])
    
    def render(self):
        self.dispatch_tasks()
        self._pass.render()
        self.tasks.clear() 
    
    def clear(self):
        self.tasks.clear()

Viewport.TASK_DISPATCH_TABLE = {
    pygame.Surface: Viewport.handle_pygame_surf,
    pygame.Rect: Viewport.handle_pygame_rect,
}