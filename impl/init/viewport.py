import nodex 

class ViewportLoader:
    def __init__(self, context : "nodex.Context"):
        self.context = context

    def load(self):
        r = self.context.renderer
        r.add_viewport("background", nodex.ViewportType.PYGAME)
        r.add_viewport("mode7", nodex.ViewportType.MODE7, settings={
            "texture" : "assets/images/grounds/main3.png",
            "texture_name" : "tex",
            "scenes" : ("main", "menu", "settings"),
            "infinite" : "assets/images/grounds/infinite.png",
            "extra" : "assets/images/grounds/materials.png"  
        })
        r.add_viewport("billboard", nodex.ViewportType.BILLBOARD,
                       self.context.shaders.get("_outline"), settings={"reference": "mode7"})

        o = self.context.overlay
        o.add_viewport("overlay", nodex.ViewportType.PYGAME)
        o.add_viewport("text", nodex.ViewportType.PYGAME, self.context.shaders.get("_outline"))
        o.add_viewport("fx", nodex.ViewportType.PYGAME, self.context.shaders.get("fx"))
        o.add_viewport("mouse", nodex.ViewportType.PYGAME)

