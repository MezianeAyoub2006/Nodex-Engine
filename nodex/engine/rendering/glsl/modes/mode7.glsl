#version 330 core

in vec2 uv;
out vec4 fragColor;

uniform sampler2D tex;
uniform sampler2D infinite;
uniform sampler2D extra;

uniform float camera_x;
uniform float camera_y;
uniform float camera_z;
uniform float camera_angle;
uniform float horizon_height;

uniform vec2 tex_scale;
uniform vec2 tex_offset;

uniform float time;

const float REFLECTION_SPEED = 0.5;
const float FOG_START = 30.0;
const float FOG_END = 150.0;
const float Z_MAX = 300.0;
const float DEPTH_MIN = 0.002;

bool is_water(vec4 extra_color) {
    return extra_color.b > 0.5 && extra_color.g < 0.3 && extra_color.r < 0.3;
}

float value_noise(vec2 p, vec2 seed) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    float a = fract(sin(dot(i,             seed)) * 43758.5);
    float b = fract(sin(dot(i + vec2(1,0), seed)) * 43758.5);
    float c = fract(sin(dot(i + vec2(0,1), seed)) * 43758.5);
    float d = fract(sin(dot(i + vec2(1,1), seed)) * 43758.5);
    vec2 u = f * f * f * (f * (f * 6.0 - 15.0) + 10.0);
    return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}

float water_specular(vec2 pixel) {
    mat2 rot = mat2(0.8, -0.6, 0.6, 0.8);
    vec2 warp = vec2(
        sin(pixel.y * 40.0 + time * REFLECTION_SPEED),
        cos(pixel.x * 40.0 - time * REFLECTION_SPEED)
    ) * 0.02;
    vec2 p1 = rot * ((pixel + warp) * 200.0) + vec2(time * 2.0, time * 1.3) * REFLECTION_SPEED;
    vec2 p2 = rot * ((pixel - warp) * 150.0) + vec2(-time * 1.7, time * 2.4) * REFLECTION_SPEED;
    float noise = (value_noise(p1, vec2(127.1, 311.7)) + value_noise(p2, vec2(269.5, 183.3))) * 0.5;
    return pow(noise, 3.0);
}

vec4 apply_fog(vec4 color, float z) {
    float fog_factor = clamp((z - FOG_START) / (FOG_END - FOG_START), 0.0, 1.0);
    return mix(color, vec4(0.0), fog_factor);
}

vec2 mode7_project(float z, float scale) {
    float xi = (uv.x - 0.5) * z * scale + camera_x;
    float yi = z * scale + camera_y;

    float cosA = cos(camera_angle);
    float sinA = sin(camera_angle);

    return vec2(
        cosA * (xi - camera_x) - sinA * (yi - camera_y) + camera_x,
        sinA * (xi - camera_x) + cosA * (yi - camera_y) + camera_y
    );
}

void main() {
    float screenY   = 1.0 - uv.y;
    bool underground = camera_z < 0.0;

    float depth;
    if (!underground) {
        if (screenY <= horizon_height) {fragColor = vec4(0.0); return;}
        depth = screenY - horizon_height;
    } else {
        if (screenY >= horizon_height) {fragColor = vec4(0.0); return;}
        depth = horizon_height - screenY;
    }

    if (depth< DEPTH_MIN) { fragColor = vec4(0.0); return; }

    float z = min(1.0 / depth, Z_MAX);
    float scale = max(0.001, abs(camera_z));
    vec2 pixel = mode7_project(z, scale);

    if (pixel.x < 0.0 || pixel.x > 1.0 || pixel.y < 0.0 || pixel.y > 1.0) {
        fragColor = texture(infinite, fract(pixel));
        fragColor = mix(fragColor, vec4(1.0), water_specular(fract(pixel)));
        return;
    }

    vec2 dyn_uv = vec2(
        (pixel.x - tex_offset.x) * tex_scale.x,
        (pixel.y - tex_offset.y) * tex_scale.y
    );

    if (dyn_uv.x < 0.0 || dyn_uv.x > 1.0 || dyn_uv.y < 0.0 || dyn_uv.y > 1.0) {
        fragColor = vec4(0.0);
        return;
    }

    fragColor = texture(tex, dyn_uv);

    if (is_water(texture(extra, pixel))) {
        fragColor = mix(fragColor, vec4(1.0), water_specular(pixel));
    }

    fragColor = apply_fog(fragColor, z);
}