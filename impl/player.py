import nodex as nx 
from nodex.nxl import key, attr 

class Player(nx.Node):
    def __init__(self, context): 
        super().__init__(context) 
        self.name = "player"
        self.tags.add("@player")
        self.can_jump = True
        self.is_jumping = key(nx.Key.SPACE).pressed & self.attr("can_jump")
        
    def update(self):
        if self.is_jumping.eval(self.context): 
            print(self.tags)
        
