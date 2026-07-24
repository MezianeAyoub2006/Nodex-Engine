from cffi import FFI
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
NATIVE_ROOT = PROJECT_ROOT.parent / "native"
NODEX_INCLUDE = NATIVE_ROOT / "include"
NODEX_SRC = NATIVE_ROOT / "src"

ffibuilder = FFI()

include_directories = [str(NODEX_INCLUDE)] + [
    str(path) for path in NODEX_INCLUDE.rglob("*") if path.is_dir()
]

ffibuilder.set_source(
    "_ndx_cffi",
    """
    #include "raylib.h"
    #include "nodex.h"  
    """,
    libraries=["raylib"],
    library_dirs=[str(PROJECT_ROOT)],
    include_dirs=include_directories, 
)

with open(PROJECT_ROOT / "cdef.h", "r") as file:
    ffibuilder.cdef(file.read())

if __name__ == "__main__":
    ffibuilder.compile(verbose=True, tmpdir=str(PROJECT_ROOT))