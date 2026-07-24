import sys  
import pygame 
import time
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
        self._lt = time.perf_counter()

    def _handle_dt(self):
        self._dt = time.perf_counter() - self._lt 
        self._lt = time.perf_counter()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._quit()    
            self._handle_dt()   
            self._context.keyboard._listen() 
            self._context.renderer.before_frame()
            Service._update(EnginePhase.PRE_FRAME)  
            self._context.root._update_all()
            Service._update(EnginePhase.PRE_RENDER)
            self._context.graphics._update()
            Service._update(EnginePhase.POST_RENDER)
            self._context.renderer.after_frame()
            Service._update(EnginePhase.POST_FRAME)
            self._clock.tick(1000)  

    @property
    def dt(self):
        return self._dt 
    
    def _quit(self):
        pygame.quit()
        sys.exit()

        