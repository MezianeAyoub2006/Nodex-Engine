import nodex.engine
import pygame

SHADER = """
#version 330
in vec2 uv;
out vec4 fragColor;
uniform sampler2D tex;
void static() {
    vec4 color = texture(tex, uv);
    fragColor = vec4(color.r + 1.0, color.g, color.b, color.a);
}
"""

class Test(nodex.engine.GameNode):
    def __init__(self, context:"nodex.engine.Context"):
        super().__init__(context)
        self.context.assets.load_image("ground", "assets/ground.png")
        self.context.assets.load_image("ground2", "assets/ground2.png")
        self.context.assets.load_image("infinite", "assets/ground-infinite.png")
        self.context.renderer.add_viewport("static", nodex.ViewportType.MODE7, 0, extra_data={"texture" : "assets/ground2.png", "slot" : 1})
        self.context.renderer.add_viewport("dynamic", nodex.ViewportType.MODE7, 1, extra_data={"surface" : None, "slot" : 2})
        self.context.renderer.add_viewport("overlay", nodex.ViewportType.PYGAME, 2)
       
    def update(self):   
        self.context.renderer.draw("dynamic", "infinite")
        
        self.context.renderer.draw("overlay", pygame.Rect(0, 0, 50, 50), color = nodex.Color.RED)
    
        

        if self.context.input.active_keys[pygame.K_UP]:
            self.context.renderer.camera3D("static").position.z += 2 * self.context.dt
            self.context.renderer.camera3D("dynamic").position.z += 2 * self.context.dt
        
        if self.context.input.active_keys[pygame.K_DOWN]:
            self.context.renderer.camera3D("static").position.z -= 2 * self.context.dt
            self.context.renderer.camera3D("dynamic").position.z -= 2 * self.context.dt
        
        if self.context.input.active_keys[pygame.K_d]:
            self.context.renderer.camera3D("static").position.x += 0.15 * self.context.dt
            self.context.renderer.camera3D("dynamic").position.x += 0.15 * self.context.dt
        
        if self.context.input.active_keys[pygame.K_q]:
            self.context.renderer.camera3D("static").position.x -= 0.15 * self.context.dt
            self.context.renderer.camera3D("dynamic").position.x -= 0.15 * self.context.dt

        if self.context.input.active_keys[pygame.K_z]:
            self.context.renderer.camera3D("static").position.y += 0.15 * self.context.dt
            self.context.renderer.camera3D("dynamic").position.y += 0.15 * self.context.dt
        
        if self.context.input.active_keys[pygame.K_s]:
            self.context.renderer.camera3D("static").position.y -= 0.15 * self.context.dt
            self.context.renderer.camera3D("dynamic").position.y -= 0.15 * self.context.dt

        if self.context.input.active_keys[pygame.K_LEFT]:
            self.context.renderer.camera3D("static").rotation += 1 * self.context.dt
            self.context.renderer.camera3D("dynamic").rotation += 1 * self.context.dt
        
        if self.context.input.active_keys[pygame.K_RIGHT]:
            self.context.renderer.camera3D("static").rotation -= 1 * self.context.dt
            self.context.renderer.camera3D("dynamic").rotation -= 1 * self.context.dt




context = nodex.engine.Context((250, 240), 2, False) 
context.scenes["main"].add_game_node(Test(context))
context.run()

"""
Probleme du mode 7 dynamique resolu
un mode 7 qui a une texture fixe (pour le fond)
un mode 7 avec surface pygame dynamique mais qui
est noir en dehors de la taille de l'ecran
on superpose les deux (transparent au lieu de noir
pour la surface dynamique, a voir comment gérer
dans GLSL) et ça nous fait une zone dynamique, de la taille
d'un ecran, une zone de fond, faut juste ajuster la positon
des deux pour pas avoir de souci.
"""