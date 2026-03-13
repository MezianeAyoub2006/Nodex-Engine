#version 330 core
in vec2 uv;
out vec4 fragColor;
uniform sampler2D tex;
uniform float strength;

void main() {
    vec2 texel = 1.0 / textureSize(tex, 0);
    vec4 color = vec4(0.0);
    
    for (int x = -2; x <= 2; x++) {
        for (int y = -2; y <= 2; y++) {
            color += texture(tex, uv + vec2(x, y) * texel * strength);
        }
    }
    
    fragColor = color / 25.0;
}