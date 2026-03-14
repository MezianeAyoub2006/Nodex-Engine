import nodex 
import impl     
import math
import pygame
import random
from .obstacle import Obstacle


class ObstaclesManager(nodex.GameNode):
    def __init__(self, context, player: "impl.Player"):
        super().__init__(context)
        self.player = player
        self._last_spawned_index = None

    def spawn(self, type, position, circuit_index):
        obs = Obstacle(self.context, position, type, self.player)
        obs.circuit_index = circuit_index
        self.add_child(obs)

    def update(self):
        n = len(impl.CIRCUIT)
        player_index = self.player.closest_circuit_index
        opposite_index = (player_index + n // 2) % n
        if self.player.frozen:
            self._last_spawned_index = None 
            self.children = set()

        if self._last_spawned_index is None:
            self._last_spawned_index = opposite_index

        if opposite_index != self._last_spawned_index:
            self._last_spawned_index = opposite_index
            vector = impl.CIRCUIT[opposite_index]
            offset = ((random.random() - 0.5) * 0.05, (random.random() - 0.5) * 0.05)
            position = (vector.x + offset[0], vector.y + offset[1])
            if impl.material_under(self.context, pygame.Vector2(*position)) != impl.Material.WATER:
                self.spawn(f"ice{0 if random.random() < 0.8 else 1}", position, opposite_index)

        for obstacle in self.children:
            if obstacle.circuit_index == (player_index - 1) % n:
                obstacle.kill()