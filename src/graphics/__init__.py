from OpenGL.GL import shaders

import OpenGL
import OpenGL.GL as GL
import OpenGL.GLU as GLU
import OpenGL.arrays
import OpenGL.arrays.vbo
import pygame as pg
import numpy as np

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
class Batcher2D[T]:
    vertices: list[T]
    indices: np.ndarray[np.int32]
    program: shaders.ShaderProgram
    mvp_mat: np.matrix

    def __init__(self):
        self.vertices = np.ndarray((0, 2), dtype=np.float32)
        self.indices = np.ndarray((0), dtype=np.int32)
        winx, winy = pg.display.get_window_size()
        self.mvp_mat = create_ortho_projection(0, winx, 0, winy)
    
    def begin(self, program: Shader):
        self.program = program.get_compiled()

    def draw_rect(self, pos: pg.Vector2, size: pg.Vector2, color = pg.color.Color('white')):
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
        mvp_location = GL.glGetUniformLocation(self.program, 'mvp')
        GL.glUniformMatrix4fv(mvp_location, 1, GL.GL_FALSE, self.mvp_mat)
        
        vertex_buffer = OpenGL.arrays.vbo.VBO(self.vertices)
        index_buffer = OpenGL.arrays.vbo.VBO(self.indices, target = GL.GL_ELEMENT_ARRAY_BUFFER)

        vertex_buffer.bind()
        index_buffer.bind()
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 2, GL.GL_FLOAT, False, 0, None)

        GL.glDrawElements(GL.GL_TRIANGLES, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)

        self.vertices = np.ndarray((0, 2), dtype=np.float32)
        self.indices = np.ndarray((0), dtype=np.int32)

if __name__ == "__main__":
    pass
