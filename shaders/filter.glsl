uniform sampler2D texture0;

in vec2 uv;
out vec4 fragColor;

void main() {
    vec4 color = texture(texture0, uv);
    float luminance = dot(color.rgb, vec3(0.299, 0.587, 0.114));
    vec3 saturated = mix(vec3(luminance), color.rgb, 1.3);
    fragColor = vec4(saturated, color.a);
}