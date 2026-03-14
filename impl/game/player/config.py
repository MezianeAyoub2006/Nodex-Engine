import impl

class PlayerConfig:
    CAM_SPEED = 10
    CAM_RESPAWN_SPEED = 2
    CAM_BASE_DIST = -0.04
    CAM_JUMP_SCALE = 2.0
    CAM_DIST_SPEED = 4.0
    CAM_HEIGHT = 0.02
    JUMP_FORCE = 0.15
    MAX_SPEED = 0.325
    MIN_SPEED = 0.0
    ACCEL = 0.2
    TURN_SPEED = 1.0
    UP_GRAVITY = 0.4
    DOWN_GRAVITY = 0.6
    SHADOW_SIZE = 8
    SHADOW_ALPHA = 100
    SHADOW_OFFSET = (-2, 1)
    FRICTION = 0.1
    BEGIN_MAX_SPEED = 0.2
    TEMPERATURE_UP_SPEED = 5
    TEMPERATURE_DOWN_SPEED = 10
    TEMPERATURE_WATER_COEF = 2.5
    CAMPFIRE_TEMP = 20

MATERIAL_CONFIG = {
    impl.Material.WATER: {"speed_ratio": 0.6, "drag": 8.0},
    impl.Material.ICE: {"speed_ratio": 1.0, "drag": 0.2},
    impl.Material.GRASS: {"speed_ratio": 1.0, "drag": 1.0},
    impl.Material.DEFAULT: {"speed_ratio": 1.0, "drag": 1.0},
}