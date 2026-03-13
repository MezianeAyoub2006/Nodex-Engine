TEXT = [
    "why do you want to quit ?",
    "do you know how much work",
    "this project involves ?",
    "So disapointed right now.",
    "Bro like imma start crying.",
    "What kind of psycho exits",
    "a game by clicking \"quit\" ?",
    "just close the window bro",
    "like everyone else.",
    "Do you actually feel",
    "different ?",
    "Btw I had fun doing this",
    "game, ban me asap.",
]

import nodex 

class QuitScene(nodex.GameNode):
    def __init__(self, context : "nodex.Context"):
        super().__init__(context)
    def render(self):
        for idx, line in enumerate(TEXT):
            txt = self.context.fonts.render("consolas16bold", line)
            self.context.overlay.draw("text", txt, (5, idx * 16 + 15))