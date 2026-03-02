from .shader_pass import ShaderPass
import pygame


class PygamePass(ShaderPass):
    def __init__(self, context, frag_prog=None, vert_prog=None):
        super().__init__(context, frag_prog, vert_prog)
        self._surf = pygame.Surface(context.window.internal_size, pygame.SRCALPHA)
        self.dump_pygame_surf("tex", self._surf, slot=0)

    @property
    def surface(self) -> pygame.Surface:
        return self._surf

    def blit(self, surface: pygame.Surface, position: tuple) -> None:
        self._surf.blit(surface, position)

    def fill(self, color=(0, 0, 0, 0)) -> None:
        self._surf.fill(color)

    def render(self) -> None:
        self.dump_pygame_surf("tex", self._surf)
        self._surf.fill((0, 0, 0, 0))
        super().render()