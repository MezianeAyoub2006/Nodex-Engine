from __future__ import annotations

from typing import TYPE_CHECKING
from .operator import Operator  
from .types import Node

if TYPE_CHECKING:
    from .entry import Entry 

class Expression:  
    def __and__(self, other: Node) -> Entry:
        from .entry import Entry
        return Entry(self, other, Operator.AND)

    def __rand__(self, other: Node) -> Entry: 
        from .entry import Entry
        return Entry(other, self, Operator.AND)

    def __or__(self, other: Node) -> Entry:
        from .entry import Entry
        return Entry(self, other, Operator.OR)

    def __ror__(self, other: Node) -> Entry:
        from .entry import Entry 
        return Entry(other, self, Operator.OR)
    
    def __gt__(self, other: Node) -> Entry:
        from .entry import Entry
        return Entry(self, other, Operator.SUP)
    
    def __lt__(self, other: Node) -> Entry:
        from .entry import Entry
        return Entry(self, other, Operator.INF)
       
    def __ge__(self, other: Node) -> Entry:
        from .entry import Entry
        return Entry(self, other, Operator.SUPQ)
    
    def __le__(self, other: Node) -> Entry:
        from .entry import Entry
        return Entry(self, other, Operator.INFQ)
    
    def __eq__(self, other: Node):
        from .entry import Entry
        return Entry(self, other, Operator.EQ)
    
    def in_(self, other: Node) -> Entry:
        from .entry import Entry
        return Entry(self, other, Operator.IN)
    
    def hash(self) -> str:
        return self.__repr__()
    
    def evaluate(self, target):
        from .eval import evaluate 
        return evaluate(target, self)

