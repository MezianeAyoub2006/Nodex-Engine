#version 330 core
in vec2 uv;
out vec4 fragColor;
uniform sampler2D tex;
uniform float strength;

void main() {
    vec2 size = textureSize(tex, 0);
    vec2 pixelated = floor(uv * size / strength) * strength / size;
    fragColor = texture(tex, pixelated);
}