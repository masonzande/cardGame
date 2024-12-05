/*
 * Files in this folder are using a custom file format. The main code sections are written in GLSL.
 * Generally, the layout of a '.sl' file looks like this:
 *      Vertex Shader
 *      // Delimeter (--SL--)
 *      Fragment Shader 
 */

#version 330
layout(location=0) in vec2 position;
layout(location=1) in vec4 color;

out vec4 f_color;

uniform mat4 mvp;
void main() {
    f_color = color;
    gl_Position = vec4(position, 0, 1) * mvp;
}

// --SL--

#version 330
in vec4 f_color;

out vec4 outputColor;
void main() {
    outputColor = f_color;
}