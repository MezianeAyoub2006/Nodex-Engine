from .....build import cffi 
from dataclasses import dataclass

_TEMP_VEC2 = cffi.ffi.new("NxVector2*")

@dataclass
class Vec2:
    x: float 
    y: float

def update_nx_vec2(rect: Vec2):
    _TEMP_VEC2.x = rect.x
    _TEMP_VEC2.y = rect.y
    return _TEMP_VEC2 

