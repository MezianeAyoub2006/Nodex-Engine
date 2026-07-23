from __future__ import annotations
from typing import TYPE_CHECKING
from ..expression import Expression
if TYPE_CHECKING:
    from ...node import Node 

class HasTagNode(Expression):
    def __init__(self, tag: str):
        self.tag = tag 

    def resolve(self, target: Node):
        return self.tag in target.tags 

    def __repr__(self):
        return f"has_tag({self.tag})"

def has_tag(tag) -> Expression:
    return HasTagNode(tag)
