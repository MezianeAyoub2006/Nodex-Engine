from .scene import Scene
import nodex

class SceneManger:
    def __init__(self, context : "nodex.Context"):
        self.context = context
        self._persistant = Scene(self.context)
        self.scenes = {"main" : Scene(self.context)}
        self.current_scene = "main"
        
    def _update(self):
        self.scenes[self.current_scene].update()  
        self.persistant.update() 

    def __getitem__(self, scene):
        return self.scenes[scene]
    
    @property
    def persistant(self):
        return self._persistant