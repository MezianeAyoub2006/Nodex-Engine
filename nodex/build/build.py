from cffi import FFI
from pathlib import Path
from pipeline import expand_includes, filter_header, pipeline_end

PROJECT_ROOT = Path(__file__).parent

NATIVE_ROOT = PROJECT_ROOT.parent / "native"
INCLUDE = NATIVE_ROOT / "include"
SRC = NATIVE_ROOT / "src" 

ffibuilder = FFI()

include_directories = [ str(INCLUDE)] + [ 
    str(path) 
    for path in INCLUDE.rglob("*") 
    if path.is_dir() 
]

source_files = [ 
    str(path) 
    for path in SRC.rglob("*.c") 
]

ffibuilder.set_source(
    "_ndx_cffi",
    """
    #include "raylib.h"
    #include "nodex.h"  
    """,
    sources=source_files,
    libraries = ["raylib"],
    library_dirs = [str(PROJECT_ROOT / "libs")],
    include_dirs = include_directories,
)

if __name__ == "__main__":
    file = expand_includes(INCLUDE / "nodex.h", INCLUDE)
    Path(PROJECT_ROOT / "cdef.h").write_text(pipeline_end(filter_header(file)), encoding="utf-8") 
    ffibuilder.cdef((PROJECT_ROOT / "cdef.h").read_text(encoding="utf-8"))
    ffibuilder.compile(verbose=True, tmpdir=str(PROJECT_ROOT / "output"))


