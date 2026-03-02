from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .context import Context

class ShaderManager:
    def __init__(self, context : "Context"):
        self.context = context 
        self._shaders = {}
    
    def load(self, name, path):
        with open(path, "r", encoding="utf-8") as f:
            self._shaders[name] = f.read() 

    def get(self, name):
        if name in self._shaders:
            return self._shaders[name]
        raise KeyError(f"Uknown shader \"{name}\"")
        
