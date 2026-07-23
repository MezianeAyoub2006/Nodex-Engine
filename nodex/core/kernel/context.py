from ..backend import Backend, BACKENDS
from ..graphics import Graphics
from .runtime import Runtime 
from ..ressources import ShaderManager
from .service import Service
from .event_bus import EventBus
from ..node import Node

class Context:
    def __init__(self, 
        virtual_size: tuple[int, int], 
        window_scale : int = 1, 
        vsync: bool = True, 
        caption: str = "Blank Shi", 
        backend = Backend.PYGAME_MODERNGL
    ) -> None:
        Service.context = self 
        self._backend_types = BACKENDS[backend]
        self.window = self._backend_types.window(virtual_size, window_scale, vsync, caption)
        self.renderer = self._backend_types.renderer(self.window) 
        self._keyboard = self._backend_types.keyboard() 
        self._runtime = Runtime(self)
        self.shaders = ShaderManager(self)
        self.graphics = Graphics(self)
        self.events = EventBus(self)
        self.root = Node(self)

    @property
    def keyboard(self):
        return self._keyboard 

    @property
    def texture_type(self):
        return self._backend_types.texture 
    
    @property
    def shader_type(self):
        return self._backend_types.shader 
         
    def run(self):
        return self._runtime.run   
    
    def fps(self):
        return self._runtime._clock.get_fps()
    
    def warning(self, type, message, priority: int):
        pass