import time 
from typing import TYPE_CHECKING 

if TYPE_CHECKING:
    from .context import Context

from .phase import EnginePhase
from .service import Service  


class Runtime:
    def __init__(self, context : "Context", target_fps = 10000):
        self._context = context 
        self._target_fps = target_fps  
        self._lt = time.perf_counter()

    def run(self):
        def wrapper(f):
            while not self._context.wrapper.window.should_close:
                #self._context.renderer.before_frame()
                Service._update(EnginePhase.PRE_FRAME)  
                self._context.root._update_all()
                Service._update(EnginePhase.PRE_RENDER)
                f()
                self._context.root._update_all() 
                self._context.wrapper.interface.update() 
                Service._update(EnginePhase.POST_RENDER)
                #self._context.renderer.after_frame()
                Service._update(EnginePhase.POST_FRAME)
        return wrapper
        
    
    def quit(self):
        pass 

        