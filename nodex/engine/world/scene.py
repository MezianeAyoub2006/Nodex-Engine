class Scene:
    def __init__(self, context):
        self.context = context 
        self.nodes = set()
    def update(self):   
        for node in self.nodes:
            node.update_all()
            if node.flags.render:
                node.render()