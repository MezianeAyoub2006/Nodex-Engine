from ..sounds.sound_loader import SoundLoader
from ..sounds.sound_state import SoundState

class SoundManager:
    def __init__(self, context):
        self.context = context 
        self.sound_loader = SoundLoader(context) 
        self._active_sounds = []
        self._crossfade_pending = None
        self._crossfade_timer = 0
    
    def load_sound(self, name, path):
        self.sound_loader.load_sound(name, path)

    def track(self, name, volume=1.0, loops=0, fade_in_ms=None):
        sound = self.sound_loader.get_sound(name).copy()
        if fade_in_ms:
            sound.play(start_volume=0.0, loops=loops, fade_in_ms=fade_in_ms, target_volume=volume)
        else:
            sound.play(volume, loops)
        self._active_sounds.append(sound)
        return sound

    def update(self):
        for sound in self._active_sounds:
            sound.update()
        self._active_sounds = [s for s in self._active_sounds if s.state != SoundState.STOPPED]

        if self._crossfade_pending:
            self._crossfade_timer -= self.context.dt
            if self._crossfade_timer <= 0:
                name, duration_ms, volume, loops = self._crossfade_pending
                self._crossfade_pending = None
                sound = self.sound_loader.get_sound(name).copy()
                sound.play(start_volume=0.0, loops=loops, fade_in_ms=duration_ms, target_volume=volume)
                self._active_sounds.append(sound)

    def pause_all(self):
        for sound in self._active_sounds:
            sound.pause()
    
    def resume_all(self):
        for sound in self._active_sounds:
            sound.resume()

    def stop_all(self, fade_out_ms = None):
        for sound in self._active_sounds:
            sound.stop(fade_out_ms)

    def crossfade(self, name, duration_ms=1000, volume=1.0, loops=-1):
        self._crossfade_pending = (name, duration_ms, volume, loops)
        self._crossfade_timer = duration_ms / 1000

        for sound in self._active_sounds:
            sound.stop(fade_out_ms=duration_ms)