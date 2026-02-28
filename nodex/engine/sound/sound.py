import pygame

def _update_volume(volume:float, target_volume:float, volume_change:float|None, delta_time) -> tuple[float, float]:
    if volume_change != None:
        volume += volume_change * delta_time
        if (volume_change < 0 and volume < target_volume) or (volume_change > 0 and volume > target_volume):
            volume = target_volume
            volume_change = None
    return volume, volume_change

class Sound:
    def __init__(self, context, sound:pygame.Sound, volume:float = 1):
        self.context = context
        self.sound = sound
        self.target_volume = volume
        self.volume = volume
        self.volume_change = None

        self.stop_at_zero = False
        self.stopped = True

        self.play_time = 0
        self.length = self.sound.get_length() * 1000

        self.loops = 0
        self._paused = False
        self.channel:pygame.Channel|None = None

    def set_volume(self, volume:float):
        self.volume = volume
        self.target_volume = volume
    
    def change_volume(self, target_volume:float, time:int):
        self.target_volume = target_volume
        self.volume_change = (target_volume - self.volume) / time * 1000

    def update(self):
        if self._paused:
            return

        self.volume, self.volume_change = _update_volume(self.volume, self.target_volume, self.volume_change, self.context.dt)
        self.sound.set_volume(self.volume)
        if self.volume == 0 and self.stop_at_zero:
            self.sound.stop()
            self.stopped = True

        self.play_time += 1000 * self.context.dt
        if self.loops != -1:
            if self.play_time > self.length * (1 + self.loops):
                self.sound.stop()
                self.stopped = True
    
    def play(self, start_volume:float, loops:int = 0, fade_in:int|None = None, target_volume:float|None = None):
        if fade_in is None:
            self.set_volume(start_volume)
        else:
            self.set_volume(start_volume)
            self.change_volume(target_volume, fade_in)
        
        self.channel = self.sound.play(loops)
        self.loops = loops
        self.stop_at_zero = False
        self.stopped = False
        self._paused = False
        self.play_time = 0
        return self.channel

    def stop(self, fade_out:int|None = None):
        if fade_out is None:
            self.set_volume(0)
        else:
            self.change_volume(0, fade_out)
        self.stop_at_zero = True

    def pause(self):
        if self.playing and self.channel:
            self.channel.pause()
            self._paused = True

    def resume(self):
        if self._paused and self.channel:
            self.channel.unpause()
            self._paused = False

    @property
    def paused(self):
        return self._paused

    @property
    def playing(self):
        return self.stopped == False
    
    @property
    def stopping(self):
        return self.stop_at_zero == True

    def copy(self):
        return Sound(self.context, self.sound, self.volume)
