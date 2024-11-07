from OpenGL.GL import shaders

import OpenGL
import OpenGL.GL as GL
import OpenGL.arrays
import OpenGL.arrays.vbo
import pygame as pg
import numpy as np

VERTEX_DEFAULT = """
#version 330
layout(location=0) in vec4 position;
void main() {
    gl_Position = position;
}                                         
"""
FRAGMENT_DEFAULT = """
#version 330
out vec4 outputColor;
void main() {
    outputColor = vec4(0.0f, 1.0f, 0.0f, 1.0f);
}
"""

class Shader:
    vertex_source: str
    fragment_source: str
    compiled_shader: shaders.ShaderProgram
    def __init__(self, vertex_source, fragment_source):
        self.vertex_source = vertex_source
        self.fragment_source = fragment_source

    def get_compiled(self):
        try:
            return self.compiled_shader
        except:
            vertex_shader = shaders.compileShader(self.vertex_source, GL.GL_VERTEX_SHADER)
            fragment_shader = shaders.compileShader(self.fragment_source, GL.GL_FRAGMENT_SHADER)
            self.compiled_shader = shaders.compileProgram(vertex_shader, fragment_shader)
            return self.compiled_shader

def clear(r: float, g: float, b: float, a: float = 1):
    GL.glClearColor(r, g, b, a)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

# For the sake of this project, everything will be assumed to be GL_TRIANGLES, to reduce the number of abstraction layers to the underlying OpenGL
class Batcher2D:
    vertices: np.ndarray[np.float32]
    indices: np.ndarray[np.int32]
    program: shaders.ShaderProgram
    def __init__(self):
        self.vertices = np.ndarray((0, 2), dtype=np.float32)
        self.indices = np.ndarray((0), dtype=np.int32)
        

    def begin(self, program: Shader):
        self.program = program.get_compiled()

    def draw_rect(self, pos: pg.Vector2, size: pg.Vector2):
        posx, posy = pos        # Deconstruct Vectors
        sizx, sizy = size
        vertices = np.array([   # Convert vectors to a strictly typed 2d array
            [posx, posy],
            [posx + sizx, posy],
            [posx + sizx, posy + sizy],
            [posx, posy + sizy],
        ], dtype=np.float32)
        indices = np.array([0, 1, 2, 0, 2, 3], dtype=np.int32) # Strictly type the index buffer
        indices += self.vertices.shape[0]
        self.vertices = np.concatenate((self.vertices, vertices), axis=0, dtype=np.float32)
        self.indices = np.concatenate((self.indices, indices), axis=0, dtype=np.int32)

    def flush(self):
        GL.glUseProgram(self.program)

        vertex_buffer = OpenGL.arrays.vbo.VBO(self.vertices)
        index_buffer = OpenGL.arrays.vbo.VBO(self.indices, target = GL.GL_ELEMENT_ARRAY_BUFFER)

        vertex_buffer.bind()
        index_buffer.bind()
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 2, GL.GL_FLOAT, False, 0, None)

        GL.glDrawElements(GL.GL_TRIANGLES, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)

        self.vertices = np.ndarray((0, 2), dtype=np.float32)
        self.indices = np.ndarray((0), dtype=np.int32)