import nodex 
import math

FLOWER_POS = [
    (0.8787, 0.5421),
    (0.8463, 0.6289),
    (0.8354, 0.5827),
    (0.7984, 0.5475),
    (0.8769, 0.5168),
    (0.7957, 0.5933)
]

ICEBERGS = [
    (0, (0.5, 0.5)),
    (0.3, (0.2827, 0.2087)),
    (0.6, (0.5754, 0.2591)),
    (0.9, (0.8576, 0.0531)),
    (1.2, (0.5841, 0.7670)),
    (1.5, (0.6985, 1.0368))
]

class Hub(nodex.GameNode):
    def __init__(self, context):
        super().__init__(context)
    
    def update(self):
        
        self.context.renderer.draw("billboard", position = (0.84, 0.54, -0.018), asset="tree") 
        self.context.renderer.draw("billboard", position = (0.9, 0.6, -0.01), asset="sign", angle=math.pi + 0.5)
        for pos in FLOWER_POS:
            self.context.renderer.draw("billboard", position = (pos[0], pos[1], -0.005), asset="flower") 
        for angle, pos in ICEBERGS:
            self.context.renderer.draw("billboard", position = (pos[0], pos[1], -0.015), asset="ice1") 
    
        self.context.renderer.draw("billboard", position = (0.254816, 0.53213, -0.02), asset="drift", angle = math.pi - 0.6)
        self.context.renderer.draw("billboard", position = (0.247927, 0.606687, -0.02), asset="drift", angle = math.pi - 0.6)
        self.context.renderer.draw("billboard", position = (0.244452, 0.56958, -0.02), asset="drift", angle = math.pi - 0.6)
        self.context.renderer.draw("billboard", position = (0.463019, 0.739912, -0.02), asset="jump", angle = -1.5)
        self.context.renderer.draw("billboard", position = (0.1007, 0.7931, -0.02), asset="jump", angle = 1.14)

    