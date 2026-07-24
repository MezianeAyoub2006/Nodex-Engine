from __future__ import annotations
from ..expression import Expression
from typing import TYPE_CHECKING
if TYPE_CHECKING: from ...core.kernel.context import Context

class IntervalNode(Expression):
    def __init__(self, range):
        super().__init__()
        self.timer = range
        self.range = range

    def resolve(self, target:Context):
        if self.timer <= 0:
            self.timer = self.range
            return True
        self.timer -= target.dt 
        return False 

    def __repr__(self):
        return f"Interval({self.range})"


def interval(range: float):
    return IntervalNode(range) 

