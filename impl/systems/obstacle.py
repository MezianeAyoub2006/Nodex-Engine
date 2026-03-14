import nodex 

Z_CONFIG = {
    "ice1" : -0.015,  
    "ice0" : -0.008
}

DISTANCES = {
    "ice1" : (0.01, 0.02), 
    "ice0" : (0.005, 0.01)
}

TEMPERATURES = {
    "ice1" : 50,
    "ice0" : 30
}
class Obstacle(nodex.GameNode):
    def __init__(self, context, position, type, player):
        super().__init__(context) 
        self.position = position
        self.type = type
        self.player = player

    def render(self):
        self.context.renderer.draw("billboard", position = (
            self.position[0],
            self.position[1], 
            Z_CONFIG[self.type]
        ), asset = self.type)

    def update(self):
        if nodex.distance2D(self.position, (self.player.entity.position.x, self.player.entity.position.y)) < DISTANCES[self.type][0] and self.player.entity.position.z < DISTANCES[self.type][0]:
            self.player.temperature -= TEMPERATURES[self.type]
            if self.player.temperature > 0:
                self.context.sounds.track("hit")
            self.kill()