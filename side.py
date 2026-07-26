import nodex 
import time 

ffi = nodex.cffi.ffi 
lib = nodex.cffi.lib

lib.Nx_RegisterBackends()
lib.Nx_Init(
    lib.Nx_GetBackendTable()[lib.NX_BACKEND_RAYLIB], 
    300,
    300,
    2.0,
    2.0,
    False,
    10000,
    b"HellAAA"
)

tex_ptr = ffi.new("NxTexture*")   
lib.Nx_TextureLoad(tex_ptr, b"nodex.png") 

x, y = 0, 0
t = time.perf_counter()
while not lib.WindowShouldClose(): 
    lib.Nx_RendererBeginFrame() 
    #lib.Nx_RendererClear(ffi.new("NxColor*", (255, 0, 0, 255))[0])
    #lib.Nx_RendererDraw(
    #    tex_ptr, 
    #    ffi.new("NxRect*", (0, 0, 512, 512))[0], 
    #    ffi.new("NxRect*", (0, 0, 100, 100))[0], 
    #    ffi.new("NxVector2*", (x, y))[0], 
    #    0,
    #    ffi.new("NxColor*", (255, 255, 255, 255))[0]
    #)
    #if (lib.Nx_KeyActive(lib.NX_K_RIGHT)):
    #    x -= 300 * lib.Nx_GetDt()
    #if (lib.Nx_KeyActive(lib.NX_K_LEFT)):
    #    x += 300 * lib.Nx_GetDt()
    #if (lib.Nx_KeyActive(lib.NX_K_UP)):
    #    y += 300 * lib.Nx_GetDt()
    #if (lib.Nx_KeyActive(lib.NX_K_DOWN)):
    #    y -= 300 * lib.Nx_GetDt() 
    lib.Nx_RendererEndFrame()
    if time.perf_counter() - t > 0.1:
        t = time.perf_counter()
        print(lib.Nx_GetFps())
