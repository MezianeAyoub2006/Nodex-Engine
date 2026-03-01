class Scene:
    def __init__(self, context):
        self.context = context 
        self.nodes = set()

    def add_game_node(self, game_node):
        self.nodes.add(game_node)

    def update(self):   
        for node in self.nodes:
            node.update_all()
            if node.flags.render:
                node.render()