import nodex 

class Player(nodex.GameNode):
    def __init__(self, context : nodex.Context):
        super().__init__(context)

    def update(self):
        print("Hello World")

