import nodex
import impl
import random

TOPLEFT = (64, 130)
HEIGHT = 35

SOUNDS = [
    ("race", 0.2),
    ("winter-turning", 0.085)
]

class MenuScene(nodex.GameNode):
    def __init__(self, context):
        super().__init__(context)
        self.context._gl_context.register_effect("blur", self.context.shaders.get("_blur"))
        self.context.post_process.enable_effect("blur")

        buttons = [
            ("play", self._play),
            ("settings", self._settings),
            ("quit", self._quit),
        ]

        for i, (title, callback) in enumerate(buttons):
            pos = (TOPLEFT[0], TOPLEFT[1] + i * HEIGHT)
            self.add_child(impl.Button(context, pos, title, callback))

    def _play(self, button):
        music = random.choice(SOUNDS)
        self.context.scenes.transition("main", 2, effect="circle",
            callback=lambda: self.context.post_process.diseable_effect("blur")
        )
        self.context.sounds.crossfade(music[0], 2000, music[1])

    def _settings(self, button):
        self.context.scenes.transition("settings", 0.5, effect="fade")

    def _quit(self, button):
        self.context.scenes.transition("quit", 0.01, effect="circle")

    def update(self):
        self.context._gl_context.set_uniform("blur", "strength", 0.5)
        self.context.overlay.draw("overlay", "title", (3, 10))
        self.context.overlay.draw("fx", "fx", (3, 10))
        self.context.overlay.set_uniform("fx", "time", self.context.timer)
        self.context.overlay.set_uniform("fx", "amplitude", 0.01)