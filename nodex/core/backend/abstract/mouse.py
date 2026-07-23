from abc import ABC, abstractmethod
from ..states.cursor import Cursor

class AbstractMouse(ABC):
    @property 
    @abstractmethod
    def position(self) -> tuple[int, int]: 
        pass
    
    @property
    @abstractmethod 
    def left_pressed(self) -> bool:
        pass 

    @property 
    @abstractmethod
    def right_pressed(self) -> bool:
        pass 

    @property
    @abstractmethod
    def left_active(self) -> bool:
        pass 

    @property
    @abstractmethod
    def right_active(self) -> bool:
        pass 

    @property
    @abstractmethod 
    def speed(self) -> tuple[int, int]:
        pass  

    def set_cursor(self, cursor: Cursor) -> None:
        pass


