from dataclasses import dataclass

ANIMATION_LENGTHS = [2, 4, 2, 2, 2]

@dataclass
class PlayerAnimation:
    animation: int = 0
    frame: int = 0
    counter: float = 0.0
    def tick(self, coef, dt):
        self.counter += coef * dt
        self.frame = int(self.counter) % ANIMATION_LENGTHS[self.animation]

    def set(self, animation):
        self.animation = animation

