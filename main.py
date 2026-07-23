import nodex as nx 
import impl 

context = nx.Context((250, 240), 1, True) 
context.root.bind(impl.Player(context)) 

@context.run()
def loop():
    pass
