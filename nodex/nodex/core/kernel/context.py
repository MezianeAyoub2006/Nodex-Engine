from .runtime import Runtime 
from .service import Service
from .event_bus import EventBus
from ..node import Node

class Context:
    def __init__(self, 
        virtual_size: tuple[int, int], 
        window_scale : int = 1, 
        vsync: bool = True, 
        caption: str = "Blank Shi", 
    ) -> None:
        Service.context = self 
        self._runtime = Runtime(self)
        self.events = EventBus(self)
        self.root = Node(self)

    @property
    def dt(self):
        return self._runtime.dt 

    def run(self):
        self._runtime.run()
         
    def fps(self):
        return self._runtime._clock.get_fps()
    
    def warning(self, type, message, priority: int):
        pass

    def start(self, node: Node):
        self.root.bind(node)