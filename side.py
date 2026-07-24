import nodex 


ffi = nodex._ndx_cffi.ffi 
lib = nodex._ndx_cffi.lib

BLACK = ffi.new("Color*", [0, 0, 0, 255])[0]

lib.SetTraceLogLevel(lib.LOG_NONE)
lib.SetConfigFlags(lib.FLAG_WINDOW_HIDDEN)
lib.InitWindow(500, 500, b"AAAA")

lib.BeginDrawing()
lib.ClearBackground(BLACK)  
lib.EndDrawing()

lib.ClearWindowState(lib.FLAG_WINDOW_HIDDEN)

while not lib.WindowShouldClose():
    lib.BeginDrawing()
    lib.ClearBackground(BLACK)
    lib.EndDrawing()

lib.CloseWindow()