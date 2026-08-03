from ....build import cffi
from .exceptions import NativeException

status_ptr = cffi.lib.NxInterface_Status_Get()

def _to_str(ptr):
    return cffi.ffi.string(ptr).decode('utf-8')

def check_native_error():
    if status_ptr.error_happened: 
        message = _to_str(status_ptr.error.message)
        source = _to_str(status_ptr.error.source) 
        raise NativeException(f"\nsource: {source}\n>>> {message}")