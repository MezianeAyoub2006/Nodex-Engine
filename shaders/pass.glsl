#version 330

uniform sampler2D tex;
uniform float t;

in vec2 uv;
out vec4 FragColor;

void main() {
    FragColor = texture(tex, vec2(uv.x + sin(t) * sin(uv.y) * 0.1, uv.y));
    FragColor.r *= 1.5;
}