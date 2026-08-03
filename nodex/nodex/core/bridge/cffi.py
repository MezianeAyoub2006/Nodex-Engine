from ....build import cffi

class Cffi:
    def __init__(self):
        self.ffi = cffi.ffi 
        self.lib = cffi.lib 
        