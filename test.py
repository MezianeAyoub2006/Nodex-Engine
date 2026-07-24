import nodex 

ffi = nodex._ndx_cffi.ffi
lib = nodex._ndx_cffi.lib

lib.InitWindow(200, 200, b"Hello World")