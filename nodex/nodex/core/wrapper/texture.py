from ....build import cffi 

class Texture:
    def __init__(self, path: str) -> None: 
        self._ptr = cffi.ffi.new("NxTexture*")
        cffi.lib.Nx_TextureLoad(self._ptr, path.encode("utf-8"))    
        self._ptr = cffi.ffi.gc(self._ptr, cffi.lib.Nx_TextureUnload)

    @property
    def width(self) -> int:
        return self._ptr.width 

    @property
    def height(self) -> int:
        return self._ptr.height