import pygame
import nodex
from .sound_state import SoundState

def _update_volume(volume:float, target_volume:float, volume_change:float|None, delta_time:float) -> tuple[float, float|None]:
    if volume_change is not None:
        volume += volume_change * delta_time
        if (volume_change < 0 and volume < target_volume) or (volume_change > 0 and volume > target_volume):
            volume = target_volume
            volume_change = None
    return volume, volume_change

class Sound:
    def __init__(self, context:"nodex.Context", sound:pygame.Sound, volume:float = 1.0):
        self.context = context
        self.sound   = sound

        self.volume        = volume
        self.target_volume = volume
        self.volume_change:float|None = None

        self.length = self.sound.get_length() * 1000  
        self.play_time = 0.0  

        self.loops   = 0
        self.state   = SoundState.STOPPED
        self.channel:pygame.Channel|None = None

    def set_volume(self, volume:float):
        self.volume = self.target_volume = volume

    def change_volume(self, target_volume:float, duration_ms:int):
        self.target_volume = target_volume
        self.volume_change = (target_volume - self.volume) / duration_ms * 1000
    def update(self):
        if self.state in (SoundState.STOPPED, SoundState.PAUSED):
            return

        self.volume, self.volume_change = _update_volume(self.volume, self.target_volume, self.volume_change, self.context.dt)
        self.sound.set_volume(self.volume)

        if self.state == SoundState.PAUSING and self.volume == 0:
            self.sound.stop()
            self.state = SoundState.STOPPED
            return

        self.play_time += 1000 * self.context.dt
        if self.loops != -1 and self.play_time > self.length * (1 + self.loops):
            self.sound.stop()
            self.state = SoundState.STOPPED

    def play(self, start_volume:float, loops:int = 0, fade_in_ms:int|None = None, target_volume:float|None = None):
        self.set_volume(start_volume)
        if fade_in_ms is not None:
            self.change_volume(target_volume, fade_in_ms)

        self.channel   = self.sound.play(loops)
        self.loops     = loops
        self.play_time = 0.0
        self.state     = SoundState.PLAYING
        return self.channel

    def stop(self, fade_out_ms:int|None = None):
        if fade_out_ms is None:
            self.sound.stop()
            self.state = SoundState.STOPPED
        else:
            self.change_volume(0, fade_out_ms)
            self.state = SoundState.PAUSING

    def pause(self):
        if self.state == SoundState.PLAYING and self.channel:
            self.channel.pause()
            self.state = SoundState.PAUSED

    def resume(self):
        if self.state == SoundState.PAUSED and self.channel:
            self.channel.unpause()
            self.state = SoundState.PLAYING

    @property
    def playing(self):
        return self.state == SoundState.PLAYING

    @property
    def paused(self):
        return self.state == SoundState.PAUSED

    @property
    def stopping(self):
        return self.state == SoundState.PAUSING

    def copy(self):
        return Sound(self.context, self.sound, self.volume)