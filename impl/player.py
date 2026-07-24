import nodex
from nodex.nxl import key, attr, interval, f
import pygame

def test(target):
    return len(target.tags) > 3

class Player(nodex.Node):
    def __init__(self, context): 
        super().__init__(context) 
        self.name = "player"
        self.tags.add("@player")
        self.tags.add("@player2")
        self.tags.add("@player3")
        self.grounded = True

        self.can_jump = (
            key(nodex.Key.SPACE).pressed 
            & attr("grounded")[self] 
        )

        self.cl_rule = interval(0.5) & f(test)[self]

    def update(self):
        if self.cl_rule(self.context):
            print("HELLO")








        
