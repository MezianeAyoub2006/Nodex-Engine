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
        self._viewports:dict[str, Viewport] = {}
        self._overlay:dict[str, Viewport] = {}      
        self._order = 0 

    def _build_task(self, drawable, **kwargs):

        task = {"content" : drawable, "tex" : kwargs["tex"]}
        if "asset" in kwargs:
            task["asset"] = kwargs["asset"]
        
        if isinstance(drawable, pygame.Rect):
            task["color"] = kwargs["color"]
        elif isinstance(drawable, pygame.Surface):
            task["position"] = kwargs["position"] 
        elif isinstance(drawable, str):
            surface = self.context.assets.get_image(drawable)
            return self._build_task(surface, **kwargs)
        
        return task
    
    def add_viewport(self, name, type, fragment_shader=None, vertex_shader=None, settings=None, order=None):
        self._viewports[name] = Viewport(self.context, name, order if order is not None else self._order, type, fragment_shader, vertex_shader, settings)
        self._order += 1

    def draw(self, viewport, drawable, position = (0, 0), color = Color.WHITE, apply_offset = False, asset = None): 
        if apply_offset:
            camera = self.camera2D(viewport) 
            position = (
                position[0] + camera.position.x, 
                position[1] - camera.position.y 
            )
        task = self._build_task(drawable, position = position, color = color, tex = "tex", asset = asset)
    
        self._viewports[viewport].add_task(task)

    def clear(self):
        for viewport in self._viewports.values():
            viewport.clear()
    
    def render(self):
        for viewport in sorted(self._viewports.values(), key = attrgetter("order")):
            viewport.render()
    
    def camera2D(self, viewport) -> Camera2D:
        _viewport = self._viewports[viewport]
        if _viewport.type == ViewportType.WORLD: 
            return _viewport._pass.camera
        if _viewport.type == ViewportType.MODE7:
            return _viewport._pass.dynamic_pass.camera

    def camera3D(self, viewport) -> Camera3D:
        _viewport = self._viewports[viewport]
        if _viewport.type == ViewportType.MODE7: 
            return _viewport._pass.camera
        
        