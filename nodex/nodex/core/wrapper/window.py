from ....build import cffi 
from .backends import BACKENDS, Backend
from .interface import Interface

class Window:
    def __init__(self, 
        interface : Interface,
        virtual_size: tuple[int, int], 
        window_scale: tuple[int, int], 
        vsync: bool, 
        target_fps: int,
        caption : str, 
        backend : Backend
    ):
        cffi.lib.Nx_RegisterBackends()  
        cffi.lib.Nx_Init(
            BACKENDS[backend], 
            virtual_size[0], virtual_size[1],
            window_scale[0], window_scale[1],
            vsync, target_fps, 
            caption.encode('utf-8') 
        )  
        self._interface = interface 

    @property
    def should_close(self):
        return self._interface.ptr.read.flags.shouldClose

