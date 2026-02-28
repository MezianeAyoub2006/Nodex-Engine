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
        self.context.load_image("ground", "assets/ground.png")
        self.font = pygame.font.SysFont("consolas", 16, True) 
        self.context.load_sound("test", "assets/test.wav")
        self.sound = self.context.sound_manager.track("test") 
        
        self.sound.play(1)

       
    def update(self): 
        self.ground.draw(self.context.get_image("ground"), (0, 0))
        self.overlay.blit(self.font.render(f"{round(self.context.fps)} FPS", False, (255, 255, 255)), (5, 5))
        self.ground.render()
        self.overlay.render()
        speed = 3.0  

        
        if self.context.active_keys[pygame.K_RIGHT]:
            
            self.ground.camera.position.x += math.cos(self.ground.camera.rotation) * speed * self.context.dt * 60
            self.ground.camera.position.y += math.sin(self.ground.camera.rotation) * speed * self.context.dt * 60
        if self.context.active_keys[pygame.K_LEFT]:
          
            self.ground.camera.position.x -= math.cos(self.ground.camera.rotation) * speed * self.context.dt * 60
            self.ground.camera.position.y -= math.sin(self.ground.camera.rotation) * speed * self.context.dt * 60
        if self.context.active_keys[pygame.K_DOWN]:
            self.ground.camera.position.x -= math.sin(self.ground.camera.rotation) * speed * self.context.dt * 60
            self.ground.camera.position.y += math.cos(self.ground.camera.rotation) * speed * self.context.dt * 60
        if self.context.active_keys[pygame.K_UP]:
            self.ground.camera.position.x += math.sin(self.ground.camera.rotation) * speed * self.context.dt * 60
            self.ground.camera.position.y -= math.cos(self.ground.camera.rotation) * speed * self.context.dt * 60
        if self.context.active_keys[pygame.K_z]:
            self.ground.camera.zoom *= 1.03 ** (self.context.dt * 60)
        if self.context.active_keys[pygame.K_s]:
            self.ground.camera.zoom /= 1.03 ** (self.context.dt * 60)
        if self.context.active_keys[pygame.K_q]:
            self.ground.camera.rotation += self.context.dt 
        if self.context.active_keys[pygame.K_d]:
            self.ground.camera.rotation -= self.context.dt 


context = nodex.engine.Context((250, 240), 2, False) 
context.add_game_node(Test(context))
context.run()