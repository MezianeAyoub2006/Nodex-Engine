from .window import Window 
from .renderer import Renderer 
from .interface import Interface

class Wrapper:
    def __init__(self, context, **w_kwargs): 
        self.interface = Interface(context)
        self.window = Window(interface = self.interface, **w_kwargs)  
        self.renderer = Renderer(self.interface)  
