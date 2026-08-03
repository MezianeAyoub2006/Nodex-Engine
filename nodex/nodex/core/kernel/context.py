from ..bridge import Cffi, Interface, extract
from ..bridge.backend import Window
from ..bridge.backend import Renderer
from ..bridge.backend import Texture
from .runtime import Runtime


class Context:
    def __init__(self, 
            virtual_size: tuple[int, int],
            scale : tuple[float, float], 
            flags : int, 
            target_fps: int, 
            caption: str
        ):
        self.cffi = Cffi() 
        self.window = Window(self, 
            virtual_size, 
            scale, 
            flags, 
            target_fps, 
            caption
        )
        self._interface = Interface(self.cffi)
        self.window._assign_ptr()
        self.runtime = Runtime(self)
        self.renderer = Renderer(self) 

    @property 
    def dt(self):
        return self._interface.dt 

    @property
    def fps(self):
        return self._interface.fps 

    @property
    def timer(self):
        return self._interface.timer 

    def run(self): 
        return self.runtime.run()

    def extract(self, element):
        return extract(self.cffi, element)

