from OpenGL.GL import shaders

import OpenGL
import OpenGL.GL as GL
import OpenGL.GLU as GLU
import OpenGL.arrays
import OpenGL.arrays.vbo
import pygame as pg
import numpy as np

import graphics
import graphics.vertices

VERTEX_DEFAULT = """
#version 330
layout(location=0) in vec4 position;
layout(location=1) in vec4 color;

out vec4 f_color;

uniform mat4 mvp;
void main() {
    f_color = color;
    gl_Position = position * mvp;
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
    "mat4": GL.GL_FLOAT_MAT4
}

class RichUniform:
    gl_type: int | float
    value: object
    def __init__(self, type, val = None):
        self.gl_type = type
        self.value = val

class Shader:
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


def clear(r: float, g: float, b: float, a: float = 1):
    GL.glClearColor(r, g, b, a)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

def create_ortho_projection(left: float, right: float, top: float, bottom: float):
    n = -1.0
    f = 1.0
    r_l = right - left
    t_b = top - bottom
    n_f = n - f
    rpl = right + left
    tpb = top + bottom
    npf = n + f
    scale = np.array([
        [2 / r_l, 0, 0, 0],
        [0, 2 / t_b, 0, 0],
        [0, 0, 2 / n_f, 0],
        [0, 0, 0, 1],
    ], dtype=np.float32)
    translation = np.array([
        [1, 0, 0, -rpl / 2],
        [0, 1, 0, -tpb / 2],
        [0, 0, 1, -npf / 2],
        [0, 0, 0, 1]
    ])
    p = scale @ translation
    return p

# For the sake of this project, everything will be assumed to be GL_TRIANGLES, to reduce the number of abstraction layers to the underlying OpenGL

# TODO: Move type parameter into shader and parse it at shader compile time.
class Batcher[T: graphics.vertices.AbstractVertex]:
    vertices: list[T]
    indices: list[int]
    program: Shader

    def __init__(self):
        self.vertices = []
        self.indices = []
    
    def begin(self, program: Shader):
        self.program = program

    def draw_indexed(self, vertices: list[T], indices: list[int]):
        indices = [index + len(self.vertices) for index in indices]
        self.vertices += vertices
        self.indices += indices

    def flush(self):
        self.program.use()
        
        vertices = np.array(self.vertices)
        indices = np.array(self.indices, dtype=np.int32)

        vertex_buffer = OpenGL.arrays.vbo.VBO(vertices)
        index_buffer = OpenGL.arrays.vbo.VBO(indices, target = GL.GL_ELEMENT_ARRAY_BUFFER)

        vertex_buffer.bind()
        index_buffer.bind()
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 2, GL.GL_FLOAT, False, 0, None)

        GL.glDrawElements(GL.GL_TRIANGLES, len(self.indices), GL.GL_UNSIGNED_INT, None)

        self.vertices = []
        self.indices = []

if __name__ == "__main__":
    pass
