import nodex

from .world_pass import WorldPass
from .shader_pass import ShaderPass
from .pygame_pass import PygamePass

class Mode7Pass:
    def __init__(self, context : "nodex.Context", extra_data):
        self.context = context
        self.camera = nodex.Camera3D()
        self.static_pass = ShaderPass(self.context, self.context.shaders.get("_mode7")) 
        self.static_pass.load_texture(extra_data["texture_name"], extra_data["texture"])
        self.dynamic_pass = PygamePass(self.context, self.context.shaders.get("_mode7")) 
 
        self.camera.position.z = 3
        self.camera.position.x = 0.5
        self.camera.position.y = -0.3
        #self.dynamic_pass.camera.zoom = 0.2

    def draw(self, surface, position):
        self.dynamic_pass.blit(surface, position)
    
    def set_uniforms(self):
        for _pass in (self.static_pass, self.dynamic_pass):
            _pass.set_uniform("camera_x", self.camera.position.x)
            _pass.set_uniform("camera_y", self.camera.position.y)
            _pass.set_uniform("camera_z", self.camera.position.z)    
            _pass.set_uniform("camera_angle", self.camera.rotation)   
            _pass.set_uniform("horizon_height", self.camera.horizon_height)
    
    def render(self):
        self.set_uniforms()
        self.static_pass.set_viewport(0, 0, *self.context.window.internal_size)

        self.static_pass.render()
        self.dynamic_pass.render()
        