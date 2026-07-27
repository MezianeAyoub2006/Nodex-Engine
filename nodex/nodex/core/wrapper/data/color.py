from .....build import cffi 
from dataclasses import dataclass

_TEMP_COLOR = cffi.ffi.new("NxColor*")

@dataclass
class Color:
    r: int
    g: int 
    b: int 
    a: int

def update_nx_color(color: Color):
    _TEMP_COLOR.r = color.r 
    _TEMP_COLOR.g = color.g
    _TEMP_COLOR.b = color.b 
    _TEMP_COLOR.a = color.a 
    return _TEMP_COLOR
