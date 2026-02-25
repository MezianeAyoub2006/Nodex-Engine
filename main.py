import nodex.engine
import pygame 
import math

class Test(nodex.engine.GameNode):
    def __init__(self, context:"nodex.engine.Context"):
        super().__init__(context)
        self._fonts = {}
        self.ground = nodex.WorldLayer(context) 
        with open("shaders/outline.glsl", "r", encoding = "utf-8") as f:
            self.overlay = nodex.PygameLayer(context, f.read()) 
        self.ground_surf = pygame.image.load("assets/ground.png")
        self.font = pygame.font.SysFont("consolas", 16, True) 
       
    def update(self): 
        self.ground.draw(self.ground_surf, (0, 0))
        self.overlay.blit(self.font.render(f"{round(self.context.fps)} FPS", False, (255, 255, 255)), (5, 5))
        self.ground.render()
        self.overlay.render()
        speed = 500

        if self.context.active_keys[pygame.K_RIGHT]:
            self.ground.camera.position.x += math.cos(self.ground.camera.rotation) * speed * self.context.dt
            self.ground.camera.position.y += math.sin(self.ground.camera.rotation) * speed * self.context.dt
        if self.context.active_keys[pygame.K_LEFT]:
            self.ground.camera.position.x -= math.cos(self.ground.camera.rotation) * speed * self.context.dt
            self.ground.camera.position.y -= math.sin(self.ground.camera.rotation) * speed * self.context.dt
        if self.context.active_keys[pygame.K_DOWN]:
            self.ground.camera.position.x -= math.sin(self.ground.camera.rotation) * speed * self.context.dt
            self.ground.camera.position.y += math.cos(self.ground.camera.rotation) * speed * self.context.dt
        if self.context.active_keys[pygame.K_UP]:
            self.ground.camera.position.x += math.sin(self.ground.camera.rotation) * speed * self.context.dt
            self.ground.camera.position.y -= math.cos(self.ground.camera.rotation) * speed * self.context.dt
        if self.context.active_keys[pygame.K_z]:
            self.ground.camera.zoom *= 5 ** self.context.dt
        if self.context.active_keys[pygame.K_s]:
            self.ground.camera.zoom /= 5 ** self.context.dt
        if self.context.active_keys[pygame.K_q]:
            self.ground.camera.rotation += 30 * self.context.dt
        if self.context.active_keys[pygame.K_d]:
            self.ground.camera.rotation -= 30 * self.context.dt


context = nodex.engine.Context((250, 240), 2, True) 
context.add_game_node(Test(context))
context.run()