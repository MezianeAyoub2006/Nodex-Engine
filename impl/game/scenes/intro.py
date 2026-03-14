import nodex

class IntroHandler:
    def __init__(self, context : "nodex.Context"):
        self.context = context
        self.transition_done = False
        self.pygame_sound_done = False
        

    def update(self):
        scene = self.context.scenes.current_scene
        if scene == "pygame":
            self.context.renderer.draw("background", "pygame", (77, 83))
            if self.context.timer > 2 and not self.transition_done:
                self.transition_done = True
                self.context.scenes.transition(
                    "moderngl", 1, ("fade",),
                    lambda: setattr(self, "transition_done", False)
                )
        if scene == "moderngl":
            self.context.renderer.draw("background", "moderngl", position=(77, 70))
            if self.context.timer > 5 and not self.transition_done:
                self.transition_done = True
                self.context.scenes.transition("menu", 3, ("wave", "fade"))
                self.context.sounds.track("winter-waltz", 0.3, -1, 2000)
