import nodex 
import random

ctx = nodex.Context(
    virtual_size = (500, 500),
    scale = (1, 1),
    flags = 0, 
    target_fps = 300, 
    caption = "Hello World"
)

tex = nodex.Texture("bird.png") 

x = 0    
t = 0 

@ctx.run()
def loop():
    global x, t
    for i in range(5000):
        ctx.renderer.draw_simple(tex, random.randint(0, 480), random.randint(0, 480))
    x += 100 * ctx.dt 
    t += ctx.dt 
    if t > 1:
        print(ctx.fps)
        t = 0
