from __future__ import annotations
from typing import TYPE_CHECKING, Union, Callable, Optional, Any
from ...nxl import Expression, attr

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
        event:str, 
        func: Callable[["Node", Any], bool]
    ):
        if event in self.subsciptions:
            self.context.warning(
                Warning.OVERRIDE,
                f"overriding node Signal named \"{event}\"",
                Priority.LOW 
            )
        self.subsciptions[event] = func
        
    def send(self, event: Signal):
        if event.depth is not None:
            if event.depth <= 0:
                return  
        for child in self.children:
            if event.type in child.subsciptions:
                if child.subsciptions[event.type](event.data):
                    child.send(Signal(
                        type=event.type,
                        data=event.data,
                        depth=None if event.depth is None else event.depth - 1
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
        self.children.sort()
        self.update()   
        for child in self.children:
            child._update_all()

    def add_tag(self, tag: str) -> None:
        self.tags.add(tag) 

    def remove_tag(self, tag: str) -> None:
        if not tag in self.tags:
            self.context.warning(
                Warning.UNKNOWN, 
                f"Node tag \"{tag}\" doesn't exist.", 
                Priority.LOW
            )
            return
        self.tags.remove(tag)

    def update(self) -> None:
        pass 

    def render(self) -> None:
        pass  

    def destroy(self) -> None:
        pass 

    def attr(self, expression:Expression) -> Expression:
        return attr(expression).on(self)

    @property
    def id(self):
        return self._id 

    @id.setter 
    def id(self, value):
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