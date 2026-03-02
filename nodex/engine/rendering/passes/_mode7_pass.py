from .shader_pass import ShaderPass
from ..cameras.camera3D import Camera3D

from .pygame_pass import PygamePass
from .shader_pass import ShaderPass


class Mode7Pass:
    def __init__(self, context, extra_data = None):
        self.context = context 
        self._set_pass(extra_data)
        self.camera = Camera3D()
        self.zone_position = (0, 0)
        self.zone_size = (1, 1)

    def _set_pass(self, extra_data):
        if "surface" in extra_data:
            self._pass = PygamePass(self.context, self.context.shaders.get("_mode7"))
            self.dynamic = True
        else:
            self._pass = ShaderPass(self.context, self.context.shaders.get("_mode7"))
            self._pass.load_texture("tex", extra_data["texture"]) 
            self.dynamic = False

    
    def set_uniforms(self):
        self._pass.set_uniform("camera_x", self.camera.position.x)
        self._pass.set_uniform("camera_y", self.camera.position.y)
        self._pass.set_uniform("camera_z", self.camera.position.z)    
        self._pass.set_uniform("camera_angle", self.camera.rotation)   
        self._pass.set_uniform("horizon_height", self.camera.horizon_height)
        self._pass.set_uniform("zone_position", self.zone_position) 
        self._pass.set_uniform("zone_size", self.zone_size)

    def blit(self, surface, position):
        if self.dynamic:
            self._pass.blit(surface, position)

    def render(self):
        self.set_uniforms()
        self._pass.render()  
            