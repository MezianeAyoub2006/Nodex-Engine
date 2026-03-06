import nodex 

def init_viewports(context : "nodex.Context"):
    context.renderer.add_viewport("mode7", nodex.ViewportType.MODE7, settings={
        "texture" : "assets/ground.png", 
        "texture_name" : "tex"
    })

    context.renderer.add_viewport("billboard", nodex.ViewportType.BILLBOARD, settings = {
        "reference" : "main"
    }) 

def init_assets(context : "nodex.Context"):
    context.window.set_caption("IceSkater FX")
    context.assets.load_image("ground", "assets/ground.png")
    context.assets.load_image("ground2", "assets/ground2.png")
    context.assets.load_image("infinite", "assets/ground-infinite.png") 