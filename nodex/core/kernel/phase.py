from enum import Enum 

class EnginePhase(Enum):
    PRE_FRAME = 0 
    PRE_RENDER = 1
    POST_RENDER = 2
    POST_FRAME = 3

