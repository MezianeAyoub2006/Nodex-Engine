from typing import TYPE_CHECKING
if TYPE_CHECKING: from ...kernel.context import Context 
from ....dtypes import Vec2
from .exceptions import WindowException 

class Window:
    def _check_exceptions(self, virtual_size, scale, flags, target_fps, caption): 
        if virtual_size[0] < 1:
            raise WindowException("(window.virtual_size[0]): must be strictly positive.")
        if virtual_size[1] < 1:
            raise WindowException("(window.virtual_size[1]): must be strictly positive.")
        if scale[0] < 1:
            raise WindowException("(window.scale[0]): must be strictly positive.")
        if scale[1] < 1:
            raise WindowException("(window.scale[1]): must be strictly positive.") 
        if target_fps < 1:
            raise WindowException("(window.target_fps): must be strictly positive.") 

    def __init__(self, context : Context, 
            virtual_size: tuple[int, int],
            scale : tuple[float, float], 
            flags : int, 
            target_fps: int,
            caption : str
        ):     
        self.context = context  
        self._check_exceptions(virtual_size, scale, flags, target_fps, caption)
   
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

    def set_caption(self, caption: str):
        self.context.cffi.lib.Nx_Window_SetCaption(caption.encode("utf-8"))  

    def set_target_fps(self, target_fps: int):
        if target_fps < 1:
            raise WindowException("(window.target_fps): must be strictly positive.") 
        self.context.cffi.lib.Nx_Window_SetTargetFps(target_fps)  

    def _assign_ptr(self):
        self._ptr = self.context._interface.window 
    
