from .....build import cffi
from ..status import check_native_error
from .exceptions import TextureException
from ..exceptions import NativeException

class Texture:
    def __init__(self, path: str):
        raw = cffi.lib.Nx_Texture_Load(path.encode("utf-8"))
        try:
            check_native_error()
        except NativeException:
            raise TextureException(f"\nfailed to load \"{path}\" (invalid path).")
        self._ptr = cffi.ffi.gc(raw, cffi.lib.Nx_Texture_Unload)

    @property
    def width(self):
        return self._ptr.size.x

    @property
    def height(self):
        return self._ptr.size.y