from operator import attrgetter 
from dataclasses import dataclass 
import nodex

@dataclass
class Flags:
    update:bool = True 
    render:bool = True 
    propagate:bool = True 
    alive:bool = True

class GameNode:
    _id:int = 0
    def __init__(self, context : "nodex.Context"):
        self.context = context 
        self.children = set()
        self.order = 0
        self.flags = Flags()
        GameNode._id += 1
        self.id = GameNode._id
    
    def update(self):
        pass 

    def render(self):
        pass 

    def load(self):
        pass

    def update_all(self): 
        if self.flags.update:
            self.update() 
        if self.flags.propagate:
            for child in sorted(self.children, key = attrgetter("order")):
                child.update_all()