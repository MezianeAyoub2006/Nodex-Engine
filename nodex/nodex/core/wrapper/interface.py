from ....build import cffi 

class Interface:
    def __init__(self):
        self._interface = cffi.lib.Nx_GetInterface()

    @property 
    def fps(self):
        return self._interface.fps 

    @property 
    def dt(self):
        return self._interface.dt 

    def update(self):
        cffi.lib.Nx_Update()
