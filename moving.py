import nodex 
import pygame
import math

class Moving(nodex.GameNode):
    def __init__(self, context):
        super().__init__(context)
    
    def update(self):
        cam = self.context.renderer.camera3D("main")
        cam2 = self.context.renderer.camera2D("main")
        angle = cam.rotation
        speed = self.context.dt * 0.3

        if self.context.input.active_keys[pygame.K_s]:
            cam.position.x += math.sin(angle) * speed
            cam.position.y -= math.cos(angle) * speed
        if self.context.input.active_keys[pygame.K_z]:
            cam.position.x -= math.sin(angle) * speed
            cam.position.y += math.cos(angle) * speed
        if self.context.input.active_keys[pygame.K_q]:
            cam.position.x -= math.cos(angle) * speed
            cam.position.y -= math.sin(angle) * speed
        if self.context.input.active_keys[pygame.K_d]:
            cam.position.x += math.cos(angle) * speed
            cam.position.y += math.sin(angle) * speed
            

        if self.context.input.active_keys[pygame.K_DOWN]:
            cam.position.z -= self.context.dt * 0.1
        if self.context.input.active_keys[pygame.K_UP]:
            cam.position.z += self.context.dt * 0.1
        if self.context.input.active_keys[pygame.K_RIGHT]:
            cam.rotation -= self.context.dt 
        if self.context.input.active_keys[pygame.K_LEFT]:
            cam.rotation += self.context.dt

        if self.context.input.active_keys[pygame.K_k]:
            cam.horizon_height -= self.context.dt 
        if self.context.input.active_keys[pygame.K_i]:
            cam.horizon_height += self.context.dt 
  