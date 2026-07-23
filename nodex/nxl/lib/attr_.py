from ..expression import Expression

class AttrNotFound(Exception):
    pass

class AttrNode(Expression):
    _MISSING = object()

    def __init__(self, path: str, default=None):
        super().__init__()
        self.path = path.split(".")
        self.default = default

    def resolve(self, target):
        curr = target
        for key in self.path:
            curr = curr.get(key, self._MISSING) if isinstance(curr, dict) else getattr(curr, key, self._MISSING)
            if curr is self._MISSING:
                if self.default is None:
                    raise AttrNotFound(f"attr path \"{'.'.join(self.path)}\" not found on {target}.")
                return self.default
        return curr

    def __repr__(self):
        return f"attr({self.path}, default={self.default})"
    
def attr(path: str, default = None):
    return AttrNode(path, default) 
