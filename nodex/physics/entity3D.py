import nodex 
import pygame 

class Entity3D(nodex.GameNode):
    def __init__(self, context):
        super().__init__(context) 
        self.position = pygame.math.Vector3(0, 0, 0)
        self.velocity = pygame.math.Vector3(0, 0, 0) 
        self.down_gravity = 0.05
        self.up_gravity = 0.05

    
    def update(self): 
        self.position.x += self.velocity.x * self.context.dt 
        self.position.y += self.velocity.y * self.context.dt 
        self.position.z += self.velocity.z * self.context.dt
        self.limit_z()
        self.apply_gravity()

    def apply_gravity(self):
        if self.velocity.z > 0:
            self.velocity.z -= self.up_gravity * self.context.dt
        else:
            self.velocity.z -= self.down_gravity * self.context.dt
            
    def limit_z(self): 
        
        if self.position.z < 0:
            self.position.z = 0

    def render(self):
        pass 

    def set_position(self, x, y, z):
        self.position.x = x 
        self.position.y = y 
        self.position.z = z

    def set_velocity(self, x, y, z):
        self.velocity.x = x 
        self.velocity.y = y 
        self.velocity.z = z
