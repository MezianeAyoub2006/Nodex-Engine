from typing import Callable, Any
from enum import Enum, auto
from .types import Node

class Operator(Enum):
    OR = auto()
    AND = auto()
    EQ = auto()
    SUP = auto()
    INF = auto()
    SUPQ = auto()
    INFQ = auto()
    IN = auto()

ACTIONS: dict[Operator, Callable[[Node, Node], Any]] = {
    Operator.OR: lambda a, b: a or b,
    Operator.AND: lambda a, b: a and b,
    Operator.EQ: lambda a, b: a == b,
    Operator.SUP: lambda a, b: a > b,
    Operator.INF: lambda a, b: a < b,
    Operator.SUPQ: lambda a, b: a >= b,
    Operator.INFQ: lambda a, b: a <= b,
    Operator.IN: lambda a, b: a in b,
}