from enum import Enum, auto

class Cursor(Enum):
    ARROW = auto()        
    IBEAM = auto()      
    WAIT = auto()           
    WAIT_ARROW = auto()    
    CROSSHAIR = auto()     
    HAND = auto()          
    NOT_ALLOWED = auto()   
    RESIZE_H = auto()       
    RESIZE_V = auto()       
    RESIZE_NWSE = auto()    
    RESIZE_NESW = auto()
    RESIZE_ALL = auto()     
    MOVE = auto()
    NONE = auto()           