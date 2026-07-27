import nodex 
import random
import gc
gc.disable()  


W, H = 1280, 720
NUM_BIRDS = 1000
SCALE = 3

ctx = nodex.Context((W, H), (1, 1), True, 1000)  

texture = nodex.Texture("bird.png")

scaled_w = texture.width * SCALE
scaled_h = texture.height * SCALE

pos = [[random.randint(0, 500), random.randint(0, 500)] for _ in range(NUM_BIRDS)]
speeds = [[random.randint(-300, 300), random.randint(-300, 300)] for _ in range(NUM_BIRDS)]
angles = [random.randint(0, 360) for _ in range(NUM_BIRDS)]

source_rect = nodex.Rect(0, 0, texture.width, texture.height)
origin_vec = nodex.Vec2(0, 0)
tint_color = nodex.Color(255, 255, 255, 255)

t = 0 

@ctx.run()
def loop():
    global t 
    dt = ctx.wrapper.interface.dt
    renderer = ctx.wrapper.renderer

    for i in range(NUM_BIRDS):
        pos[i][0] += speeds[i][0] * dt
        pos[i][1] += speeds[i][1] * dt
        angles[i] += dt * 200

        if pos[i][0] < 0:
            pos[i][0] = 1
            speeds[i][0] *= -1
        elif pos[i][0] > W - scaled_w:
            pos[i][0] = W - scaled_w - 1
            speeds[i][0] *= -1

        if pos[i][1] < 0:
            pos[i][1] = 1
            speeds[i][1] *= -1
        elif pos[i][1] > H - scaled_h:
            pos[i][1] = H - scaled_h - 1
            speeds[i][1] *= -1

        renderer.draw(
            texture,
            nodex.Rect(0, 0, texture.width, texture.height), 
            nodex.Rect(int(pos[i][0]), int(pos[i][1]), scaled_w, scaled_h),  
            nodex.Vec2(scaled_w / 2, scaled_h / 2), 
            angles[i], 
            0, 
            tint_color, 
        )
    t += ctx.wrapper.interface.dt 
    if t > 3:
        t= 0
        print(ctx.wrapper.interface.fps)

    if nodex.cffi.lib.Nx_KeyPressed(nodex.cffi.lib.NX_K_SPACE):
        pass