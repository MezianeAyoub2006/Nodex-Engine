from .....build import cffi 
from dataclasses import dataclass

_TEMP_RECT = cffi.ffi.new("NxRect*")

@dataclass
class Rect:
    x: float
    y: float
    width: float
    height: float

def update_nx_rect(rect: Rect):
    _TEMP_RECT.x = rect.x
    _TEMP_RECT.y = rect.y
    _TEMP_RECT.width = rect.width
    _TEMP_RECT.height = rect.height
    return _TEMP_RECT 

