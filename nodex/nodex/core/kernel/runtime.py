from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .context import Context

class Runtime:
    def __init__(self, context: Context):
        self.context = context 

    def run(self):
        def wrapper(f):
            while not self.context._interface.should_close:
                self.context._interface.update()
                self.context.keyboard._update()
                f()  
                self.context.cffi.lib.Nx_Update()
        return wrapper
                