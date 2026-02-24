from .pygame_layer import PygameLayer
from .camera import Camera

WORLD_VERTEX = """ 
#version 330
in vec2 in_pos;
in vec2 in_uv;
out vec2 uv;

uniform float rotation;
uniform float zoom; 

void main() {
    uv = in_uv;

    float c = cos(rotation);
    float s = sin(rotation);

    vec2 pos = vec2(
        in_pos.x * c - in_pos.y * s,
        in_pos.x * s + in_pos.y * c
    );

    gl_Position = vec4(pos * zoom, 0.0, 1.0);
}
"""

class WorldLayer(PygameLayer):
    def __init__(self, context, frag_prog=None): 
        self.camera = Camera()
        super().__init__(context, frag_prog, WORLD_VERTEX)
    
    def draw(self, surf, position):
        self.blit(surf, (position[0] - self.camera.position.x, position[1] - self.camera.position.y))
    
    def render(self):
        self.set_uniform("rotation", self.camera.rotation)
        self.set_uniform("zoom", self.camera.zoom)
        super().render()