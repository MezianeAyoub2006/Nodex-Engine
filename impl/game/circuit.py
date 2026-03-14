from dataclasses import dataclass
import pygame 
import math

CIRCUIT_RECORDED_VECTORS = [
    (2.975578853737047,  0.88572,  0.83783),
    (1.708039810224290,  0.54026,  0.90125),
    (0.718500250040524,  0.16367,  0.88432),
    (-0.505670929739862, 0.08781,  0.49823),
    (-0.176591689746855, 0.19908,  0.14116),
    (-1.775428849987364, 0.54052,  0.06037),
    (-2.619801649499711, 0.88947,  0.20186),
    (-4.364109229667954, 0.61161,  0.39663),
    (-3.121232149996358, 0.28134,  0.57660),
    (-2.212182470334375, 0.60168,  0.61075),
    (-2.317899534327346, 0.84723,  0.73679),
]
@dataclass
class CircuitVector:
    angle: float
    x: float
    y: float
    direction: pygame.math.Vector2  

def _build_circuit():
    return [
        CircuitVector(a, x, y, pygame.math.Vector2(math.cos(a), math.sin(a)))
        for a, x, y in CIRCUIT_RECORDED_VECTORS
    ]

CIRCUIT = _build_circuit()