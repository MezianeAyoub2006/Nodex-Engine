from typing import TYPE_CHECKING, Union, Callable
from dataclasses import dataclass
if TYPE_CHECKING: from .context import Context 
from .phase import EnginePhase

@dataclass
class ServiceTask:
    order: int  
    cls: type 
    func: Callable

class Service:
    
    parent: Union["Service", None] = None 
    children: list["Service"] = []
    context: "Context" 

    tasks : dict[EnginePhase, list[ServiceTask]] = {
        EnginePhase.PRE_FRAME : [], 
        EnginePhase.PRE_RENDER : [], 
        EnginePhase.POST_RENDER :[], 
        EnginePhase.POST_FRAME : []
    }

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.children = []
        parent = cls.__bases__[0]
        if issubclass(parent, Service):
            cls.parent = parent
            parent.children.append(cls)

    @staticmethod
    def register(owner, func: Callable, order: int = 0, phase: "EnginePhase" = EnginePhase.PRE_FRAME):
        Service.tasks[phase].append(ServiceTask(order = order, cls = owner, func = func))

    @classmethod 
    def update(cls, order:int = 0, sys_order:EnginePhase = EnginePhase.PRE_FRAME):
        def wrapper(f):
            Service.tasks[sys_order].append(ServiceTask(
                order = order, 
                cls = cls, 
                func = f  
            ))
            return f 
        return wrapper  
 
    @staticmethod
    def _update(sys_order: EnginePhase):
        for task in sorted(
            Service.tasks[sys_order], 
            key=lambda t: t.order
        ):  
            if hasattr(task.func, "__self__"):
                task.func()
            else:
                task.func(task.cls)
          
    @classmethod 
    def reset(cls):
        pass 

    @classmethod 
    def destroy(cls):
        pass

    @classmethod
    def propagate(cls, method_name: str, *args, **kwargs):
        if hasattr(cls, method_name):
            func = getattr(cls, method_name)
            func(*args, **kwargs)
            for child in cls.children:
                child.propagate(method_name, *args, **kwargs)
        else:
            raise Exception("FREROT YA PAS LE FCK HOOK")