import math 

from .config import PlayerConfig 

class PlayerCamera:
    def __init__(self, entity, angle_ref):
        self.x = entity.position.x
        self.y = entity.position.y
        self.z = entity.position.z + PlayerConfig.CAM_HEIGHT
        self.rotation = 0.0
        self.distance = PlayerConfig.CAM_BASE_DIST
        self.angle_ref = angle_ref

    def update_distance(self, z, dt):
        target = PlayerConfig.CAM_BASE_DIST - z * PlayerConfig.CAM_JUMP_SCALE
        t = 1.0 - math.exp(-PlayerConfig.CAM_DIST_SPEED * dt)
        self.distance += (target - self.distance) * t

    def follow(self, entity, real_angle, dt, camera, speed):
        angle = self.angle_ref()
        target_x = entity.position.x - math.cos(real_angle) * self.distance
        target_y = entity.position.y + math.sin(real_angle) * self.distance
        target_z = entity.position.z + PlayerConfig.CAM_HEIGHT
        target_rot = math.pi - angle

        t = 1.0 - math.exp(-speed * dt)
        self.x += (target_x - self.x) * t
        self.y += (target_y - self.y) * t
        self.z += (target_z - self.z) * t

        diff = (target_rot - self.rotation) % (2 * math.pi)
        if diff > math.pi:
            diff -= 2 * math.pi
        self.rotation += diff * t

        camera.position.x = self.x
        camera.position.y = self.y
        camera.position.z = self.z
        camera.rotation = self.rotation
    def sync_from(self, camera):
        self.x = camera.position.x
        self.y = camera.position.y
        self.z = camera.position.z
        self.rotation = camera.rotation

