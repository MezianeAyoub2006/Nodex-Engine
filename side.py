import nodex 

ffi = nodex._ndx_cffi.ffi 
lib = nodex._ndx_cffi.lib


lib.Nx_RegisterBackends()
lib.Nx_Init(
    lib.backendTable[lib.NX_BACKEND_RAYLIB], 
    300,
    300,
    2.0,
    2.0,
    True,
    b"HellAAA"
)


