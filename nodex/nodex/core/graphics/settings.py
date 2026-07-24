from dataclasses import dataclass

class SettingsType:
    pass

@dataclass
class TextureSettings(SettingsType):
    position: tuple[int, int]

@dataclass
class RectangleSettings(SettingsType):
    color: tuple[int, int, int, int]

class settings:
    texture = TextureSettings
    rectangle = RectangleSettings 
