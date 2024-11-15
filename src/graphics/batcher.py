import graphics.vertices as vertices
import graphics.shader as shader
import numpy as np
import pygame as pg

import OpenGL
import OpenGL.GL as GL

class Batcher[T: vertices.AbstractVertex]:
    vertices: list[T]
    indices: list[int]
    program: shader.Shader

    def __init__(self):
        self.vertices = []
        self.indices = []
    
    def begin(self, program: shader.Shader):
        self.program = program

    def draw_indexed(self, vertices: list[T], indices: list[int]):
        indices = [index + len(self.vertices) for index in indices]
        self.vertices += vertices
        self.indices += indices

    def flush(self):
        self.program.use()
        
        indices = np.array(self.indices, dtype=np.uint32)
        index_buffer = OpenGL.arrays.vbo.VBO(indices, target = GL.GL_ELEMENT_ARRAY_BUFFER)
        index_buffer.bind()

        vertex_buffer = vertices.VertexArrayObject(self.vertices)
        vertex_buffer.bind()

        GL.glDrawElements(GL.GL_TRIANGLES, len(indices), GL.GL_UNSIGNED_INT, None)

        self.vertices = []
        self.indices = []

class ShapeBatcher(Batcher[vertices.VertexPosition3Color4]):
    def __init__(self):
        super().__init__()

    def begin(self, program):
        return super().begin(program)
    
    def draw_indexed(self, vertices, indices):
        return super().draw_indexed(vertices, indices)
    
    def draw_rect(self, pos: pg.Vector2, size: pg.Vector2, depth: float, color: pg.Color):
        INDICES = [0, 1, 2, 0, 2, 3]
        verts = [
            vertices.VertexPosition3Color4(pg.Vector3(pos.x, pos.y, depth), color),
            vertices.VertexPosition3Color4(pg.Vector3(pos.x + size.x, pos.y, depth), color),
            vertices.VertexPosition3Color4(pg.Vector3(pos.x + size.x, pos.y + size.y, depth), color),
            vertices.VertexPosition3Color4(pg.Vector3(pos.x, pos.y + size.y, depth), color),
        ]
        self.draw_indexed(verts, INDICES)

    def flush(self):
        return super().flush()
    