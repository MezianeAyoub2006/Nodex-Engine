#version 330 core

in vec2 uv;
out vec4 fragColor;
uniform sampler2D tex;

uniform float camera_x;
uniform float camera_y;
uniform float camera_z;
uniform float camera_angle;
uniform float horizon_height;

void main() {
    float screenY = 1.0 - uv.y;
    
    bool underground = camera_z < 0.0;
    
    float depth;
    if (!underground) {
        if (screenY <= horizon_height) {
            fragColor = vec4(0.0, 0.0, 0.0, 0.0);
            return;
        }
        depth = screenY - horizon_height;
    } else {
        if (screenY >= horizon_height) {
            fragColor = vec4(0.0, 0.0, 0.0, 0.0);
            return;
        }
        depth = horizon_height - screenY;
    }

    if (depth < 0.002) {
        fragColor = vec4(0.0, 0.0, 0.0, 0.0);
        return;
    }

    float z = min(1.0 / depth, 300.0);
    float scale = abs(camera_z) * abs(camera_z) / 100.0;

    float xi = (uv.x - 0.5) * z * scale + camera_x;
    float yi = z * scale + camera_y;

    float cosA = cos(camera_angle);
    float sinA = sin(camera_angle);

    vec2 pixel = vec2(
        cosA * (xi - camera_x) - sinA * (yi - camera_y) + camera_x,
        sinA * (xi - camera_x) + cosA * (yi - camera_y) + camera_y
    );
    
    /*
    if (pixel.x < 0.0 || pixel.x > 1.0 || pixel.y < 0.0 || pixel.y > 1.0) {
        fragColor = vec4(0.0, 0.0, 0.0, 0.0);
        return;
    }
    */

    fragColor = texture(tex, pixel);
}