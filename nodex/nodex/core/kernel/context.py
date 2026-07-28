from .runtime import Runtime 
from .service import Service
from .event_bus import EventBus
from ..node import Node
from ..wrapper import Backend, Wrapper

class Context:
    def __init__(self, 
        virtual_size: tuple[int, int], 
        window_scale : tuple[int, int] = (1, 1), 
        vsync: bool = True, 
        target_fps = 10000, 
        caption: str = "Hello World", 
        backend = Backend.RAYLIB   
        
    ) -> None:
        Service.context = self 

        self.wrapper = Wrapper(
            self, 
            virtual_size = virtual_size, 
            window_scale = window_scale,
            target_fps = target_fps,  
            vsync = vsync, 
            caption = caption, 
            backend = backend
        )

        self._runtime = Runtime(self)
        self.events = EventBus(self)
        self.root = Node(self)

    @property
    def dt(self):
        return self.wrapper.interface.dt 

    @property     
    def fps(self):
        return self.wrapper.interface.dt  

    def run(self):
        return self._runtime.run()
    
    def warning(self, type, message, priority: int):
        pass

