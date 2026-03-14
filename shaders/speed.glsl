uniform sampler2D tex;
uniform float amplitude;

in vec2 uv;
out vec4 fragColor;

void main() {
    vec2 p = uv * 2.0 - 1.0;
    float r = dot(p, p);
    vec2 distorted = p * (1.0 + amplitude * r + amplitude * 0.3 * r * r);
    vec2 final_uv = distorted * 0.5 + 0.5;

    if (final_uv.x < 0.0 || final_uv.x > 1.0 || final_uv.y < 0.0 || final_uv.y > 1.0)
        fragColor = vec4(0.0, 0.0, 0.0, 1.0);
    else
        fragColor = texture(tex, final_uv);
}