import nodex, random
import numpy as np

ctx = nodex.Context(
    virtual_size = (256, 240),
    scale = (3, 3),
    flags = 1,
    target_fps = 1000,
    caption = "Test Nodex"
)

ctx.window.set_caption("HELLAA") 

tex = nodex.Texture("bird.png")

t = 0
N = 100

x = np.random.randint(0, 256, size=N).astype(np.float64)
y = np.random.randint(0, 240, size=N).astype(np.float64)
dx = np.random.uniform(-30, 30, size=N)
dy = np.random.uniform(-30, 30, size=N)

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

    dt = ctx.dt

    x += dx * dt
    y += dy * dt

    below_min_x = x < 0
    above_max_x = x > max_x
    dx[below_min_x | above_max_x] *= -1
    x[:] = np.clip(x, 0, max_x)

    below_min_y = y < 0
    above_max_y = y > max_y
    dy[below_min_y | above_max_y] *= -1
    y[:] = np.clip(y, 0, max_y)

    for i in range(N):
        ctx.renderer.draw_simple(tex, x[i], y[i])

    if ctx.keyboard.pressed(nodex.Key.F11):
        ctx.cffi.lib.Nx_ToggleFullscreen()