from typing import TYPE_CHECKING
if TYPE_CHECKING: from .context import Context
from collections import defaultdict
from typing import Callable
from dataclasses import dataclass
from .service import Service

@dataclass
class Event:
    type: str
    data: dict 
    timer: float = 0
    frames:int = 0
    alive: bool = True

class EventBus:
    def __init__(self, context : "Context"):
        self.context = context
        self._stack: list[Event] = []
        self._registry: defaultdict[str, list[Callable[[Event], None]]] = defaultdict(list)
        self.public_stack: list[Event] = []
        Service.register(self, EventBus._update)

    def subscribe(self, type: str, callback: Callable[[Event], None]):
        self._registry[type].append(callback)

    def emit(self, event=None, **kwargs):
        if isinstance(event, Event):
            self._stack.append(event)
        else:
            self._stack.append(Event(**kwargs))

    def _update(self): 
        self.public_stack.clear()
        current_batch = self._stack       
        self._stack = []                   
        for event in current_batch:
            self._dispatch(self._registry.get(event.type, []), event)
            self._event_lifecycle(event)
        self._stack.extend(e for e in current_batch if e.alive)

    def _event_lifecycle(self, event: Event):
        if event.timer > 0:
            event.timer -= self.context.dt
        if event.frames > 0:
            event.frames -= 1
        if event.timer <= 0 and event.frames <= 0:
            event.alive = False

    def _dispatch(self, handlers, event):
        if handlers:
            for cb in handlers:
                cb(event)
        else:
            self.public_stack.append(event)

    def poll(self):
        return self.public_stack.copy()
    