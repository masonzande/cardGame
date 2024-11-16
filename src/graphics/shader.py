from OpenGL.GL import shaders
import OpenGL.GL as GL
import pygame as pg

from loader import ILoadable

VERTEX_DEFAULT = """
#version 330
layout(location=0) in vec2 position;
layout(location=1) in vec4 color;

out vec4 f_color;

uniform mat4 mvp;
void main() {
    f_color = color;
    gl_Position = vec4(position, 0, 1) * mvp;
}                                         
"""
FRAGMENT_DEFAULT = """
#version 330
in vec4 f_color;

out vec4 outputColor;
void main() {
    outputColor = f_color;
}
"""
# TODO: Finish this
STRING_TO_GL_TYPE = {
    "mat4": GL.GL_FLOAT_MAT4,
    'sampler2D': GL.GL_SAMPLER_2D
}

class RichUniform:
    gl_type: int | float
    value: object
    def __init__(self, type, val = None):
        self.gl_type = type
        self.value = val

class Shader(ILoadable):
    vertex_source: str
    fragment_source: str
    compiled_shader: shaders.ShaderProgram
    uniforms: dict[str, RichUniform]

    def __init__(self, vertex_source, fragment_source):
        self.vertex_source = vertex_source
        self.fragment_source = fragment_source
        self.uniforms = {}
        self.parse_shader_typings()

    def get_compiled(self):
        try:
            return self.compiled_shader
        except:
            vertex_shader = shaders.compileShader(self.vertex_source, GL.GL_VERTEX_SHADER)
            fragment_shader = shaders.compileShader(self.fragment_source, GL.GL_FRAGMENT_SHADER)
            self.compiled_shader = shaders.compileProgram(vertex_shader, fragment_shader)
            return self.compiled_shader
        
    def parse_shader_typings(self):
        v_lines = self.vertex_source.splitlines()
        for line in v_lines:
            if line.startswith("uniform"):
                 args = line.split(' ')
                 type = STRING_TO_GL_TYPE[args[1]]
                 name = args[2][0:-1]
                 self.uniforms[name] = RichUniform(type)
        f_lines = self.fragment_source.splitlines()
        for line in f_lines:
            if line.startswith("uniform"):
                 args = line.split(' ')
                 type = STRING_TO_GL_TYPE[args[1]]
                 name = args[2][0:-1]
                 self.uniforms[name] = RichUniform(type)

    def set_uniform(self, name: str, value):
        # TODO: Type checking
        self.uniforms[name].value = value

    def use(self):
        GL.glUseProgram(self.get_compiled())
        for uniform_name in self.uniforms.keys():
            location = GL.glGetUniformLocation(self.compiled_shader, uniform_name)
            type = self.uniforms[uniform_name].gl_type
            # TODO: Expand this to support more uniform types
            if type == GL.GL_FLOAT_MAT4:
                GL.glUniformMatrix4fv(location, 1, GL.GL_FALSE, self.uniforms[uniform_name].value)

    def load_from_file(path) -> "Shader":
        try:
            with open(path, mode='r') as file:
                text = file.read().split("// --SL--")
                return Shader(text[0], text[1])
        except Exception() as e:
            raise e
            
        
        