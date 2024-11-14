import OpenGL
from OpenGL.arrays.vbo import VBO
import numpy as np
import pygame as pg
import OpenGL.GL as GL

class VertexAttribute:
    gl_type: int | float
    use_c: int
    def __init__(self, type, use_count):
        self.gl_type = type
        self.use_c = use_count

class AbstractVertex:
    def position(self) -> np.ndarray[np.float32]:
        raise NotImplementedError("Implement in super class.")
    def color(self) -> np.ndarray[np.float32]:
        raise NotImplementedError("Implement in super class.")
    
    def get_attributes() -> list[VertexAttribute]:
        raise NotImplementedError("Implement in super class.")

    # TODO: Add a system here for constructing a vertex array object to be loaded and used by the main batcher as needed. This should make the batcher type agnostic.
    def construct_vbos(vertices: list["AbstractVertex"]) -> tuple[list[VBO], int]:
        raise NotImplementedError("Implement in super class.")
    
class VertexPosition2Color4(AbstractVertex):
    pos: pg.Vector2
    col: pg.Color
    def __init__(self, pos, col):
        self.pos = pos
        self.col = col
    def position(self) -> np.ndarray[np.float32]:
        return np.array([self.pos.x, self.pos.y])
    def color(self) -> np.ndarray[np.float32]:
        return np.array([self.col.r, self.col.g, self.col.b, self.col.a])
    
    def get_attributes():
        return [
            VertexAttribute(GL.GL_FLOAT, 2),
            VertexAttribute(GL.GL_FLOAT, 4)
        ]

    def construct_vbos(vertices: list["VertexPosition2Color4"]):
        positions = np.array([vertex.position() for vertex in vertices])
        colors = np.array([vertex.color() for vertex in vertices])
        position_buffer = VBO(positions)
        color_buffer = VBO(colors)
        return [position_buffer, color_buffer], len(vertices)
    
class VertexArrayObject[T: AbstractVertex]:
    vbos: list[VBO]
    attrib: list[VertexAttribute]
    v_count: int
    def __init__(self, vertices: list[T]):
        self.vbos, self.v_count = T.construct_vbos(vertices)
        self.attrib = T.get_attributes()

    def bind(self):
        for i in range(0, len(self.vbos)):
            self.vbos[i].bind()
            GL.glEnableVertexAttribArray(i)
            # TODO: Instead of storing just VBOs, create a custom 'VertexAttribute' type which stores the following:
            #         - GL_TYPE
            #         - Element Count per Vertex
            # Have 1 array of VBOs and 1 array of VertexAttributes. VertexAttributes should be static, VBO is data dependent. 
            GL.glVertexAttribPointer(i, 2, GL.GL_FLOAT, False, 0, None)