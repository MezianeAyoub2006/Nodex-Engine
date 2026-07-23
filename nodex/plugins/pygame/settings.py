from dataclasses import dataclass 

from ...core.graphics.settings import SettingsType

@dataclass
class PygameSettings(SettingsType):
    position: tuple[int, int]
    viewport: str  
