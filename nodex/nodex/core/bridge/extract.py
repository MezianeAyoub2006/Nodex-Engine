from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .cffi import Cffi
    
from ...dtypes import Vec2

def extract(cffi: Cffi, element):
    if isinstance(element, Vec2): 
        return cffi.ffi.new("NxVec2*", (element.x, element.y))[0] 
    