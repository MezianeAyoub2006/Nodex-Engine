import nodex
import impl 

context = nodex.Context(
    (250, 240), 1, True, 
    # make sur the game runs on pygame
    backend = nodex.backend.Backend.PYGAME_MODERNGL 
)

# adds the initializing node
context.root.bind(impl.Player(context)) 
context.root.bind(impl.GameLoop(context))

# runs the game loop 
context.run() 