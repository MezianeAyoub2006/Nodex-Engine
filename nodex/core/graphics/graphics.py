from typing import TYPE_CHECKING, Any, Callable
from dataclasses import dataclass 
from ..backend import AbstractShader, AbstractRenderer
if TYPE_CHECKING: from ..kernel.context import Context 
from .settings import settings, SettingsType

@dataclass
class RenderTask:
    drawable: Any
    settings: SettingsType
    order: float 
    shader: AbstractShader

START_TASK_MAP = { 
    settings.texture: lambda ctx, task:
        ctx.renderer.draw_texture(
            texture = task.drawable, 
            position = task.settings.position, 
            shader = task.shader
        ), 

    settings.rectangle: lambda ctx, task:
        ctx.renderer.draw_rectangle(
            rectangle = task.drawable,
            color = task.settings.color,
            shader = task.shader
        )   
}   

class Graphics:
    _task_map = START_TASK_MAP.copy()

    @staticmethod
    def override(setting_type : type[SettingsType]):
        def wrapper(f):
            Graphics._task_map[setting_type] = f 
            return f
        return wrapper

    def __init__(self, context : "Context") -> None:
        self._context = context
        self._tasks: list[RenderTask] = []
        self._renderer = self._context.renderer
        self._shaders = self._context.shaders
        self._bg_color = (0, 0, 0, 0) 
    
    @property
    def _current_shader(self) -> AbstractShader | None:
        return self._shaders._stack[-1] if self._shaders._stack else None

    def draw(self, drawable: Any, settings: SettingsType, order: float) -> None:
        if isinstance(drawable, self._context.texture_type.INJECTION_TYPE):
            drawable = self._context.texture_type.inject(drawable)
        self._tasks.append(RenderTask(
            drawable = drawable, 
            settings = settings, 
            order = order, 
            shader = self._current_shader
        )) 

    def _update(self) -> None:
        self._renderer.fill(self.bg_color)
        for task in sorted(self._tasks, key = lambda t: t.order):
            Graphics._task_map[type(task.settings)](self._context, task)
        self._tasks.clear()

    @property
    def bg_color(self) -> tuple[int, int, int, int]:  
        return self._bg_color 
    
    @bg_color.setter 
    def bg_color(self, color: tuple[int, int, int, int]):
        self._bg_color = color