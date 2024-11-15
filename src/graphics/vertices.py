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
    
    @staticmethod
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
        return np.array([self.pos.x, self.pos.y], dtype=np.float32)
    def color(self) -> np.ndarray[np.float32]:
        return np.array([self.col.r, self.col.g, self.col.b, self.col.a], dtype=np.float32) / 255
    
    @staticmethod
    def get_attributes():
        return [
            VertexAttribute(GL.GL_FLOAT, 2),
            VertexAttribute(GL.GL_FLOAT, 4)
        ]

    def construct_vbos(vertices: list["VertexPosition2Color4"]):
        positions = np.array([vertex.position() for vertex in vertices], dtype=np.float32)
        colors = np.array([vertex.color() for vertex in vertices], dtype=np.float32)
        position_buffer = VBO(positions)
        color_buffer = VBO(colors)
        return [position_buffer, color_buffer], len(vertices)
    
class VertexPosition3Color4(AbstractVertex):
    pos: pg.Vector3
    col: pg.Color
    def __init__(self, pos, col):
        self.pos = pos
        self.col = col
    def position(self) -> np.ndarray[np.float32]:
        return np.array([self.pos.x, self.pos.y, self.pos.z], dtype=np.float32)
    def color(self) -> np.ndarray[np.float32]:
        return np.array([self.col.r, self.col.g, self.col.b, self.col.a], dtype=np.float32) / 255
    
    @staticmethod
    def get_attributes():
        return [
            VertexAttribute(GL.GL_FLOAT, 3),
            VertexAttribute(GL.GL_FLOAT, 4)
        ]

    def construct_vbos(vertices: list["VertexPosition3Color4"]):
        positions = np.array([vertex.position() for vertex in vertices], dtype=np.float32)
        colors = np.array([vertex.color() for vertex in vertices], dtype=np.float32)
        position_buffer = VBO(positions)
        color_buffer = VBO(colors)
        return [position_buffer, color_buffer], len(vertices)
    
class VertexPosition3Texture2(AbstractVertex):
    pos: pg.Vector3
    tex: pg.Vector2
    def __init__(self, pos, tex):
        self.pos = pos
        self.tex = tex
    def position(self) -> np.ndarray[np.float32]:
        return np.array([self.pos.x, self.pos.y, self.pos.z], dtype=np.float32)
    def texture(self) -> np.ndarray[np.float32]:
        return np.array([self.tex.x, self.tex.y], dtype=np.float32)
    
    @staticmethod
    def get_attributes():
        return [
            VertexAttribute(GL.GL_FLOAT, 3),
            VertexAttribute(GL.GL_FLOAT, 2)
        ]

    def construct_vbos(vertices: list["VertexPosition3Texture2"]):
        positions = np.array([vertex.position() for vertex in vertices], dtype=np.float32)
        colors = np.array([vertex.texture() for vertex in vertices], dtype=np.float32)
        position_buffer = VBO(positions)
        color_buffer = VBO(colors)
        return [position_buffer, color_buffer], len(vertices)
    
class VertexArrayObject:
    vbos: list[VBO]
    attrib: list[VertexAttribute]
    v_count: int
    def __init__[T: AbstractVertex](self, vertices: list[T]):
        if len(vertices) == 0:
            raise Exception("Tried to create a VertexArrayObject with no elements.")
        vertex_type = vertices[0].__class__
        self.vbos, self.v_count = vertex_type.construct_vbos(vertices)
        self.attrib = vertex_type.get_attributes()

    def bind(self):
        for i in range(0, len(self.vbos)):
            self.vbos[i].bind()
            GL.glVertexAttribPointer(i, self.attrib[i].use_c, self.attrib[i].gl_type, GL.GL_FALSE, 0, None)
            GL.glEnableVertexAttribArray(i)