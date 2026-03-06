import nodex
import impl

from moving import Moving
            
if __name__ == "__main__":

    context = nodex.engine.Context((250, 240), 2, False) 
    context.scenes.persistant.add_game_node(impl.GlobalNode(context))
    context.scenes.persistant.add_game_node(Moving(context))
    context.run()
