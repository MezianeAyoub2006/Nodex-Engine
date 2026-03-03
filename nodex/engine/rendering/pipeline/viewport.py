import pygame
import nodex

from .viewport_type import ViewportType 

class Viewport:
    TASK_DISPATCH_TABLE = None
    def __init__(self, context : "nodex.Context", name, order, type : ViewportType, frag_prog = None, vert_prog = None, extra_data = None):
        self.context = context  
        self.name = name
        self.type = type
        self.init_pass(frag_prog, vert_prog, extra_data) 
        self.tasks = []   
        self.order = order
        self.rendering_id = 0

    def add_task(self, task):
        self.tasks.append(task)

    def init_pass(self, frag_prog, vert_prog, extra_data):
        if self.type == ViewportType.BASIC:
            self._pass = nodex.ShaderPass(self.context, frag_prog, vert_prog) 
        elif self.type == ViewportType.PYGAME:
            self._pass = nodex.PygamePass(self.context, frag_prog, vert_prog)
        elif self.type == ViewportType.WORLD:
            self._pass = nodex.WorldPass(self.context, frag_prog)
        elif self.type == ViewportType.MODE7:
            self._pass = nodex.Mode7Pass(self.context, extra_data)
    
    def dispatch_tasks(self):
        for task in self.tasks:
            Viewport.TASK_DISPATCH_TABLE[type(task["content"])](self, task)
            if self.type == ViewportType.BASIC:
                self._pass.render()
            self.rendering_id += 1

    def render(self):
        self.dispatch_tasks()
        if self.type != ViewportType.BASIC:
            self._pass.render()
        self.tasks.clear()
        self.rendering_id = 0
        
    def handle_pygame_rect(self, task):
        rect = task["content"]
        surface = pygame.Surface((rect.w, rect.h)) 
        surface.fill(task["color"]) 
        task["position"] = (rect.x, rect.y) 
        self.handle_pygame_surf(task | {"content": surface})
     
    def handle_pygame_surf(self, task):
        surface = task["content"]      
        if self.type == ViewportType.BASIC:
            pos = task["position"]
            self._pass.set_viewport(pos[0], pos[1], surface.get_width(), surface.get_height())
            self._pass.dump_pygame_surf(task["tex"], surface)
        if self.type == ViewportType.PYGAME:
            self._pass.blit(surface, task["position"])
        if self.type == ViewportType.WORLD or ViewportType.MODE7:
            self._pass.draw(surface, task["position"])
        

    
 
    def clear(self):
        self.tasks.clear()

Viewport.TASK_DISPATCH_TABLE = {
    pygame.Surface: Viewport.handle_pygame_surf,
    pygame.Rect: Viewport.handle_pygame_rect,
}