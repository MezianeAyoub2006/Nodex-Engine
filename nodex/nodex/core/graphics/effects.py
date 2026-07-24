from __future__ import annotations
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from ..kernel.context import Context 

class Effects:
    def __init__(self, context:Context):
        self.context = context 

    def register(self, effect_name: str, shader_name: str):
        self.context.renderer.register_effect(
            effect_name, 
            self.context.shaders[shader_name]
        )

    def activate(self, effect_name: str):
        self.context.renderer.activate_effect(effect_name)

    def deactivate(self, effect_name: str):
        self.context.renderer.deactivate_effect(effect_name)

    def is_active(self, effect_name: str):
        self.context.renderer.is_effect_active(effect_name) 

    def clear(self):
        self.context.renderer.clear_effects()

    def set_uniform(self, effect_name: str, uniform_name: str, value: Any):
        self.context.renderer.set_effect_uniform(
            effect_name, 
            uniform_name, 
            value
        )

    @property
    def active(self):
        return self.context.renderer.active_effects()

    