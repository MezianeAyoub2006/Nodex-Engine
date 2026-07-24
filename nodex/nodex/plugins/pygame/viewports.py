from ...core.graphics.graphics import RenderTask, Graphics, RenderTask
from ...core.kernel.context import Context
from .settings import PygameSettings 
from ...core.kernel.service import Service
from ...core.kernel.phase import EnginePhase
from ...math import Rectangle 
from .viewport import PygameViewport 


class PygameViewports(Service): 
    _viewports: dict[str, PygameViewport] = {}

    @Service.update(sys_order = EnginePhase.PRE_FRAME)
    def update_before(cls):
        for viewport in PygameViewports._viewports.values():
            viewport.render()
    
    @staticmethod
    def create(name: str, order:float, shader_name:str = None, region: Rectangle = None):
        PygameViewports._viewports[name] = PygameViewport(Service.context, shader_name, order, region) 

    @staticmethod 
    def set_uniform(viewport_name: str, uniform:str, value):
        Service.context.shaders[PygameViewports.get(viewport_name).shader_name].set_uniform(uniform, value)

    @classmethod
    def get(cls, name: str) -> PygameViewport:
        return cls._viewports[name]
    
  
@Graphics.override(PygameSettings)
def draw_pygame(_: Context, task: RenderTask):
    settings:PygameSettings = task.settings
    PygameViewports.get(settings.viewport).surface.blit(
        task.drawable._internal, 
        settings.position)
