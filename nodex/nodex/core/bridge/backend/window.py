from typing import TYPE_CHECKING
if TYPE_CHECKING: from ...kernel.context import Context 
from ....dtypes import Vec2
from .exceptions import WindowException 

class Window:
    def __init__(self, context : Context, 
            virtual_size: tuple[int, int],
            scale : tuple[float, float], 
            flags : int, 
            target_fps: int,
            caption : str
        ):     

        self.context = context  
   
        self.context.cffi.lib.Nx_Init(
            self.context.extract(Vec2(*virtual_size)),
            self.context.extract(Vec2(*scale)), 
            flags, 
            target_fps, 
            caption.encode("utf-8"),
            self.context.cffi.lib.Raylib_WindowDriver(),
            self.context.cffi.lib.Raylib_RendererDriver(), 
            self.context.cffi.lib.Raylib_TextureDriver(), 
            self.context.cffi.lib.Raylib_KeyboardDriver(),
            self.context.cffi.lib.Raylib_Get_Dt
        )    

        self.caption = caption 
        self.target_fps = target_fps 
        self.scale = scale
        self.virtual_size = virtual_size     

    @property
    def virtual_size(self):
        return self._virtual_size 

    @property
    def scale(self):
        return self._scale 

    @property
    def target_fps(self):
        return self._target_fps 

    @property
    def caption(self):
        return self._caption 

    @virtual_size.setter
    def virtual_size(self, value: tuple[int, int]):
        if value[0] < 1:
            raise WindowException("(window.virtual_size[0]): must be strictly positive.")
        if value[1] < 1:
            raise WindowException("(window.virtual_size[1]): must be strictly positive.")
        self._virtual_size = value
        self.context.cffi.lib.Nx_Window_SetVirtualSize(value)

    @scale.setter
    def scale(self, value: tuple[int, int]):
        if value[0] < 1:
            raise WindowException("(window.scale[0]): must be strictly positive.")
        if value[1] < 1:
            raise WindowException("(window.scale[1]): must be strictly positive.") 
        self._scale = value
        self.context.cffi.lib.Nx_Window_SetScale(value)

    @target_fps.setter
    def target_fps(self, value: int):
        if value < 1:
            raise WindowException("(window.target_fps): must be strictly positive.") 
        self._target_fps = value 
        self.context.cffi.lib.Nx_Window_SetTargetFps(value)

    @caption.setter 
    def caption(self, value : str):
        self._caption = value
        self.context.cffi.lib.Nx_Window_SetCaption(value.encode("utf-8"))

    def _assign_ptr(self):
        self._ptr = self.context._interface.window 
    
