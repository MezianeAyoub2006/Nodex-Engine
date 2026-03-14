import impl 
import nodex
import random
import math


N_CLOUDS = 15
Y_MAX = 20
DISPLAY_X = 256

def generate_clouds(n, display_x, y_max, dist_x=32, dist_y=16):
    clouds = []
    attempts = 0
    while len(clouds) < n and attempts < n * 100:
        attempts += 1
        type_ = (random.randint(0, 2), random.randint(0, 1))
        pos   = (random.randint(-display_x, display_x * 2), random.randint(0, y_max))
        dist_ok = all(
            abs(pos[0] - c[1][0]) >= dist_x or abs(pos[1] - c[1][1]) >= dist_y
            for c in clouds
        )
        if dist_ok:
            clouds.append((type_, pos))
    return clouds

CLOUDS_BACK  = generate_clouds(N_CLOUDS, DISPLAY_X, Y_MAX)
CLOUDS_FRONT = generate_clouds(N_CLOUDS, DISPLAY_X, Y_MAX)

class Sky:
    def __init__(self, context: "nodex.Context"):
        self.context = context
        self.mountains = [impl.ParallaxLayer(self.context, "parallax1", 190), impl.ParallaxLayer(self.context, "parallax0", 195)]
        self.clouds_back = [
            impl.ParallaxObject(self.context, f"clouds.{type[0]}.{type[1]}", *pos, 193, cycle=DISPLAY_X * 3, auto_speed=3)
            for type, pos in CLOUDS_BACK
        ]
        self.clouds_front = [
            impl.ParallaxObject(self.context, f"clouds.{type[0]}.{type[1]}", *pos, 200, cycle=DISPLAY_X * 3, auto_speed=3)
            for type, pos in CLOUDS_FRONT
        ]
        self.island = impl.ParallaxObject(self.context, "island", 0, 0, 204, repeat = False)
        self.boats = impl.ParallaxObject(self.context, "boats", 0, 0, 204, repeat = False)
        self.iceberg = impl.ParallaxObject(self.context, "iceberg", 600, 0, 204, repeat = False)
        self.iceberg1 = impl.ParallaxObject(self.context, "iceberg1", 835, 0, 204, repeat = False)
        self.iceberg2 = impl.ParallaxObject(self.context, "iceberg2", 400, 0, 204, repeat = False)
    

    def update(self, cam):
        self.context.renderer.draw("background", "sky")
        for cloud in self.clouds_back:   
            cloud.draw(cam, "background")
        for mountain in self.mountains:
            mountain.draw(cam)
        for cloud in self.clouds_front:  
            cloud.draw(cam, "background")
        self.island.draw(cam, "background")
        self.boats.draw(cam, "background")
        self.iceberg.draw(cam, "background")
        self.iceberg1.draw(cam, "background")
        self.iceberg2.draw(cam, "background")
