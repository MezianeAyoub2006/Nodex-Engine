import nodex
import pygame

from operator import itemgetter
from moving import Moving


class Test(nodex.GameNode):
    def __init__(self, context:"nodex.Context"):
       
        super().__init__(context)
        self.context.assets.load_image("ground", "assets/ground.png")
        self.context.assets.load_image("ground2", "assets/ground2.png")
        self.context.assets.load_image("infinite", "assets/ground-infinite.png")
        self.context.renderer.add_viewport("main", nodex.ViewportType.MODE7, 0, extra_data={"texture" : "assets/ground.png", "texture_name" : "tex"})

    
    def update(self): 
        self.context.renderer.draw("main", "ground2")
        self.context.window.set_caption(str(round(self.context.fps)))

    


context = nodex.engine.Context((250, 240), 2, False, benchmark_fps_target=200) 
context.scenes["main"].add_game_node(Test(context))
context.scenes["main"].add_game_node(Moving(context))
context.run()