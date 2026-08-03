from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...kernel.context import Context 

from ....dtypes import Vec2

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
            self.context.cffi.lib.Raylib_Get_Dt
        )

    def _assign_ptr(self):
        self._ptr = self.context._interface.window 
    
