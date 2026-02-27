import pygame
import math
import pydub
from typing import TYPE_CHECKING

from .sounds import _sound, Sound

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

class ChannelData:
    __slots__ = ("volume", "target_volume", "volume_change", "paused")
    def __init__(self, volume:float):
        self.volume = volume
        self.target_volume = volume
        self.volume_change = None
        self.paused = False

    def set_volume(self, volume:float):
        self.volume = volume
        self.target_volume = volume
        
    def change_volume(self, target_volume:float, time:int):
        self.target_volume = target_volume
        self.volume_change = (target_volume - self.volume) / time * 1000
    
    def update(self, dt:float):
        self.volume, self.volume_change = _update_volume(self.volume, self.target_volume, self.volume_change, dt)
        
    def pause(self):
        self.paused = True
        
    def unpause(self):
        self.paused = False

class MusicData:
    __slots__ = ("file", "file_name", "target_volume", "volume", "volume_change", "loops", "stop_at_zero", "stopped", "paused")
    def __init__(self):
        self.file = None
        self.file_name = None
        self.target_volume = 0
        self.volume = 0
        self.volume_change = 0
        self.loops = 0

        self.stop_at_zero = False
        self.stopped = True

        self.paused = False

    def play(self, file:str, start_volume:float, loops:int = 0, fade_in:int|None = None, target_volume:float|None = None):
        if self.file != file:
            pygame.mixer.music.load(file)
            self.file = file
            self.file_name = self.get_name_of_file(file)

        if fade_in == None:
            self.set_volume(start_volume)
        else:
            self.set_volume(start_volume)
            self.change_volume(target_volume, fade_in)

        self.loops = loops
        self.stop_at_zero = False
        self.stopped = False

        pygame.mixer.music.play(loops)
        
    def set_volume(self, volume:float):
        self.volume = volume
        self.target_volume = volume
        
    def change_volume(self, target_volume:float, time:int):
        self.target_volume = target_volume
        self.volume_change = (target_volume - self.volume) / time * 1000

    def update(self, dt:float):
        self.volume, self.volume_change = _update_volume(self.volume, self.target_volume, self.volume_change, dt)
        
        pygame.mixer.music.set_volume(self.volume)

        if self.volume == 0 and self.stop_at_zero:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            self.file = None
            self.file_name = None
            self.stopped = True

    def stop(self, fade_out:int|None = None):
        if fade_out == None:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            self.file = None
            self.file_name = None
            self.stopped = True
        else:
            self.change_volume(0, fade_out)
        self.stop_at_zero = True

    @property
    def playing(self):
        return self.stopped == False
        
    @property
    def stopping(self):
        return self.stop_at_zero == True

    def get_name_of_file(self, file:str):
        file_parts = file.split("/")
        file_name = file_parts[len(file_parts) - 1]
        if file_name.endswith(".ogg"):
            file_name = file_name.removesuffix(".ogg")
        if file_name.endswith(".mp3"):
            file_name = file_name.removesuffix(".mp3")
        if file_name.endswith(".wav"):
            file_name = file_name.removesuffix(".wav")
        return file_name

    def pause(self):
        self.paused = True
        pygame.mixer.music.pause()

    def unpause(self):
        self.paused = False
        pygame.mixer.music.unpause()

