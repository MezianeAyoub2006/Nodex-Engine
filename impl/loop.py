import nodex 

class GameLoop(nodex.Node):
    def __init__(self, context):
        super().__init__(context)

    def update(self):
        if self.context.keyboard.is_pressed(nodex.Key.SPACE): 
            self.context.events.emit(nodex.Event(type = "wake_up"))  