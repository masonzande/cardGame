#version 330 core
layout(location = 0) in vec3 position;
layout(location = 1) in vec2 f_tex_coord;

out vec2 tex_coord;

uniform mat4 mvp;
void main() {
    tex_coord = f_tex_coord;
    gl_Position = vec4(position, 1) * mvp;
}

// --SL--

#version 330

in vec2 tex_coord;

out vec4 outputColor;

uniform vec4 text_color;
uniform sampler2D font;

void main() {
    vec4 sample = vec4(1.0, 1.0, 1.0, texture(font, tex_coord).r);
    outputColor = sample * text_color;
}