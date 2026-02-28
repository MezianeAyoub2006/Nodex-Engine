from enum import Enum, auto

class SoundState(Enum):
    STOPPED  = auto()
    PLAYING  = auto()
    PAUSING  = auto()  
    PAUSED   = auto()