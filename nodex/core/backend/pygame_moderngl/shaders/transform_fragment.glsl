#version 330

uniform sampler2D tex;
uniform vec4 u_tint;

in vec2 uv;
out vec4 FragColor;

void main() {
    FragColor = texture(tex, uv) * u_tint;
}