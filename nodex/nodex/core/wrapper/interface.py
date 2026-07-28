from ....build import cffi 
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..kernel.context import Context
from .exceptions import NativeException 
from ..kernel.warning import Warning, Priority

def is_error(status):
    return cffi.lib.NX_ERR <= status < cffi.lib.NX_WARN

def buffer_to_string(buff):
    return cffi.ffi.string(buff).decode("utf-8", errors = "replace")

class Interface:
    def _handle_status(self, status):
        buff = cffi.ffi.new("char[256]") 
        cffi.lib.Nx_FormatStatus(buff, 256, status) 
        formated_status = buffer_to_string(buff)
        message = buffer_to_string(self.ptr.read.status.message)
        output = f"[ {formated_status} ] {message}"
        if is_error(status):
            raise NativeException(output)
        else:
            self.context.warning(Warning.NATIVE, output, Priority.HIGH)
        self.ptr.write.flags.statusConsumed = True  
     
    def __init__(self, context: Context):
        self.ptr = cffi.lib.Nx_GetInterface()
        self.context = context 

    @property 
    def fps(self):
        return self.ptr.read.time.fps

    @property 
    def dt(self):
        return self.ptr.read.time.dt

    def update(self):
        status = self.ptr.read.status.last
        print(status) 
        if (status != 0): 
            self._handle_status(status)
        cffi.lib.Nx_Update()
