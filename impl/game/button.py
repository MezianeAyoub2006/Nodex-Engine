import nodex
import pygame

RECT_OFFSET = (12, 4)
TEXT_OFFSET = (20, 4)
CHAR_SPACE = 5
MAX_CHARS = 9
CLICKED_OFFSET = 5

class Button(nodex.GameNode):
    def __init__(self, context, position, title, callback, viewport="overlay", slider=None):
        super().__init__(context)
        self.position = position
        self.title = title
        self.slider = slider
        self._slider_index = 0
        self.callback = callback
        self.viewport = viewport
        self.hovered = False
        self.clicked = False
        self.pressed = False

    @property
    def display_title(self):
        if self.title == "WINDOWED":
            return "FULLSCREEN" if self.context.window.fullscreen else "WINDOWED"
        if self.slider:
            return self.slider[self._slider_index]
        return self.title

    def slide(self):
        if self.title == "WINDOWED":
            return
        if not self.slider:
            return
        self._slider_index = (self._slider_index + 1) % len(self.slider)

    def update(self):
        pass

    def render(self):
        self.hovered = self.rect.collidepoint(self.context.input.mouse_position)
        self.pressed = self.context.input.mouse_pressed[0] and self.hovered
        self.clicked = self.context.input.mouse_clicked[0] and self.hovered

        if self.pressed and self.context.scenes.transition_done:
            self.context.sounds.track("button")
            if self.slider:
                self.slide()
            self.callback(self)

        if self.clicked:
            asset = "buttons.0.2"
        elif self.hovered:
            asset = "buttons.0.1"
        else:
            asset = "buttons.0.0"

        self.context.overlay.draw(self.viewport, asset, self.position)

        title = self.display_title
        text = self.context.fonts.render("main16", title, nodex.Color.BLACK)
        self.context.overlay.draw("text", text, (
            self.position[0] + TEXT_OFFSET[0] + (MAX_CHARS - len(title)) * CHAR_SPACE,
            self.position[1] + TEXT_OFFSET[1] + (CLICKED_OFFSET if self.clicked else 0)
        ))

    @property
    def rect(self):
        return pygame.Rect(
            (self.position[0] + RECT_OFFSET[0], self.position[1] + RECT_OFFSET[1]),
            (100, 20)
        )