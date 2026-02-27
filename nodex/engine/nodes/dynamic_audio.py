#for handling dynamic audio
class dynamic_sound_manager:
    def __init__(self, sound_manager:, listening_distance:int|float):
        self.sound_manager = sound_manager
        self.listening_position = (0, 0)
        self.listening_distance = listening_distance

    def set_listening_position(self, position:tuple):
        self.listening_position = position

    def play_sound_at_position(self, channel_type:str, position:tuple, sound:sound, start_volume:float, loops:int = 0, fade_in:int|None = None, target_volume:float|None = None):
        distance_to_listening_position = math.dist(position, self.listening_position)
        if distance_to_listening_position <= self.listening_distance:
            volume_factor = 1 - (distance_to_listening_position / self.listening_distance)
            if target_volume == None:
                self.sound_manager.play_sound(channel_type, sound, start_volume * volume_factor, loops, fade_in, target_volume)
            else:
                self.sound_manager.play_sound(channel_type, sound, start_volume * volume_factor, loops, fade_in, target_volume * volume_factor)
