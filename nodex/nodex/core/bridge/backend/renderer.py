from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...kernel.context import Context
    
class Renderer:
    __slots__ = ('context', '_queue', 'draw_simple', 'draw', 'draw_full')
    def __init__(self, context: Context):
        self.context = context
        self._queue = self.context._interface._rendering_queue

        lib = context.cffi.lib
        q = self._queue

        TASK_SIMPLE = lib.TASK_SIMPLE
        TASK_NORMAL = lib.TASK_NORMAL
        TASK_FULL = lib.TASK_FULL

        tasks = q.tasks  

        def draw_simple(texture, x, y):
            idx = q.count
            task = tasks[idx]
            task.type = TASK_SIMPLE
            t = task.simple
            t.texture = texture._ptr
            t.pos_x = x
            t.pos_y = y
            task.order = 0
            q.count = idx + 1

        def draw(texture, x, y, rotation=0, scale=1):
            idx = q.count
            task = tasks[idx]
            task.type = TASK_NORMAL
            t = task.normal
            t.texture = texture._ptr
            t.pos_x = x
            t.pos_y = y
            t.rotation = rotation
            t.scale = scale
            task.order = 0
            q.count = idx + 1

        def draw_full(texture, source, dest, origin_x, origin_y, rotation, color):
            idx = q.count
            task = tasks[idx]
            task.type = TASK_FULL
            t = task.full
            t.texture = texture._ptr

            t.source_x = source.x
            t.source_y = source.y
            t.source_w = source.w
            t.source_h = source.h

            t.dest_x = dest.x
            t.dest_y = dest.y
            t.dest_w = dest.w
            t.dest_h = dest.h

            t.origin_x = origin_x
            t.origin_y = origin_y

            t.tint_r = color.r
            t.tint_g = color.g
            t.tint_b = color.b
            t.tint_a = color.a

            t.rotation = rotation
            task.order = 0
            q.count = idx + 1

        self.draw_simple = draw_simple
        self.draw = draw
        self.draw_full = draw_full
