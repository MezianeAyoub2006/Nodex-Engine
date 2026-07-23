#version 330

uniform vec2 u_position;      
uniform float u_rotation;     
uniform vec2 u_scale;         
uniform vec2 u_flip;          
uniform vec2 u_resolution;

in vec2 in_pos;   
in vec2 in_uv;

out vec2 uv;

vec2 pixels_to_ndc(vec2 px, vec2 res) {
    vec2 zero_to_one = px / res;
    return zero_to_one * 2.0 - 1.0;
}

void main() {
    vec2 pos = in_pos * u_flip;
    pos *= u_scale;

    float c = cos(u_rotation);
    float s = sin(u_rotation);
    pos = vec2(pos.x * c - pos.y * s, pos.x * s + pos.y * c);

    vec2 world_pos = pos + u_position;

    gl_Position = vec4(pixels_to_ndc(world_pos, u_resolution), 0.0, 1.0);
    uv = in_uv;
}