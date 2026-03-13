import nodex 
import impl
import pygame
import math

TEMP_POS = (5, 186)

class GameScene(nodex.GameNode):
    def __init__(self, context : "nodex.Context"):
        super().__init__(context)
        self.player = impl.Player(self.context, "mode7", "billboard") 
        self.add_child(self.player)
        self.add_child(impl.ObstaclesManager(self.context, self.player))
        self.temp_img_size = self.context.assets.get_image("temp").get_size()

    def render(self):
        self.render_score()
        self.render_temperaturre()

    def load(self):
        self.context.post_process.diseable_effect("fx")
        self.player.load()

    def render_score(self):
        lenght = len(str(math.floor(self.player.score)))
        self.pretty_display_number(math.floor(self.player.score), (120 - lenght * 12, 3))
    
    def pretty_display_number(self, number, position):
        for idx, char in enumerate(str(number)):
            index = int(char)
            self.context.overlay.draw("overlay", f"nums.{index}.0", (position[0] + 24 * idx, position[1]))

    def render_temperaturre(self):
        filled_h = (self.player.temperature / 100) * self.temp_img_size[1] - 1
        offset_y = self.temp_img_size[1] - filled_h
        if filled_h > 0:
            self.context.overlay.draw("overlay", pygame.Rect(
                (TEMP_POS[0], TEMP_POS[1] + offset_y - 1), (
                    self.temp_img_size[0],
                    filled_h
                )), color=((self.player.temperature / 100) * 255, 0, 255 - (self.player.temperature / 100) * 255)
            )
        self.context.overlay.draw("overlay", "temp", TEMP_POS) 
    
    