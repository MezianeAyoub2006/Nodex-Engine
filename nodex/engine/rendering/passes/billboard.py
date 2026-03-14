import pygame 
import math
import bisect
import nodex 

from .world_pass import WorldPass 
from operator import itemgetter

SCALES = [i / 100 for i in range(1, 300)]

class BillboardPass(WorldPass):
    def __init__(self, context, frag_prog=None, settings=None):
        self.settings = settings
        self.draw_tasks = []
        self._cache = {}  
        self._frames_count = {}
        super().__init__(context, frag_prog)

    def _is_spritesheet(self, name):
        return f"{name}.0.0" in self.context.assets._assets

    def _num_frames(self, name):
        if name not in self._frames_count:
            self._frames_count[name] = sum(
                1 for k in self.context.assets._assets 
                if k.startswith(f"{name}.") and k.endswith(".0")
            )
        return self._frames_count[name]
    
    def _resolve_name(self, element, camera, world_pos, angle):
        if isinstance(element, str) and self._is_spritesheet(element):
            frame = nodex.angle_to_frame_index(camera, world_pos, self._num_frames(element), angle)
            return f"{element}.{frame}.0"
        return element

    def _quantize(self, scale):
        i = bisect.bisect_left(SCALES, scale)
        if i == 0:
            return SCALES[0]
        if i >= len(SCALES):
            return SCALES[-1]
        return SCALES[i] if abs(SCALES[i] - scale) < abs(SCALES[i-1] - scale) else SCALES[i-1]

    def _get_scaled(self, name, scale):
        quantized = self._quantize(scale) 
        key = (name, quantized)
        if key not in self._cache:
            surface = self.context.assets.get_image(name)
            w, h = surface.get_size()
            self._cache[key] = pygame.transform.scale(
                surface, (max(1, int(w * quantized)), max(1, int(h * quantized)))
            )
        return self._cache[key] 
    
    def draw(self, element, world_pos, angle = 0, anchor = (0.5, 1.0)):
        if len(world_pos) == 2:
            self.draw_tasks.append({"position" : world_pos, "surface" : element, "z" : float('inf')})

        camera = self.context.renderer.camera3D(self.settings["reference"])

        screen_pos, scale = nodex.world_to_screen((
            world_pos[0], world_pos[1], -world_pos[2]
        ), camera, self.context.window.internal_size)

        if screen_pos is None or not self.context.window.in_display(screen_pos):
            return
        
        if isinstance(element, pygame.Surface):
            w, h = element.get_size()
            scaled = pygame.transform.scale(element, (max(1, int(w * scale)), max(1, int(h * scale))))
        else:
            name = self._resolve_name(element, camera, world_pos, angle)
            scaled = self._get_scaled(name, scale)

        if scaled is None:
            return

        w, h = scaled.get_size()
        x = screen_pos[0] - w * anchor[0]
        y = screen_pos[1] - h * anchor[1]
        self.draw_tasks.append({"position": (x, y), "surface": scaled, "z": scale})

    def render(self):
        for task in sorted(self.draw_tasks, key=itemgetter("z")):
            super().draw(task["surface"], task["position"])
        self.draw_tasks.clear()
        super().render()