#version 330
layout(location=0) in vec3 position;
layout(location=1) in vec4 color;

out vec4 f_color;

uniform mat4 mvp;
void main() {
    f_color = color;
    gl_Position = vec4(position, 1) * mvp;
}

// --SL--

#version 330
in vec4 f_color;

out vec4 outputColor;
void main() {
    outputColor = f_color;
}