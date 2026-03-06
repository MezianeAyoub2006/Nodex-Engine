import pygame 
import math

from .world_pass import WorldPass 
from operator import itemgetter

def world_to_screen(pos, camera, screen_size):
    if camera.position.z < 0:
        return None, None
    wx, wy = pos[:2]
    wz = pos[2] if len(pos) > 2 else 0.0
    dx = wx - camera.position.x
    dy = wy - camera.position.y
    cosA = math.cos(camera.rotation)
    sinA = math.sin(camera.rotation)
    xi = cosA * dx + sinA * dy
    yi = -sinA * dx + cosA * dy
    if yi <= 0.0001:
        return None, None
    scale = max(0.001, abs(camera.position.z))
    depth = scale / yi
    screenY = depth + camera.horizon_height
    uv_y = 1.0 - screenY
    uv_y -= (wz / yi)
    uv_x = xi / yi + 0.5
    w, h = screen_size
    return (uv_x * w, (1 - uv_y) * h), min(max(1/yi, 0.2), 12) / 4

SCALES = [i/100 for i in range(300)] 

class BillboardPass(WorldPass):
    def __init__(self, context, frag_prog = None, settings = None):
        self.settings = settings
        self.draw_tasks = []
        self.scaling_cache = {}
        super().__init__(context, frag_prog)


    def _get_scaled(self, element, scale):
        if isinstance(element, pygame.Surface):
            w, h = element.get_size()
            return pygame.transform.scale(element, (int(w * scale), int(h * scale)))
        if isinstance(element, str):
            if not element in self.scaling_cache:
                asset = self.context.assets.get_image(element)
                w, h = asset.get_size()
                self.scaling_cache[element] = {
                    i : pygame.transform.scale(asset, (w * i, h * i)) for i in SCALES
                }
            
            return self.scaling_cache[element][min(SCALES, key=lambda s: abs(s - scale))] 
        
            
    def draw(self, element, world_pos, anchor=(0.5, 1.0)):
        camera = self.context.renderer.camera3D(self.settings["reference"])
        if len(world_pos) == 2:
            return  
        
        screen_pos, scale = world_to_screen((
            world_pos[0],
            world_pos[1],
            -world_pos[2]
        ), camera, self.context.window.internal_size)

        if screen_pos is None:
            return
        
        scaled = self._get_scaled(element, scale)

        w, h = scaled.get_size()
        x = screen_pos[0] - w * anchor[0]
        y = screen_pos[1] - h * anchor[1]
        
        self.draw_tasks.append({"position" : (x, y), "surface" : scaled, "z" : scale})
        

           

    def render(self):
        for task in sorted(self.draw_tasks, key = itemgetter("z")):
            super().draw(task["surface"], task["position"])
        self.draw_tasks.clear()
        super().render()
        