import pygame 

from ..abstract.window import AbstractWindow

class PygameModernglWindow(AbstractWindow):
    def _create_screen(self, scale:int = 1, vsync:bool = False) -> pygame.Surface:  
        if scale:
            self.offset = (0, 0)
            return pygame.display.set_mode(
                    (
                        self.virtual_size[0] * scale, 
                        self.virtual_size[1] * scale
                    ), 
                    pygame.OPENGL | pygame.DOUBLEBUF, 
                    vsync = vsync
                )
        else:
            fullscreen_viewport = self._fullscreen_viewport()
            self.offset = (
                fullscreen_viewport[0], 
                fullscreen_viewport[1]
            )
            return pygame.display.set_mode(
                self.screen_size, 
                pygame.OPENGL | pygame.DOUBLEBUF | pygame.FULLSCREEN, 
                vsync = vsync
            ) 
      
    def _fullscreen_viewport(self) -> tuple:
        ratio = self.virtual_size[0] / self.virtual_size[1]
        
        if self.screen_size[0] / self.screen_size[1] > ratio:
            fullscreen_y = self.screen_size[1]
            fullscreen_x = fullscreen_y * ratio
            offset_x = (self.screen_size[0] - fullscreen_x) / 2
            offset_y = 0
        else:
            fullscreen_x = self.screen_size[0]
            fullscreen_y = fullscreen_x / ratio
            offset_x = 0
            offset_y = (self.screen_size[1] - fullscreen_y) / 2
        
        return int(offset_x), int(offset_y), int(fullscreen_x), int(fullscreen_y)

    def __init__(self, virtual_size : tuple[int, int], scale : float, vsync : bool, caption : str):
        pygame.init()
        self._virtual_size = virtual_size
        self._window_scale = scale
        self._vsync = vsync
        print(self._vsync)
        info = pygame.display.Info()
        self.screen_size = (info.current_w, info.current_h) 
        self.screen = self._create_screen(self._window_scale, self._vsync)
        self.fullscreen = False
        self.set_caption(caption)
    
    def toggle_fullscreen(self) -> None:
        if self.fullscreen:
            self.screen = self._create_screen(self._window_scale, self._vsync)     
        else:
            self.screen = self._create_screen(None, self._vsync)  
        self.fullscreen = not self.fullscreen  
         
    def set_caption(self, caption : str) -> None:
        pygame.display.set_caption(caption)
        self._caption = caption

    @property
    def virtual_size(self) -> tuple[int, int]:
        return self._virtual_size
    
    @property 
    def scale(self) -> float:
        if self.fullscreen:
            return self._fullscreen_viewport()[2] / self._virtual_size[0]
        return self._window_scale

    @property
    def caption(self) -> str:
        return self._caption
    
    @property
    def is_fullscreen(self):
        return self.fullscreen
    
    def rescale(self, virtual_size = None, scale = None) -> None:
        pass
