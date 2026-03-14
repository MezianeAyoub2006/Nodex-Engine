import math 
import numpy as np

def make_quad(x1:int, y1:int, x2:int, y2:int) -> np.ndarray:
    return np.array([
        x1, y1,  0.0, 0.0,
        x2, y1,  1.0, 0.0,
        x1, y2,  0.0, 1.0,
        x2, y1,  1.0, 0.0,
        x2, y2,  1.0, 1.0,
        x1, y2,  0.0, 1.0,
    ], dtype='f4')

def pixels_to_ndc(ox:int, oy:int, sw:int, sh:int, W:int, H:int) -> tuple:
    x1 = (ox / W) * 2 - 1
    y1 = 1 - ((oy + sh) / H) * 2
    x2 = ((ox + sw) / W) * 2 - 1
    y2 = 1 - (oy / H) * 2
    return x1, y1, x2, y2

def world_to_screen(pos, camera, screen_size):
    if camera.position.z < 0:
        return None, None
    wx, wy = pos[:2]
    wz = pos[2] if len(pos) > 2 else 0.0
    dx = wx - camera.position.x
    dy = wy - camera.position.y
    cosA = math.cos(camera.rotation)
    sinA = math.sin(camera.rotation)
    xi = cosA * dx + sinA * dy
    yi = -sinA * dx + cosA * dy
    if yi <= 0.0001:
        return None, None
    scale = max(0.001, abs(camera.position.z))
    depth = scale / yi
    screenY = depth + camera.horizon_height
    uv_y = 1.0 - screenY
    uv_y -= (wz / yi)
    uv_x = xi / yi + 0.5
    w, h = screen_size
    return (uv_x * w, (1 - uv_y) * h), min(max(1/yi, 0.2) / 12, 8)

def angle_to_frame_index(camera, position, num_frames=4, element_angle=0.0) -> int:
    element_angle += 1
    angle = math.atan2(
        camera.position.x - position[0],
        camera.position.y - position[1]
    ) - element_angle
    angle = (-angle) % (2 * math.pi)
    return int((angle / (2 * math.pi)) * num_frames) % num_frames

def distance2D(pos1, pos2):
    return math.sqrt(
        (pos1[0] - pos2[0]) ** 2 + 
        (pos1[1] - pos2[1]) ** 2
    )

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]