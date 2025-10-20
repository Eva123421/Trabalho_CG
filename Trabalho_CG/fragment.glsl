#version 460

uniform vec3 color;

in vec3 pos;
out vec4 fragColor;

void main(){
    fragColor = vec4(color, 1.0);
}