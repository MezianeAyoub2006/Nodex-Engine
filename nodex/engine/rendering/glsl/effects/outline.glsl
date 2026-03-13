#version 330
in vec2 uv;
out vec4 fragColor;
uniform vec3 color;
uniform sampler2D tex;

void main() {
    vec4 c = texture(tex, uv);
    float d = 0.005;

    float a = 0.0;
    a = max(a, texture(tex, uv + vec2( d,  0)).a);
    a = max(a, texture(tex, uv + vec2(-d,  0)).a);
    a = max(a, texture(tex, uv + vec2( 0,  d)).a);
    a = max(a, texture(tex, uv + vec2( 0, -d)).a);

    if (c.a < 0.5 && a > 0.5)
        fragColor = vec4(color, 1.0);
    else
        fragColor = c;
}