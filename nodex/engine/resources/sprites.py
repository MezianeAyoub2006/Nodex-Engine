import pygame
import math

pygame.init()
pygame.display.set_mode((640, 360))

class frame:
    __slots__ = ("surface", "duration", "offset")
    def __init__(self, surface:pygame.Surface, duration:int = float("inf"), offset:tuple = (0, 0)):
        self.surface = surface
        self.duration = duration
        self.offset = offset

class sprite:
    __slots__ = ("_frames", "_frame_durations", "total_time")
    def __init__(self, frames:list[frame]|frame):
        self._frames = []
        self._frame_durations = []
        self.total_time = 0
        
        self.frames = frames

    def get_frame(self, time:int) -> frame:
        time = time % self.total_time
        for i, frame_time in enumerate(self._frame_durations):
            if time >= frame_time:
                return self._frames[i]
            
    def get_frame_hash(self, time:int) -> int:
        time = time % self.total_time
        for i, frame_time in enumerate(self._frame_durations):
            if time >= frame_time:
                return len(self._frames) - 1 - i

    @property
    def frames(self) -> list[frame]:
        return list(reversed(self._frames))
    
    @frames.setter
    def frames(self, frames:list[frame]|frame):
        if type(frames) == list:
            self._frames = frames
            self._frame_durations = []
            time = 0
            for frame in self._frames:
                self._frame_durations.append(time)
                time += frame.duration
            self.total_time = time
            self._frames.reverse()
            self._frame_durations.reverse()
        else:
            self._frames = [frames]
            self._frame_durations = [0]
            self.total_time = float("inf")

    @property
    def frame_durations(self) -> list[int]:
        return list(reversed(self._frame_durations))

    def __len__(self):
        return len(self._frames)
    
    def __getitem__(self, index:int):
        return self._frames[len(self._frames) - 1 - index]

SPRITES:dict[str, sprite] = {}

class _sprite_loader:
    def __init__(self):
        self._spritesheet = None
        self._sprite_size = None
        self._width = None
        self._height = None
        self._x = None
        self._y = None

    def load_spritesheet(self, file:str, size:tuple):
        self.set_spritesheet(pygame.image.load(file).convert_alpha(), size)

    def set_spritesheet(self, spritesheet:pygame.Surface, size:tuple):
        self._spritesheet = spritesheet
        self._sprite_size = size
        self._width = self._spritesheet.width // self._sprite_size[0]
        self._height = self._spritesheet.height // self._sprite_size[1]
        self._x = 0; self._y = 0

    def load_sprite(self, names:str|int|list, frames:int = 1, duration:int|list[int] = float("inf"), offset:tuple = (0, 0)):
        def increment(self):
            self._x += 1
            if self._x >= self._width:
                self._x = 0
                self._y += 1

        def add_sprite(names:str|int|list, sprite:sprite):
            if type(names) == list:
                for name in names:
                    SPRITES[name] = sprite
            else:
                SPRITES[names] = sprite
        
        if frames == 1:
            surface = pygame.Surface(self._sprite_size, pygame.SRCALPHA)
            surface.blit(self._spritesheet, (0, 0), (self._x * self._sprite_size[0], self._y * self._sprite_size[1], self._sprite_size[0], self._sprite_size[1]))
            add_sprite(self, names, sprite(frame(surface, offset=offset)))
            increment(self)
        else:
            if type(duration) == list:
                if len(duration) == 1:
                    sprite_frames = []
                    for i in range(frames):
                        surface = pygame.Surface(self._sprite_size, pygame.SRCALPHA)
                        surface.blit(self._spritesheet, (0, 0), (self._x * self._sprite_size[0], self._y * self._sprite_size[1], self._sprite_size[0], self._sprite_size[1]))
                        sprite_frames.append(frame(surface, duration[0], offset))
                        increment(self)
                    add_sprite(names, sprite(sprite_frames))
                else:
                    sprite_frames = []
                    for i in range(frames):
                        surface = pygame.Surface(self._sprite_size, pygame.SRCALPHA)
                        surface.blit(self._spritesheet, (0, 0), (self._x * self._sprite_size[0], self._y * self._sprite_size[1], self._sprite_size[0], self._sprite_size[1]))
                        sprite_frames.append(frame(surface, duration[i], offset))
                        increment(self)
                    add_sprite(names, sprite(sprite_frames))
            else:
                sprite_frames = []
                for i in range(frames):
                    surface = pygame.Surface(self._sprite_size, pygame.SRCALPHA)
                    surface.blit(self._spritesheet, (0, 0), (self._x * self._sprite_size[0], self._y * self._sprite_size[1], self._sprite_size[0], self._sprite_size[1]))
                    sprite_frames.append(frame(surface, duration, offset))
                    increment(self)
                add_sprite(names, sprite(sprite_frames))

    def load_all_sprites_sequentially(self, start:int = 0, stop:int|None = None):
        for i in range(start, stop if stop != None else (self._width * self._height)):
            surface = pygame.Surface(self._sprite_size, pygame.SRCALPHA)
            surface.blit(self._spritesheet, (0, 0), (self._x * self._sprite_size[0], self._y * self._sprite_size[1], self._sprite_size[0], self._sprite_size[1]))
            SPRITES[i] = sprite(frame(surface))
            self._x += 1
            if self._x >= self._width:
                self._x = 0
                self._y += 1

_SPRITE_LOADER = _sprite_loader()

def load_spritesheet(file:str, size:tuple):
    _SPRITE_LOADER.load_spritesheet(file, size)

def set_spritesheet(spritesheet:pygame.Surface, size:tuple):
    _SPRITE_LOADER.set_spritesheet(spritesheet, size)

def load_sprite(names:str|int|list, frames:int = 1, duration:int|list[int] = float("inf"), offset:tuple = (0, 0)):
    _SPRITE_LOADER.load_sprite(names, frames, duration, offset)

def load_all_sprites_sequentially(start:int = 0, stop:int|None = None):
    _SPRITE_LOADER.load_all_sprites_sequentially(start, stop)

def load_single_image(names:str|int|list, file:str, offset:tuple = (0, 0)):
    _sprite = sprite(frame(pygame.image.load(file).convert_alpha(), offset=offset))
    if type(names) == list:
        for name in names:
            SPRITES[name] = _sprite
    else:
        SPRITES[names] = _sprite

def get_sprite(name:str|int) -> sprite:
    return SPRITES.get(name, None)

def get_frame_of_sprite(name:str|int, time:int) -> frame:
    return SPRITES.get(name, None).get_frame(time)