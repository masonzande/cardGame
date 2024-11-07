import OpenGL
import OpenGL.GL
import OpenGL.arrays
import OpenGL.arrays.vbo
import pygame as pg
import numpy as np
from OpenGL.GL import glClearColor, glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT

def clear(r: float, g: float, b: float, a: float = 1):
    glClearColor(r, g, b, a)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


# For the sake of this project, everything will be assumed to be GL_TRIANGLES, to reduce the number of abstraction layers to the 
# underlying OpenGL
class Batcher2D:
    vertices: np.ndarray[np.float32]
    indices: np.ndarray[np.int32]
    def __init__(self):
        self.vertices = np.ndarray((0, 2), dtype=np.float32)
        self.indices = np.ndarray((0), dtype=np.int32)

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
        self.vertices = np.concatenate((self.vertices, vertices), axis=0)
        self.indices = np.concatenate((self.indices, indices), axis=0)

    def flush(self):
        vertex_buffer = OpenGL.arrays.vbo.VBO(self.vertices)
        index_buffer = OpenGL.arrays.vbo.VBO(self.indices, target=OpenGL.GL.GL_ELEMENT_ARRAY_BUFFER)
        
        print(self.vertices)

        vertex_buffer.bind()
        index_buffer.bind()
        OpenGL.GL.glEnableVertexAttribArray(0)
        OpenGL.GL.glVertexAttribPointer(0, 2, OpenGL.GL.GL_FLOAT, False, 0, None)

        OpenGL.GL.glDrawElements(OpenGL.GL.GL_TRIANGLES, self.vertices.shape[0], OpenGL.GL.GL_UNSIGNED_INT, None)

        self.vertices = np.ndarray((0, 2), dtype=np.float32)
        self.indices = np.ndarray((0), dtype=np.int32)