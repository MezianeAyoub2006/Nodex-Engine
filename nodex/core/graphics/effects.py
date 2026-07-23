from __future__ import annotations
from ...core.kernel.context import Context 

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
        self.context.renderer.