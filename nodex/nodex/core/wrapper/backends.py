from ....build import cffi 
from enum import Enum, auto 

class Backend(Enum):
    RAYLIB = auto()

BACKENDS = {
    Backend.RAYLIB : cffi.lib.Nx_GetBackendTable()[cffi.lib.NX_BACKEND_RAYLIB] 
}