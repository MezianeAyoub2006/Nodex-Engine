import nodex 
import time 
import random

ffi = nodex.cffi.ffi 
lib = nodex.cffi.lib

lib.Nx_RegisterBackends()  

lib.Nx_Init(lib.Nx_GetBackendTable()[lib.NX_BACKEND_RAYLIB], 600, 600, 1.0, 1.0, True, 10000, b"HellAAA")

interface = lib.Nx_GetInterface()

tex_ptr = ffi.new("NxTexture*")
lib.Nx_TextureLoad(tex_ptr, b"bird.png")

N_BIRDS = 8000


for i in range(N_BIRDS):
    task = interface.drawQueueFast.drawTasks[i]
    task.texture = tex_ptr
    task.dest.width = tex_ptr.width
    task.dest.height = tex_ptr.height
    task.tint.r = 255
    task.tint.g = 255
    task.tint.b = 255
    task.tint.a = 255

def draw_tex_fast(x, y):
    ptr = interface.drawQueueFast.ptr
    dst = interface.drawQueueFast.drawTasks[ptr].dest
    dst.x = x
    dst.y = y
    interface.drawQueueFast.ptr = ptr + 1

class Bird:
    def __init__(self):
        self.x = random.randint(0, 600)
        self.y = random.randint(0, 600)
        self.dx = 0
        while (abs(self.dx) < 30):
            self.dx = random.randint(-100, 100)
        self.dy = 0
        while (abs(self.dy) < 30):
            self.dy = random.randint(-100, 100)

    def update(self, dt):  
        if interface.keyboardState.active[lib.NX_K_SPACE]:
            self.x += self.dx * dt
            self.y += self.dy * dt
        if self.x < 0 or self.x > 570 or self.y < 0 or self.y > 580:
            self.x = 300
            self.y = 300
    
        draw_tex_fast(self.x, self.y)


BIRDS = [Bird() for i in range(N_BIRDS)]

t = time.perf_counter()

while not interface.shouldClose:
    dt = interface.dt
    for bird in BIRDS:
        bird.update(dt)

    lib.Nx_Update()
   
    if time.perf_counter() - t > 1:
        t = time.perf_counter()
        print(interface.fps)