import nodex, random
import numpy as np
import math

ctx = nodex.Context((256, 240), (3, 3), 1, 1000, "Test Nodex")


tex = nodex.Texture("bird.png")

t = 0
N = 2000

x = np.random.randint(0, 256, size = N).astype(np.float64)
y = np.random.randint(0, 240, size = N).astype(np.float64)

w = tex.width
h = tex.height 

max_x = 256 - w
max_y = 240 - h

@ctx.run()
def loop():
    global t, x, y
    t += ctx.dt
    if t > 1:
        print(ctx.fps)
        t = 0

    angle = (1 + math.sin(ctx.timer * 3) * 0.1)
    scale_x = tex.width * angle 
    scale_y = tex.height * angle

    for i in range(N):
        ctx.renderer.draw_full(
            tex,  
            0, 0, tex.width, tex.height,
            x[i], y[i], scale_x, scale_y, 
            scale_x / 2,
            scale_y / 2, 
            ctx.timer * 30, 
            255, 255, 255, 255
        )
    if ctx.keyboard.pressed(nodex.Key.F11):
        ctx.cffi.lib.Nx_ToggleFullscreen()
    if ctx.keyboard.pressed(nodex.Key.A):
        print(ctx.window.caption)