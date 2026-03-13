#version 330 core

in vec2 uv;
out vec4 fragColor;
uniform sampler2D tex;
uniform float time;
uniform float amplitude;

void main() {
    float frequency = 48.0;
    float speed     = 4.0;

    float offset = amplitude * sin(uv.y * frequency + time * speed);

    vec2 warped_uv = vec2(uv.x + offset, uv.y);

    fragColor = texture(tex, warped_uv);
}