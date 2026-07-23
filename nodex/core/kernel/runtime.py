import sys  
import pygame 
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .context import Context
from .phase import EnginePhase
from .service import Service  


class Runtime:
    def __init__(self, context : "Context", target_fps = 10000):
        pygame.init()
        self._context = context 
        self._clock = pygame.time.Clock()
        self._target_fps = target_fps  

    def run(self, f):
        def wrapper(*args, **kwargs):
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self._quit()       
                self._context.keyboard._listen() 
                self._context.renderer.before_frame()
                Service._update(EnginePhase.PRE_FRAME)  
                self._context.root._update_all()
                f(*args, **kwargs) 
                Service._update(EnginePhase.PRE_RENDER)
                self._context.graphics._update()
                Service._update(EnginePhase.POST_RENDER)
                self._context.renderer.after_frame()
                Service._update(EnginePhase.POST_RENDER)
                self._clock.tick(1000)  
        wrapper()
        return wrapper
    
    def _quit(self):
        pygame.quit()
        sys.exit()

        