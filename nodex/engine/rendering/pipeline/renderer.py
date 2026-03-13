import nodex 
import pygame

from operator import attrgetter 
from nodex.misc.color import Color

from .viewport_type import ViewportType
from .viewport import Viewport
from ..cameras.camera2D import Camera2D
from ..cameras.camera3D import Camera3D


class Renderer:
    def __init__(self, context : "nodex.Context"):
        self.context = context 
        self.viewports: dict[str, Viewport] = {}
        self.next_order = 0 

    def add_viewport(self, name, type, fragment_shader=None, vertex_shader=None, settings=None, order=None):
        self.viewports[name] = Viewport(self.context, name, order if order is not None else self.next_order, type, fragment_shader, vertex_shader, settings)
        self.next_order += 1

    def get_viewport(self, name) -> Viewport:
        return self.viewports[name]

    def camera2D(self, viewport) -> Camera2D:
        vp = self.viewports[viewport]
        if vp.type == ViewportType.WORLD: 
            return vp.pass_.camera
        if vp.type == ViewportType.MODE7:
            return vp.pass_.dynamic_pass.camera

    def camera3D(self, viewport) -> Camera3D:
        vp = self.viewports[viewport]
        if vp.type == ViewportType.MODE7: 
            return vp.pass_.camera

    def draw(self, viewport, drawable = None, position = (0, 0), color = Color.WHITE, asset = None, angle = 0): 
        task = self.build_task(drawable, position=position, color=color, tex="tex", asset=asset, angle=angle)
        self.viewports[viewport].add_task(task)

    def draw_world(self, viewport, drawable = None, position = (0, 0), color = Color.WHITE, asset = None, angle = 0):
        camera = self.camera2D(viewport)
        world_position = (
            position[0] + camera.position.x, 
            position[1] - camera.position.y 
        )
        self.draw(viewport, drawable, world_position, color, asset, angle)

    def set_uniform(self, viewport, name, value):
        self.viewports[viewport].pass_.set_uniform(name, value)

    def clear(self):
        for viewport in self.viewports.values():
            viewport.clear()
    
    def render(self):
        for viewport in sorted(self.viewports.values(), key=attrgetter("order")):
            if viewport.tasks or viewport.type == ViewportType.MODE7:
                viewport.render()

    def build_task(self, drawable, **kwargs):
        task = {"content": drawable, "tex": kwargs["tex"], "angle": kwargs["angle"]}
        if "asset" in kwargs and kwargs["asset"] is not None:
            task["asset"] = kwargs["asset"]
        
        if isinstance(drawable, pygame.Rect):
            task["color"] = kwargs["color"]
        elif isinstance(drawable, pygame.Surface):
            task["position"] = kwargs["position"] 
        elif isinstance(drawable, str):
            return self.build_task(self.context.assets.get_image(drawable), **kwargs)
        elif drawable is None:
            return self.build_task(pygame.Surface((0, 0)), **kwargs)
            
        return task