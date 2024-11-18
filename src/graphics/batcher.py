import graphics
from graphics import target
import graphics.vertices as vertices
import graphics.shader as shader
import graphics.sprite as sprite

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
    

class SpriteBatch():
    vertices: list[graphics.vertices.VertexPosition3Texture2]
    indices: list[int]
    texture: sprite.Sprite
    def __init__(self, texture: sprite.Sprite):
        self.vertices = []
        self.indices = []
        self.texture = texture
        

class SpriteBatcher(Batcher[vertices.VertexPosition3Texture2]):
    batches: dict[int, SpriteBatch]

    def __init__(self):
        self.batches = {}
        super().__init__()

    def begin(self, program):
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        return super().begin(program)
    
    def draw_indexed(self, vertices, indices, batch_id):
        indices = [index + len(self.batches[batch_id].vertices) for index in indices]
        self.batches[batch_id].vertices += vertices
        self.batches[batch_id].indices += indices
    
    def draw(self, texture: sprite.Texture | target.RenderTarget, pos: pg.Vector2, size: pg.Vector2, depth: float):
        if isinstance(texture, target.RenderTarget):
            texture = texture.get_texture()
        
        try:
            self.batches[texture.texture_id]
        except KeyError:
            self.batches[texture.texture_id] = SpriteBatch(texture)

        INDICES = [0, 1, 2, 0, 2, 3]
        verts = [
            vertices.VertexPosition3Texture2(pg.Vector3(pos.x, pos.y, depth), pg.Vector2(0, 0)),
            vertices.VertexPosition3Texture2(pg.Vector3(pos.x + size.x, pos.y, depth), pg.Vector2(1, 0)),
            vertices.VertexPosition3Texture2(pg.Vector3(pos.x + size.x, pos.y + size.y, depth), pg.Vector2(1, 1)),
            vertices.VertexPosition3Texture2(pg.Vector3(pos.x, pos.y + size.y, depth), pg.Vector2(0, 1)),
        ]
        self.draw_indexed(verts, INDICES, texture.texture_id)

    def flush(self):
        self.program.use()
        
        for batch in self.batches.values():
            indices = np.array(batch.indices, dtype=np.uint32)
            index_buffer = OpenGL.arrays.vbo.VBO(indices, target = GL.GL_ELEMENT_ARRAY_BUFFER)
            index_buffer.bind()

            vertex_buffer = vertices.VertexArrayObject(batch.vertices)
            vertex_buffer.bind()

            batch.texture.bind()

            GL.glDrawElements(GL.GL_TRIANGLES, len(indices), GL.GL_UNSIGNED_INT, None)

            batch.vertices = []
            batch.indices = []
        
        self.batches = {}