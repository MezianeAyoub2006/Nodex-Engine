from .texture import Texture
from .interface import Interface

from .data.rect import Rect
from .data.color import Color
from .data.vec2 import Vec2

import numpy as np

class Renderer:
    def __init__(self, interface: Interface):
        interface_ptr = interface._interface
        self._queue = interface_ptr.drawQueue
        self._fast_queue = interface_ptr.drawQueueFast
        self._tasks = self._queue.drawTasks
        self._fast_tasks = self._fast_queue.drawTasks
        self._interface_ptr = interface_ptr

    def increment(self):
        self._queue.ptr += 1

    def increment_fast(self):
        self._fast_queue.ptr += 1

    @property
    def current_task(self):
        return self._tasks[self._queue.ptr]

    @property
    def current_task_fast(self):
        return self._fast_tasks[self._fast_queue.ptr]
    
    def draw(
        self,
        texture: Texture,
        source: Rect,
        dest: Rect,
        origin: Vec2,
        rotation: float,
        z_index: float,
        tint: Color,
    ):
        idx = self._queue.ptr
        task = self._tasks[idx]
        task.texture = texture._ptr
        task.rotation = rotation
        task.z_index = z_index
        task.arrival_id = idx
        task_source = task.source
        task_source.x = source.x
        task_source.y = source.y
        task_source.width = source.width
        task_source.height = source.height
        task_dest = task.dest
        task_dest.x = dest.x
        task_dest.y = dest.y
        task_dest.width = dest.width
        task_dest.height = dest.height
        task_origin = task.origin
        task_origin.x = origin.x
        task_origin.y = origin.y
        task_tint = task.tint
        task_tint.r = tint.r
        task_tint.g = tint.g
        task_tint.b = tint.b
        task_tint.a = tint.a
        self._queue.ptr = idx + 1

    def draw_fast(
        self,
        texture: Texture,
        dest: Rect,
        tint: Color,
        z_index: float = 0,
    ):
        idx = self._fast_queue.ptr
        task = self._fast_tasks[idx]
        task.texture = texture._ptr
        task.z_index = z_index
        task.arrival_id = idx
        task_dest = task.dest
        task_dest.x = dest.x
        task_dest.y = dest.y
        task_dest.width = dest.width
        task_dest.height = dest.height
        task_tint = task.tint
        task_tint.r = tint.r
        task_tint.g = tint.g
        task_tint.b = tint.b
        task_tint.a = tint.a
        self._fast_queue.ptr = idx + 1

  