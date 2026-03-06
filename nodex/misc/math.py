import math 


def cam_position_angle(camera, position: tuple) -> float:
    dx = position[0] - camera.position.x
    dy = position[1] - camera.position.y
    return math.atan2(dx, dy) - camera.rotation