class Mixer:
    def __init__(self, context:"Context", channels:int, default_channel_volume:float, master_volume:float = 1, minimum_volume:int = 0.1):
        self.context = context

        pygame.mixer.set_num_channels(channels)
        
        self.channels:dict[pygame.Channel:str] = {}
        self.channels_data:dict[str:ChannelData] = {}
        self.playing_sounds:list[Sound] = []
        self.sound_channels:dict[Sound:pygame.Channel] = {}
        self.named_playing_sounds:dict[str:Sound] = {}

        self.default_channel_volume = default_channel_volume

        self.paused = False

        self.master_volume = master_volume
        self.target_master_volume = master_volume
        self.master_volume_change = None

        self.minimum_volume = minimum_volume

        self.music = MusicData()

    def set_channel_type_volume(self, channel_type:str, volume:float):
        if not channel_type in self.channels_data:
            self.channels_data[channel_type] = ChannelData(self.default_channel_volume)
        self.channels_data[channel_type].set_volume(volume)

    def change_channel_type_volume(self, channel_type:str, target_volume:float, time:int):
        if not channel_type in self.channels_data:
            self.channels_data[channel_type] = ChannelData(self.default_channel_volume)
        self.channels_data[channel_type].change_volume(target_volume, time)

    def set_master_volume(self, volume:float):
        self.master_volume = volume

    def change_master_volume(self, target_volume:float, time:int):
        self.target_master_volume = target_volume
        self.master_volume_change = (target_volume - self.master_volume) / time * 1000
    
    def update_channel_with_channel_data(self, channel_type:str, channel:pygame.Channel):
        if not channel_type in self.channels_data:
            self.channels_data[channel_type] = ChannelData(self.default_channel_volume)
        channel.set_volume(self.channels_data[channel_type].volume)

    def play_sound(self, channel_type:str, sound:Sound, start_volume:float, loops:int = 0, fade_in:int|None = None, target_volume:float|None = None):
        if target_volume == None:
            if start_volume < self.minimum_volume:
                return
        else:
            if target_volume < self.minimum_volume:
                return
        channel = sound.play(start_volume, loops, fade_in, target_volume)
        self.channels[channel] = channel_type
        self.sound_channels[sound] = channel
        self.playing_sounds.append(sound)
        self.update_channel_with_channel_data(channel_type, channel)

    def play_named_sound(self, channel_type:str, sound_name:str, sound:Sound, start_volume:float, loops:int = 0, fade_in:int|None = None, target_volume:float|None = None, single:bool = False):
        if target_volume == None:
            if start_volume < self.minimum_volume:
                return
        else:
            if target_volume < self.minimum_volume:
                return
        if single:
            if sound_name not in self.named_playing_sounds:
                channel = sound.play(start_volume, loops, fade_in, target_volume)
                self.channels[channel] = channel_type
                self.sound_channels[sound] = channel
                self.named_playing_sounds[sound_name] = sound
                self.update_channel_with_channel_data(channel_type, channel)
        else:
            channel = sound.play(start_volume, loops, fade_in, target_volume)
            self.channels[channel] = channel_type
            self.named_playing_sounds[sound_name] = sound
            self.sound_channels[sound] = channel
            self.update_channel_with_channel_data(channel_type, channel)

    def update(self):
        if self.master_volume_change != None:
            self.master_volume += self.master_volume_change * self.context.dt
            if self.master_volume_change < 0:
                if self.master_volume < self.target_master_volume:
                    self.master_volume = self.target_master_volume
                    self.master_volume_change = None
            elif self.master_volume_change > 0:
                if self.master_volume > self.target_master_volume:
                    self.master_volume = self.target_master_volume
                    self.master_volume_change = None

        for channel_data in self.channels_data.values():
            if channel_data.paused == False:
                channel_data.update(self.context.dt)
        
        for channel in self.channels:
            channel_type = self.channels[channel]
            channel_data:ChannelData = self.channels_data[channel_type]
            if channel_data.paused == False:
                channel.unpause()

        for sound in self.playing_sounds.copy():
            if (sound_channel := self.sound_channels[sound]) in self.channels:
                if (channel_type := self.channels[sound_channel]) in self.channels_data:
                    if self.channels_data[channel_type].paused == False:
                        sound.update(self.context.dt)
                        if sound.stopped:
                            self.playing_sounds.remove(sound)
                            del self.sound_channels[sound]
        
        named_playing_sounds = self.named_playing_sounds.copy()
        for sound_name, sound in zip(named_playing_sounds.keys(), named_playing_sounds.values()):
            if (sound_channel := self.sound_channels[sound]) in self.channels:
                if (channel_type := self.channels[sound_channel]) in self.channels_data:
                    if self.channels_data[channel_type].paused == False:
                        sound.update(self.context.dt)
                        if sound.stopped:
                            del self.named_playing_sounds[sound_name]
                            del self.sound_channels[sound]
    
        for channel in self.channels.copy():
            if channel.get_busy() == False and self.channels_data[self.channels[channel]].paused == False:
                del self.channels[channel]
        
        self.music.update(self.context.dt)
        if not self.music.paused:
            pygame.mixer.music.set_volume(self.music.volume * self.master_volume)

    def pause_all(self):
        for channel_data in self.channels_data.values():
            channel_data.pause()
        for channel in self.channels:
            channel.pause()
        self.music.pause()
        self.paused = True

    def pause_channels(self, channel_types:str):
        for channel_type in channel_types:
            if channel_type in self.channels_data:
                self.channels_data[channel_type].pause()
                for channel in self.channels:
                    if self.channels[channel] == channel_type:
                        channel.pause()
        
    def unpause_all(self):
        for channel_data in self.channels_data.values():
            channel_data.unpause()
        for channel in self.channels:
            channel.unpause()
        self.music.unpause()
        self.paused = False

    def unpause_channels(self, channel_types:str):
        for channel_type in channel_types:
            if channel_type in self.channels_data:
                self.channels_data[channel_type].unpause()
                for channel in self.channels:
                    if self.channels[channel] == channel_type:
                        channel.unpause()

    def play_music(self, file:str, start_volume:float, loops:int = 0, fade_in:int|None = None, target_volume:float|None = None):
        self.music.play(file, start_volume, loops, fade_in, target_volume)
    
    def stop_music(self, fade_out:int|None = None):
        self.music.stop(fade_out)

    def pause_music(self):
        self.music.pause()

    def unpause_music(self):
        self.music.unpause()

    def stop_named_sound(self, sound_name:str, fade_out:int|None = None):
        if sound_name in self.named_playing_sounds:
            self.named_playing_sounds[sound_name].stop(fade_out)

    def stop_sounds_in_channel_type(self, channel_type:str, fade_out:int|None = None):
        for sound in self.sound_channels:
            if self.channels[self.sound_channels[sound]] == channel_type:
                sound.stop(fade_out)
    
    def stop_all_sounds(self, fade_out:int|None = None):
        for sound in self.playing_sounds:
            sound.stop(fade_out)
        for sound in self.named_playing_sounds.values():
            sound.stop(fade_out)

    @property
    def playing_music(self):
        return self.music.playing

class DynamicMixer:
    def __init__(self, context:"Context", mixer:Mixer, listening_distance:int|float):
        self.context = context
        
        self.mixer = mixer
        self.listening_position = (0, 0)
        self.listening_distance = listening_distance

    def set_listening_position(self, position:tuple):
        self.listening_position = position

    def play_sound_at_position(self, channel_type:str, position:tuple, sound:Sound, start_volume:float, loops:int = 0, fade_in:int|None = None, target_volume:float|None = None):
        distance_to_listening_position = math.dist(position, self.listening_position)
        if distance_to_listening_position <= self.listening_distance:
            volume_factor = 1 - (distance_to_listening_position / self.listening_distance)
            if target_volume == None:
                self.mixer.play_sound(channel_type, sound, start_volume * volume_factor, loops, fade_in, target_volume)
            else:
                self.mixer.play_sound(channel_type, sound, start_volume * volume_factor, loops, fade_in, target_volume * volume_factor)
