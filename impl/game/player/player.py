import nodex
import pygame
import math
import impl

from ..circuit import CIRCUIT, CircuitVector
from .animation import PlayerAnimation
from .camera import PlayerCamera 
from .config import PlayerConfig, MATERIAL_CONFIG
from .key import WASD, ZQSD, ARROWS

START_POS = (0.80887, 0.575599, 0)

class Player(nodex.GameNode):
    def __init__(self, context, mode7_viewport, billboard_viewport):
       
        self.mode7_viewport = mode7_viewport
        self.billboard_viewport = billboard_viewport
        super().__init__(context)

        self.entity = self.make_entity((0, 0, 0))
        self.load()
       
        self.speed = PlayerConfig.MIN_SPEED
        
        self.drift = 1
        self.direction = None
        self.accelerate = False
        self.material = None
        self.cam_follow = True
        self.record = False

        self.key = ARROWS
        self.anim = PlayerAnimation()
        self.cam = PlayerCamera(self.entity, lambda: self.angle)
          
    def load(self):
        self.frozen = False
        self.angle = math.pi + 0.35
        self.death_timer = 2
        self.temperature = 20
        self.max_speed = 0.2
        self.score = 0
        self.entity.set_position(*START_POS)
        self.entity.set_velocity(0, 0, 0)
        self.freeze_timer = 1
        self.respawn_timer = 3

    @property
    def real_angle(self):
        return self.angle - math.pi / 2

    @property
    def camera(self):
        return self.context.renderer.camera3D(self.mode7_viewport)

    @property
    def mode7_pass(self):
        return self.context.renderer.viewports[self.mode7_viewport].pass_

    @property
    def on_ground(self):
        return self.entity.position.z <= 0.001

    @property
    def closest_circuit_vector(self) -> CircuitVector:
        return CIRCUIT[self.closest_circuit_index]

    @property
    def circuit_direction_dot(self) -> float:
        cv = self.closest_circuit_vector
        self_vec = pygame.math.Vector2(math.cos(self.angle), math.sin(self.angle))
        return cv.direction.dot(self_vec)

    def make_entity(self, position):
        entity = nodex.Entity3D(self.context)
        entity.position.x = position[0]
        entity.position.y = position[1]
        entity.position.z = position[2]
        entity.up_gravity = PlayerConfig.UP_GRAVITY
        entity.down_gravity = PlayerConfig.DOWN_GRAVITY
        return entity

    def jump(self):
        self.context.sounds.track("jump", 0.7)
        self.entity.velocity.z = PlayerConfig.JUMP_FORCE

    def toggle_cam_follow(self):
        self.cam_follow = not self.cam_follow
        if self.cam_follow:
            self.cam.sync_from(self.camera)

    def handle_movements(self):
        dt = self.context.dt
        self.accelerate = False

        if self.context.input.active_keys[self.key.left] and self.on_ground:
            self.angle -= PlayerConfig.TURN_SPEED * dt * (self.speed * self.drift * 2 + 1)
            self.direction = "left"
        if self.context.input.active_keys[self.key.right] and self.on_ground:
            self.angle += PlayerConfig.TURN_SPEED * dt * (self.speed * self.drift * 2 + 1)
            self.direction = "right"

        if self.context.input.active_keys[self.key.up]:
            self.accelerate = True
            self.speed += PlayerConfig.ACCEL * dt
        else:
            self.apply_friction()

        if self.context.input.active_keys[self.key.down]:
            self.speed -= PlayerConfig.ACCEL * dt

        if self.context.input.pressed_keys[self.key.jump] and self.on_ground and not self.material == impl.Material.WATER:
            self.jump()

        can_drift = (
            self.context.input.active_keys[self.key.drift]
            and self.speed > self.max_speed * 0.8
            and self.direction is not None
            and self.material != impl.Material.WATER
        )
        self.drift = 5 if can_drift else 1

        if self.context.input.pressed_keys[pygame.K_y]:
            self.record = not self.record

    def apply_friction(self):
        self.speed *= PlayerConfig.FRICTION ** self.context.dt

    def handle_speed(self):
        config = MATERIAL_CONFIG.get(self.material, MATERIAL_CONFIG[impl.Material.DEFAULT])
        max_speed = self.max_speed * config["speed_ratio"]

        if self.on_ground:
            if self.speed > max_speed:
                t = 1.0 - math.exp(-config["drag"] * self.context.dt)
                self.speed += (max_speed - self.speed) * t
            self.speed = min(max(PlayerConfig.MIN_SPEED, self.speed), max_speed)
        else:
            self.speed = min(max(PlayerConfig.MIN_SPEED, self.speed), self.max_speed)

    def handle_velocity(self):
        self.entity.velocity.x = -math.cos(self.real_angle) * self.speed
        self.entity.velocity.y =  math.sin(self.real_angle) * self.speed

    def handle_camera(self):
        self.cam.update_distance(self.entity.position.z, self.context.dt)
        if self.cam_follow:
            self.cam.follow(self.entity, self.real_angle, self.context.dt, self.camera, self.cam_speed)
        self.mode7_pass.dynamic_follow((self.entity.position.x, self.entity.position.y))

    def handle_animation(self):
        coef = 2
        in_water = self.material == impl.Material.WATER and self.entity.position.z == 0

        if in_water:
            self.anim.set(4)
        elif self.entity.position.z > 0:
            self.anim.set(2)
        elif self.drift != 1:
            self.anim.set(3)
            self.anim.frame = 0 if self.direction == "left" else 1
            return
        elif self.accelerate:
            self.anim.set(1)
            coef = self.speed * 20
        else:
            self.anim.set(0)

        self.anim.tick(coef, self.context.dt)

    def handle_material(self):
        self.material = impl.material_under(self.context, self.entity.position)

    def handle_recording(self):
        if self.record and int(self.context.timer) != int(self.context.timer - self.context.dt):
            print(self.angle, self.entity.position.x, self.entity.position.y)

    def render_shadow(self, alpha=PlayerConfig.SHADOW_ALPHA, color=nodex.Color.BLACK, size=PlayerConfig.SHADOW_SIZE):
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*color, alpha), (size // 2, size // 2), size // 2)
        w, h   = self.context.window.internal_size
        ox, oy = PlayerConfig.SHADOW_OFFSET
        self.context.renderer.draw_world(
            self.mode7_viewport, surf,
            position=(w // 2 - size // 2 + ox, h // 2 - size // 2 + oy)
        )

    def render(self):
        if not self.frozen:
            self.context.renderer.draw(
                self.billboard_viewport,
                f"player.{self.anim.frame}.{self.anim.animation}",
                position=self.entity.position,
                angle=self.angle
            )
        else:
            self.context.renderer.draw(
                self.billboard_viewport,
                f"player_ice",
                position=self.entity.position,
                angle=self.angle
            )
  
        self.context.renderer.draw("mode7", "ground")
        if not self.on_ground:
            self.render_shadow()

        if self.speed > self.max_speed * 0.8 and self.circuit_direction_dot > 0:
            prev_score = self.score
            self.score += self.context.dt * (2 if self.temperature == 100 else 1)
            if int(self.score) != int(prev_score):
                self.context.sounds.track("score", 0.5)

        self.max_speed = min(PlayerConfig.BEGIN_MAX_SPEED + self.score / 1000, PlayerConfig.MAX_SPEED)
    
    def handle_temperature(self):
        if self.material == impl.Material.GRASS:
            if self.temperature < PlayerConfig.CAMPFIRE_TEMP:
                self.temperature += PlayerConfig.TEMPERATURE_UP_SPEED * self.context.dt
            else:
                self.temperature -= PlayerConfig.TEMPERATURE_UP_SPEED * self.context.dt 
        else:
            coef = 1
            direction = {0 : 1, 1 : -1}[self.speed < self.max_speed * 0.8]
            if direction == 1:
                speed = PlayerConfig.TEMPERATURE_UP_SPEED 
            else:
                speed = PlayerConfig.TEMPERATURE_DOWN_SPEED 
            if self.on_ground and self.material == impl.Material.WATER:
                coef = PlayerConfig.TEMPERATURE_WATER_COEF
            self.temperature += direction * speed * self.context.dt * coef
        self.temperature = min(max(self.temperature, 0), 100)

    def handle_death(self):
        if self.temperature <= 0:
            if not self.frozen:
                self.context.sounds.track("freeze")
            self.frozen = True 
            self.apply_friction()
            if self.context.input.pressed_keys[self.key.jump]: 
                self.load()
                self.context.sounds.track("respawn")
            if self.context.input.pressed_keys[pygame.K_ESCAPE] and self.context.scenes.transition_done:
                self.context.scenes.transition("menu", 2, callback=lambda : self.context.post_process.enable_effect("blur"))
                self.context.sounds.crossfade("winter-waltz", 2000, 0.3)   

    def handle_key(self):
        profile = self.context.globals["key_profile"] 
        if profile == "WASD":
            self.key = WASD 
        if profile == "ZQSD":
            self.key = ZQSD 
        if profile == "ARROWS":
            self.key = ARROWS

    def update(self):
        self.handle_material()
        if not self.frozen:
            self.handle_movements()
        self.handle_speed()
        self.handle_velocity()
        self.handle_camera()
        self.entity.update()
        self.handle_animation()
        self.handle_recording()
        self.handle_temperature()
        self.handle_death() 
        self.handle_key()
        if self.respawn_timer > 0:
            self.respawn_timer -= self.context.dt 
        else:
            self.respawn_timer = 0

    @property
    def cam_speed(self):
        t = max(0.0, self.respawn_timer / 3) ** 0.3
        return PlayerConfig.CAM_SPEED + t * (PlayerConfig.CAM_RESPAWN_SPEED - PlayerConfig.CAM_SPEED)
    
    @property
    def closest_circuit_index(self) -> int:
        pos = (self.entity.position.x, self.entity.position.y)
        return min(range(len(CIRCUIT)), key=lambda i: nodex.distance2D((CIRCUIT[i].x, CIRCUIT[i].y), pos))