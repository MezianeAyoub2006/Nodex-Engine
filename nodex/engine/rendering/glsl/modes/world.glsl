#version 330 core
in vec2 in_pos;
in vec2 in_uv;
out vec2 uv;

uniform float rotation;
uniform float zoom;

void main() {
    vec2 centered = in_uv - 0.5;

    float c = cos(rotation);
    float s = sin(rotation);

    vec2 rotated = vec2(
        centered.x * c - centered.y * s,
        centered.x * s + centered.y * c
    );

    uv = (rotated / zoom) + 0.5;

    gl_Position = vec4(in_pos, 0.0, 1.0);
}