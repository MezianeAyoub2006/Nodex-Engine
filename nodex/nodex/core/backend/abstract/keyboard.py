from abc import ABC, abstractmethod 
from ..states.key import Key

class AbstractKeyboard(ABC): 
    @abstractmethod
    def is_pressed(self, key: Key):
        pass 

    @abstractmethod
    def is_active(self, key: Key):
        pass 

    @abstractmethod
    def is_released(self, key: Key):
        pass 

    @property
    @abstractmethod
    def active(self) -> list[Key]: 
        pass

    @property
    @abstractmethod 
    def pressed(self) -> list[Key]:
        pass 

    @property 
    @abstractmethod
    def released(self) -> list[Key]:
        pass 

    @abstractmethod 
    def _listen(self):
        pass


