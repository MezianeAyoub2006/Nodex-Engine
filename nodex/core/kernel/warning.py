from enum import Enum, auto

class Priority(Enum):
    LOW = auto()
    MIDLOW = auto()
    MID = auto()
    MIDHIGH = auto()
    HIGH = auto()
    
class Warning(Enum):
    OVERRIDE = auto()
    UNKNOWN = auto()
    RESERVED = auto()