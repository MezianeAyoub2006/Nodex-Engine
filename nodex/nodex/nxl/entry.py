from .types import Node
from .operator import Operator 
from .expression import Expression 

class Entry(Expression):
    def __init__(self, left: Node, right: Node, op: Operator):
        self.op = op
        self.left = left
        self.right = right

    def _format(self, depth: int = 0) -> str:
        pad = "  " * depth
        next_pad = "  " * (depth + 1)

        left_str = (
            self.left._format(depth + 1)
            if hasattr(self.left, "_format")
            else str(self.left)
        )
        right_str = (
            self.right._format(depth + 1)
            if hasattr(self.right, "_format")
            else str(self.right)
        )

        return (
            f"(NXL) {{\n"
            f"{next_pad}left: {left_str},\n"
            f"{next_pad}op: {self.op.name},\n"
            f"{next_pad}right: {right_str}\n"
            f"{pad}}}"
        )

    def __repr__(self) -> str:
        return self._format(depth=0)
    
    def hash(self) -> str:
        return self.__repr__()
