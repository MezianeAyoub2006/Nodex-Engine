import nodex 
import impl

TOPLEFT = (64, 72)
HEIGHT = 35

SLIDERS = [
    ["WASD", "ZQSD", "ARROWS"],
    ["WINDOWED", "FULLSCREEN"],
]

class SettingsScene(nodex.GameNode):
    def __init__(self, context: "nodex.Context"):
        super().__init__(context) 
        
        buttons = [
            ("WASD", self._controls),
            ("WINDOWED", self._fullscreen),
            ("MENU", self._menu), 
        ]

        for i, (title, callback) in enumerate(buttons):
            pos = (TOPLEFT[0], TOPLEFT[1] + i * HEIGHT)
            if i < 2:
                slider = SLIDERS[i]
            else:
                slider = None
            self.add_child(impl.Button(context, pos, title, callback, slider = slider))
    
    def update(self):
        pass

    def _controls(self, button : "impl.Button"):
        button.context.globals["key_profile"] = button.slider[button._slider_index]

    def _fullscreen(self, button : "impl.Button"):
        button.context.window.toggle_fullscreen()

    def _menu(self, button):
        self.context.scenes.transition("menu", 0.5, "fade")
