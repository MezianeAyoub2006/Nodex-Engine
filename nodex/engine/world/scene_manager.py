from .scene import Scene

class SceneManger:
    def __init__(self, context):
        self.context = context
        self.scenes = {"main" : Scene(self.context)}
        self.current_scene = "main"
        
    def _update(self):
        self.scenes[self.current_scene].update()    

    def __getitem__(self, scene):
        return self.scenes[scene]