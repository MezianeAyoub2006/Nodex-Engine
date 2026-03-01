from .sound_loader import SoundLoader
from .sound_state import SoundState

class SoundManager:
    def __init__(self, context):
        self.context = context 
        self.sound_loader = SoundLoader(context) 
        self._active_sounds = []
    
    def load_sound(self, name, path):
        self.sound_loader.load_sound(name, path)

    def track(self, name):
        sound = self.sound_loader.get_sound(name)
        self._active_sounds.append(sound)
        return sound 

    def update(self):
        for sound in self._active_sounds:
            sound.update()
        self._active_sounds = [s for s in self._active_sounds if s.state != SoundState.STOPPED]

    def pause_all(self):
        for sound in self._active_sounds:
            sound.pause()
    
    def resume_all(self):
        for sound in self._active_sounds:
            sound.resume()

    def stop_all(self, fade_out_ms = None):
        for sound in self._active_sounds:
            sound.stop(fade_out_ms)