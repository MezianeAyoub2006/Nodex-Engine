import pygame
import math
import pydub
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .context import Context

def _update_volume(volume:float, target_volume:float, volume_change:float|None, delta_time:int) -> tuple[float, float]:
    if volume_change != None:
        volume += volume_change * delta_time
        if volume_change < 0:
            if volume < target_volume:
                volume = target_volume
                volume_change = None
        elif volume_change > 0:
            if volume > target_volume:
                volume = target_volume
                volume_change = None
    return volume, volume_change

class _sound:
    __slots__ = ("sound", "target_volume", "volume", "volume_change", "stop_at_zero", "stopped", "play_time", "length", "loops")
    def __init__(self, sound:pygame.Sound, volume:float = 1):
        self.sound = sound
        self.target_volume = volume
        self.volume = volume
        self.volume_change = None

        self.stop_at_zero = False
        self.stopped = True

        self.play_time = 0
        self.length = self.sound.get_length() * 1000

        self.loops = 0

    def set_volume(self, volume:float):
        self.volume = volume
        self.target_volume = volume
    
    def change_volume(self, target_volume:float, time:int):
        self.target_volume = target_volume
        self.volume_change = (target_volume - self.volume) / time * 1000

    def update(self, delta_time:float):
        self.volume, self.volume_change = _update_volume(self.volume, self.target_volume, self.volume_change, delta_time)
        self.sound.set_volume(self.volume)
        if self.volume == 0 and self.stop_at_zero:
            self.sound.stop()
            self.stopped = True

        self.play_time += 1000 * delta_time
        if self.loops != -1:
            if self.play_time > self.length * (1 + self.loops):
                self.sound.stop()
                self.stopped = True
    
    def play(self, start_volume:float, loops:int = 0, fade_in:int|None = None, target_volume:float|None = None):
        if fade_in == None:
            self.set_volume(start_volume)
            channel = self.sound.play(loops)
        else:
            self.set_volume(start_volume)
            self.change_volume(target_volume, fade_in)
            channel = self.sound.play(loops)
        
        self.loops = loops
        self.stop_at_zero = False
        self.stopped = False
        self.play_time = 0
        return channel

    def stop(self, fade_out:int|None = None):
        if fade_out == None:
            self.set_volume(0)
        else:
            self.change_volume(0, fade_out)
        self.stop_at_zero = True

    @property
    def playing(self):
        return self.stopped == False
    
    @property
    def stopping(self):
        return self.stop_at_zero == True

    def copy(self):
        return Sound(self.file, self.volume)

class Sound(_sound):
    __slots__ = ("file", "sound", "target_volume", "volume", "volume_change", "stop_at_zero", "stopped", "play_time", "length", "loops")
    def __init__(self, file:str, volume:float = 1):
        self.file = file
        super().__init__(pygame.Sound(file), volume)

class SoundLoader:
    def __init__(self, context:"Context"):
        self.context = context

        self.sounds:dict[str, _sound] = {}

    def load_sound(self, name:str, file:str):
        self.sounds[name] = Sound(file)

    def get_sound(self, name:str, copy:bool = True):
        if copy:
            return self.sounds.get(name).copy()
        else:
            return self.sounds.get(name)
