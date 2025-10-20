#version 460

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

layout(location = 0) in vec3 a_pos;

out vec3 pos;

void main(){
    pos = a_pos;
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(a_pos, 1.0);
}