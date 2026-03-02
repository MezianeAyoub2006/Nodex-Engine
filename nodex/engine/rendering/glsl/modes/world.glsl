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