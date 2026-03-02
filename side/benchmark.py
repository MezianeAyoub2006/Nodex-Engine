import time
from dataclasses import dataclass 

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..nodex.engine.core.context import Context

@dataclass 
class BenchmarkData:
    elapsed:float
    ratio:float
    order:int
    fps:int
    depth:int 

class Benchmark:
    def __init__(self, context, fps_target):
        self.context = context
        self.fps_target = fps_target
        self.budget = 1 / self.fps_target
        self._times:dict[str, float] = {}
        self._results:dict[str, BenchmarkData] = {}
        self._orders = {}
        self._depths = {}
        self.order = 0
        self.depth = 0
    
    def start(self, label):
        if label in self._times:
            raise KeyError(f"Cannot start the \"{label}\" benchmark twice")
        else:
            self._times[label] = time.perf_counter()
            self._depths[label] = self.depth 
            self._orders[label] = self.order
            self.order += 1
            self.depth += 1
            

    def end(self, label):
        self.bugdet = self.context.fps - self.fps_target
        if label in self._times:
            elapsed = time.perf_counter() - self._times[label] 
            ratio = (elapsed / self.context.dt) * 100
            self._results[label] = BenchmarkData(elapsed, ratio, self._orders[label], elapsed / (self.context.dt ** 2), self.depth)
            del self._times[label]
        else:
            raise KeyError(f"Unknown benchmark label \"{label}\"")
        self.depth -= 1
        
    def get(self, label):
        if label in self._results:
            result = self._results[label]
            del self._results[label]
            return result
        else:
            raise KeyError(f"Unknown benchmark label \"{label}\"")
        
    def clear(self, label):
        if label in self._results:
            del self._results[label]
        else:
            raise KeyError(f"Unknown benchmark label \"{label}\"")
    
    @property 
    def results(self):
        return self._results
    
    @property
    def target_fps(self):
        return self.fps_target

