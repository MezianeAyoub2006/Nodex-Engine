from __future__ import annotations
from typing import TYPE_CHECKING, Union, Callable, Optional, Any
from ...NX_L import Expression, attr

if TYPE_CHECKING: 
    from ..kernel.context import Context

from dataclasses import dataclass

from ..kernel.warning import Warning, Priority
from .exceptions import NodeRegisteryException, NodeIdChange

@dataclass
class Signal:
    type: str 
    data: Optional[Any] = None 
    depth: Optional[int] = None 

class Node:
    _id: int = 0 
    _id_registry: dict[int, "Node"] = {}
    _name_registry: dict[str, int] = {}

    @staticmethod
    def register(node: "Node", name: str) -> None:
        if name == "UNKNOWN":
            node.context.warning(
                Warning.RESERVED, 
                f"\"UNKNOWN\" refers to unnamed nodes.",
                Priority.MID 
            )
        if name in Node._name_registry:
            node.context.warning(
                Warning.OVERRIDE, 
                f"overriding Node named \"{name}\".",
                Priority.LOW 
            )
        Node._id_registry[node.id] = node
        Node._name_registry[name] = node.id 
        node._name = name 

    @staticmethod
    def get(key: Union[str, int]) -> "Node":
        if isinstance(key, str):
            if key in Node._name_registry:
                node_id = Node._name_registry[key]
                return Node._id_registry[node_id]
            raise NodeRegisteryException(f"Node named \"{key}\" not found.")
        elif isinstance(key, int):
            if key in Node._id_registry:
                return Node._id_registry[key] 
            raise NodeRegisteryException(f"Node id {key} not found.") 
        else:
            raise NodeRegisteryException(f"Node registery key type \"{type(key).__name__}\" not valid.")
        
    def subscribe(self, 
        signal:str, 
        func: Callable[["Node", Any], bool]
    ):
        if signal in self.subsciptions:
            self.context.warning(
                Warning.OVERRIDE,
                f"overriding node Signal named \"{signal}\"",
                Priority.LOW 
            )
        self.subsciptions[signal] = func
        
    def send(self, signal: Signal):
        if signal.depth is not None:
            if signal.depth <= 0:
                return  
        for child in self.children:
            if signal.type in child.subsciptions:
                if child.subsciptions[signal.type](signal.data):
                    child.send(Signal(
                        type=signal.type,
                        data=signal.data,
                        depth=None if signal.depth is None else signal.depth - 1
                    ))

    def search(self, rule: Expression, depth: int) -> list["Node"]: 
        def search_rec(node: Node, rule_ : Expression, depth_ : int, l: list[Node]): 
            print("passage par", node)
            if depth_ <= 0:
                return
            if rule_.evaluate(node):
                l.append(node)
            for child in node.children:
                search_rec(child, rule_, depth_ - 1, l) 
        l = []
        search_rec(self, rule, depth, l)
        return l

    def bind(self, child: "Node"):
        self.children.append(child)
        
    def __init__(self, context : "Context", order:int = 0) -> None:
        self.context: "Context" = context
        self.children:list["Node"] = []
        self._id: int = Node._id 
        self.tags:set[str] = {"@node"}
        self.subscribed = set()
        self.order:int = order
        self.subsciptions:dict[str, Callable[["Node", Any], bool]] = {}
        Node._id += 1
        self._name = None 

    def _update_all(self) -> None:
        self.children.sort(key = lambda c: c.order)
        self.update()   
        for child in self.children:
            child._update_all()

    def update(self) -> None:
        pass 

    def render(self) -> None:
        pass  

    def destroy(self) -> None:
        pass 

    def attr(self, expression:Expression) -> Expression:
        return attr(expression)[self]

    @property
    def id(self):
        return self._id 

    @id.setter 
    def id(self, _):
        raise NodeIdChange("Node id cannot be manually changed.")

    @property
    def name(self):
        if self._name:
            return self._name 
        else:
            return "UNKNOWN" 

    @name.setter
    def name(self, value:str):
        Node._name_registry[value] = self._id 
        self._name = value
        Node.register(self, value)

    def __repr__(self):
        return f"Node<{self.name}>"