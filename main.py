import nodex
import pygame

from operator import itemgetter


class Test(nodex.GameNode):
    def __init__(self, context:"nodex.Context"):
       
        super().__init__(context)
        self.context.assets.load_image("ground", "assets/ground.png")
        self.context.assets.load_image("ground2", "assets/ground2.png")
        self.context.assets.load_image("infinite", "assets/ground-infinite.png")
        self.context.renderer.add_viewport("main", nodex.ViewportType.BASIC, 0)
        self.context.renderer.add_viewport("main1", nodex.ViewportType.BASIC, 1)
        self.context.renderer.add_viewport("main2", nodex.ViewportType.BASIC, 2)
        self.context.renderer.add_viewport("main3", nodex.ViewportType.BASIC, 3)
        self.context.renderer.add_viewport("main4", nodex.ViewportType.BASIC, 4)
        self.context.renderer.add_viewport("main5", nodex.ViewportType.BASIC, 5)
    
    def update(self): 
        self.context.renderer.draw("main", "ground2", position=(50, 0))
        self.context.renderer.draw("main3", "infinite", position=(-10, 0))
    


context = nodex.engine.Context((250, 240), 2, False, benchmark_fps_target=200) 
context.scenes["main"].add_game_node(Test(context))
context.run()