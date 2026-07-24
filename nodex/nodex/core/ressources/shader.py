from typing import TYPE_CHECKING
if TYPE_CHECKING: from ..kernel.context import Context
from contextlib import contextmanager
from ..backend import AbstractShader

class ShaderManager:
    def __init__(self, context : "Context"):
        self._context = context 
        self._stack:list[str] = []
        self._registry:dict[str, AbstractShader] = {}

    def load(self, name:str, fragment_path: str, vertex_path: str) -> None:
        with open(fragment_path, "r") as file:
            frag_prog = file.read()
        with open(vertex_path, "r") as file:
            vert_prog = file.read()
        self[name] = self._context._backend_types.shader(
            self._context.renderer,
            frag_prog, 
            vert_prog
        )
        
    def __setitem__(self, name:str, shader:AbstractShader):
        self._registry[name] = shader

    def __getitem__(self, item:str) -> AbstractShader:
        return self._registry[item]
    
    @contextmanager
    def apply(self, name: str):
        shader_obj = self[name]
        self._stack.append(shader_obj)
        try:
            yield shader_obj
        finally:
            self._stack.pop() 


