from .cffi import Cffi

class Interface:
    def __init__(self, cffi: Cffi):
        self._cffi = cffi 
        self.ptr = self._cffi.lib.Nx_Interface_Get() 
        self._status = self.ptr.status 
        self._window = self.ptr.window 
        self._rendering_queue = self.ptr.rendering_queue
        self._should_close = False

    def update(self):
        self._dt = self.ptr.time.dt 
        self._fps = self.ptr.time.fps 
        self._timer = self.ptr.time.timer 
        self._should_close = self.ptr.should_close

    @property
    def dt(self):
        return self._dt 

    @property
    def fps(self):
        return self._fps 

    @property
    def timer(self):
        return self._timer 
    
    @property
    def should_close(self):
        return self._should_close

    @property
    def window(self):
        return self._window 

    @property
    def rendering_queue(self):
        return self._rendering_queue 

    @property
    def status(self):
        return self._status