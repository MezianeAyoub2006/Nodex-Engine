from cffi import FFI
from pathlib import Path
from _parse import read_cdef_body

PROJECT_ROOT = Path(__file__).parent
NATIVE_ROOT = PROJECT_ROOT.parent / "native"
NODEX_INCLUDE = NATIVE_ROOT / "include"
NODEX_SRC = NATIVE_ROOT / "src"

ffibuilder = FFI()

include_directories = [str(NODEX_INCLUDE)] + [
    str(path) for path in NODEX_INCLUDE.rglob("*") if path.is_dir()
]

source_files = [
    str(path) for path in NODEX_SRC.rglob("*.c")
    ]

ffibuilder.set_source(
    "_ndx_cffi",
    """
    #include "raylib.h"
    #include "nodex.h"  
    """,
    sources=source_files,
    libraries=["raylib"],
    library_dirs=[str(PROJECT_ROOT)],
    include_dirs=include_directories,
)


ffibuilder.cdef(read_cdef_body(PROJECT_ROOT / "cdef.h"))

if __name__ == "__main__":
    ffibuilder.compile(verbose=True, tmpdir=str(PROJECT_ROOT))