import nodex
import pygame
import random

class GlobalNode(nodex.GameNode):
    def __init__(self, context:"nodex.Context"): 
        super().__init__(context)
        pygame.display.set_icon(pygame.image.load("logo.png"))
        self.context.assets.load_image("player", "assets/images/billboard/player.png")
        self.context.assets.load_image("ground", "assets/ground.png")
        self.context.assets.load_image("ground2", "assets/ground2.png")
        self.context.assets.load_image("infinite", "assets/ground-infinite.png") 
        self.context.assets.load_image("title", "assets/images/ui/title.png")
        self.context.renderer.add_viewport("main", nodex.ViewportType.MODE7, settings={
            "texture" : "assets/ground.png", 
            "texture_name" : "tex"
        })

        self.context.renderer.add_viewport("billboard", nodex.ViewportType.BILLBOARD, settings = {
            "reference" : "main"
        })
    
    def update(self): 
        self.context.window.set_caption(f"IceRunner FX  {self.context.fps} FPS")
        self.context.renderer.draw("billboard", "player", position = (0.5, 0.5, 0), asset="player")
        self.context.renderer.draw("billboard", "title", position = (0.5, 0.7, 0.3), asset="title")
        self.context.renderer.draw("main", "ground2")