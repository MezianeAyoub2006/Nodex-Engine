import nodex
import impl 



DISPLAY_FPS = False

# I did not have the time to integrate properly these to the settings menu, sorry ;(
VSYNC = True
WINDOW_SCALE = 2
            
if __name__ == "__main__":
    context = nodex.engine.Context((256, 240), WINDOW_SCALE, VSYNC) 
    context.scenes.persistant.add_game_node(impl.Persistant(context, DISPLAY_FPS))
    context.run()
