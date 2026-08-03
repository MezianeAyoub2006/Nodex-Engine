from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...kernel.context import Context
    from .texture import Texture
    
class Renderer:
    def __init__(self, context: Context):
        self.context = context
        self._queue = self.context._interface._rendering_queue 

    def draw_simple(self, texture: Texture, x: float, y: float): 
        idx = self._queue.count 
        task = self.context.cffi.ffi.addressof(self._queue.tasks[idx]) 
        task.type = self.context.cffi.lib.TASK_SIMPLE 
        s = task.simple
        s.texture = texture._ptr 
        s.pos_x = x 
        s.pos_y = y
        task.order = 0 
        self._queue.count += 1 




