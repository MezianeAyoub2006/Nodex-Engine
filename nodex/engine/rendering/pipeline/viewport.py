import pygame
import nodex

from .viewport_type import ViewportType 

PASS_FACTORY = {
    ViewportType.BASIC : lambda ctx, frag, vert, _ : nodex.ShaderPass(ctx, frag, vert),
    ViewportType.PYGAME : lambda ctx, frag, vert, _ : nodex.PygamePass(ctx, frag, vert),
    ViewportType.WORLD : lambda ctx, frag, vert, _ : nodex.WorldPass(ctx, frag),
    ViewportType.MODE7 : lambda ctx, frag, vert, settings: nodex.Mode7Pass(ctx, settings),
    ViewportType.BILLBOARD : lambda ctx, frag, vert, settings: nodex.BillboardPass(ctx, frag, settings),
}

class Viewport:
    def __init__(self, context, name, order, type, frag_prog=None, vert_prog=None, settings=None):
        self.context = context  
        self.name = name
        self.type = type
        self.order = order
        self.tasks = []
        self.rendering_id = 0
        self.pass_ = PASS_FACTORY[type](context, frag_prog, vert_prog, settings)

    def add_task(self, task):
        self.tasks.append(task)

    def clear(self):
        self.tasks.clear()

    def render(self):
        for task in self.tasks:
            handler = TASK_DISPATCH_TABLE[type(task["content"])]
            handler(self, task)
            if self.type == ViewportType.BASIC:
                self.pass_.render()
            self.rendering_id += 1

        if self.type != ViewportType.BASIC:
            self.pass_.render()

        self.tasks.clear()
        self.rendering_id = 0

    def handle_pygame_rect(self, task):
        rect = task["content"]
        surface = pygame.Surface((rect.w, rect.h)) 
        surface.fill(task["color"]) 
        self.handle_pygame_surf(task | {"content": surface, "position": (rect.x, rect.y)})

    def handle_pygame_surf(self, task):
        surface = task["content"]
        if self.type == ViewportType.BASIC:
            pos = task["position"]
            self.pass_.set_viewport(pos[0], pos[1], surface.get_width(), surface.get_height())
            self.pass_.dump_pygame_surf(task["tex"], surface)
        elif self.type == ViewportType.PYGAME:
            self.pass_.blit(surface, task["position"])
        elif self.type == ViewportType.MODE7:
            self.pass_.draw(surface, task["position"])
        elif self.type == ViewportType.BILLBOARD:
            if "asset" in task:
                self.pass_.draw(task["asset"], task["position"], task["angle"])
            else:
                self.pass_.draw(surface, task["position"], task["angle"])

    def set_uniform(self, name, value):
        self.pass_.set_uniform(name, value)

TASK_DISPATCH_TABLE = {
    pygame.Surface: Viewport.handle_pygame_surf,
    pygame.Rect   : Viewport.handle_pygame_rect,  
}