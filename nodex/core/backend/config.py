from .abstract import AbstractRenderer, AbstractShader, AbstractTexture, AbstractWindow, AbstractKeyboard
from .pygame_moderngl import PygameModernglRenderer, PygameModernglShader, PygameModernglTexture, PygameModernglWindow, PygameKeyboard
from enum import Enum, auto 
from dataclasses import dataclass

class Backend(Enum):
    PYGAME_MODERNGL = auto()

@dataclass
class BackendTypes:
    renderer: type[AbstractRenderer]
    window: type[AbstractWindow]
    texture: type[AbstractTexture] 
    shader: type[AbstractShader]  
    keyboard: type[AbstractKeyboard]

BACKENDS = {
    Backend.PYGAME_MODERNGL: BackendTypes(
        renderer = PygameModernglRenderer,
        window = PygameModernglWindow,
        texture = PygameModernglTexture, 
        shader = PygameModernglShader,
        keyboard = PygameKeyboard
    )
}