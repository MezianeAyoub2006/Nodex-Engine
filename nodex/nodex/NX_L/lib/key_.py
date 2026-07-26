from __future__ import annotations 
from typing import TYPE_CHECKING
if TYPE_CHECKING: from ...core.kernel.context import Context
from ..expression import Expression

class KeyPressedNode(Expression):
    def __init__(self, key): 
        super().__init__()
        self.key = key

    def resolve(self, target:Context): 
        return target.keyboard.is_pressed(self.key)
    def __repr__(self): 
        return f"key_pressed({self.key})" 

class KeyActiveNode(Expression):
    def __init__(self, key): 
        super().__init__()
        self.key = key
    def resolve(self, target:Context): 
        return target.keyboard.is_active(self.key)
    def __repr__(self): 
        return f"key_active({self.key})" 

class KeyReleasedNode(Expression):
    def __init__(self, key): 
        super().__init__()
        self.key = key
    def resolve(self, target:Context): 
        return target.keyboard.is_released(self.key)
    def __repr__(self): 
        return f"key_released({self.key})"  

class KeyExpressionFactory:
    def __init__(self, key):
        self.key = key 
    @property
    def pressed(self) -> Expression:
        return KeyPressedNode(self.key)
    @property
    def active(self) -> Expression:
        return KeyActiveNode(self.key)
    @property
    def released(self) -> Expression:
        return KeyReleasedNode(self.key)

def key(key) -> KeyExpressionFactory:
    return KeyExpressionFactory(key) 
