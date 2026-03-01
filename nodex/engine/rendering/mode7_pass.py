from .shader_pass import ShaderPass
from .camera3D import Camera3D

from .pygame_pass import PygamePass
from .shader_pass import ShaderPass

import pygame
MODE7_FRAG = """
#version 330 core

in vec2 uv;
out vec4 fragColor;
uniform sampler2D tex;

uniform float camera_x;
uniform float camera_y;
uniform float camera_z;
uniform float camera_angle;
uniform float horizon_height;
void main() {
    float screenY = 1.0 - uv.y;

    if (screenY <= horizon_height) {
        fragColor = vec4(0.0, 0.0, 0.0, 0.0);  // ← transparent
        return;
    }

    float depth = screenY - horizon_height;
    if (depth < 0.002) {
        fragColor = vec4(0.0, 0.0, 0.0, 0.0);  // ← transparent
        return;
    }

    float z = min(1.0 / depth, 300.0);
    float scale = camera_z * camera_z / 100.0;

    float xi = (uv.x - 0.5) * z * scale + camera_x;
    float yi = z * scale + camera_y;

    float cosA = cos(camera_angle);
    float sinA = sin(camera_angle);

    vec2 pixel = vec2(
        cosA * (xi - camera_x) - sinA * (yi - camera_y) + camera_x,
        sinA * (xi - camera_x) + cosA * (yi - camera_y) + camera_y
    );

    if (pixel.x < 0.0 || pixel.x > 1.0 || pixel.y < 0.0 || pixel.y > 1.0) {
        fragColor = vec4(0.0, 0.0, 0.0, 0.0);  // ← transparent
        return;
    }

    fragColor = texture(tex, pixel);
}
"""

class Mode7Pass:
    def __init__(self, context, extra_data = None):
        self.context = context 
        self._set_pass(extra_data)
        self.camera = Camera3D()



    def _set_pass(self, extra_data):
        if "surface" in extra_data:
            self._pass = PygamePass(self.context, MODE7_FRAG)
            self.dynamic = True
            self._pass.set_tex(extra_data["slot"])
        else:
            self._pass = ShaderPass(self.context, MODE7_FRAG)
            self._pass.load_texture("tex", extra_data["texture"], extra_data["slot"]) 
            self.dynamic = False

    
    def set_uniforms(self):
        self._pass.set_uniform("camera_x", self.camera.position.x)
        self._pass.set_uniform("camera_y", self.camera.position.y)
        self._pass.set_uniform("camera_z", self.camera.position.z)    
        self._pass.set_uniform("camera_angle", self.camera.rotation)   
        self._pass.set_uniform("horizon_height", self.camera.horizon_height)

    def blit(self, surface, position):
        if self.dynamic:
            self._pass.blit(surface, position)

    def render(self):
        self.set_uniforms()
        self._pass.render()  # PygamePass.render() gère tex.write + surf.fill lui même
            