from .scene import Scene

class SceneManger:
    def __init__(self, context):
        self.context = context
        self.scenes = {"main" : Scene(self.context)}
        self.current_scene = "main"
    
    def update(self):
        self.scenes[self.current_scene].update()

    def add_game_node(self, game_node, scene):
        if scene:
            self.scenes[scene].nodes.add(game_node)
        else:
            self.scenes[self.current_scene].nodes.add(game_node)
