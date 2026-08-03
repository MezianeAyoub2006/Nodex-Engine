import arcade
import numpy as np
import time

WIDTH, HEIGHT = 600, 600
N_OISEAUX = 6000
BOUNDS_MIN = 0.0
BOUNDS_MAX = 600.0

class BenchWindow(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Hello Some Shi")
        arcade.set_background_color(arcade.color.BLACK)

        self.sprite_list = arcade.SpriteList()

        for _ in range(N_OISEAUX):
            sprite = arcade.Sprite("bird.png", scale=2.0)
            self.sprite_list.append(sprite)

        self.positions = np.random.uniform(0, 600, size=(N_OISEAUX, 2)).astype(np.float32)
        self.velocities = np.random.uniform(-60, 60, size=(N_OISEAUX, 2)).astype(np.float32)

        self.timer = 0.0
        self.frames = 0
        self.last_time = time.perf_counter()

    def update_birds(self, dt):
        self.positions += self.velocities * dt
        below = self.positions < BOUNDS_MIN
        above = self.positions > BOUNDS_MAX
        self.positions[below] = BOUNDS_MIN
        self.positions[above] = BOUNDS_MAX
        self.velocities[below] *= -1
        self.velocities[above] *= -1

    def on_update(self, delta_time):
        self.update_birds(delta_time)

        pos_list = self.positions.tolist()
        for i, sprite in enumerate(self.sprite_list):
            sprite.center_x, sprite.center_y = pos_list[i]

        self.frames += 1
        self.timer += delta_time
        if self.timer > 1:
            print(self.frames)
            self.frames = 0
            self.timer -= 1

    def on_draw(self):
        self.clear()
        self.sprite_list.draw()

window = BenchWindow()
arcade.run()