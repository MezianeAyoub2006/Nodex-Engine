import nodex 

class Renderer:
    def __init__(self, context):
        self.context = context 
        self._tasks = []

    def clear(self):
        self._tasks.clear()