import graphics
from graphics import target
import graphics.vertices as vertices
import graphics.shader as shader
import graphics.sprite as sprite

import type_convert

import numpy as np
import pygame as pg

import OpenGL
import OpenGL.GL as GL

class Batcher[T: vertices.AbstractVertex]:
    started: bool

    vertices: list[T]
    indices: list[int]
    program: shader.Shader

    def __init__(self):
        self.started = False
        self.vertices = []
        self.indices = []
    
    def begin(self, program: shader.Shader):
        if self.started:
            return
        self.program = program

    def draw_indexed(self, vertices: list[T], indices: list[int]):
        if not self.started:
            raise UnboundLocalError
        indices = [index + len(self.vertices) for index in indices]
        self.vertices += vertices
        self.indices += indices

    def flush(self):
        if not self.started:
            return
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
    texture: sprite.Texture
    def __init__(self, texture: sprite.Texture):
        self.vertices = []
        self.indices = []
        self.texture = texture

class SpriteBatcher(Batcher[vertices.VertexPosition3Texture2]):
    _font_program: shader.Shader
    batches: dict[int, SpriteBatch]

    temp_rts: list[target.RenderTarget]

    def __init__(self):
        self.batches = {}
        self.temp_rts = []
        super().__init__()

    def begin(self, program, font_program: shader.Shader = None):
        self._font_program = font_program
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

    def draw_string(self, font: sprite.SpriteFont, message: str, pos: pg.Vector2, depth: float = 0, color: pg.Color = pg.Color(255, 255, 255, 255)):
        if self._font_program == None:
            print("BATCH ERR: Font Program was not initialized. Printing message to console.")
            print(message)
            return
        
        GL.glActiveTexture(GL.GL_TEXTURE0)

        str_dim = font.string_dims(message)

        self._font_program.set_uniform("text_color", type_convert.pg_color_to_numpy_array(color))
        self._font_program.set_uniform("mvp", graphics.create_ortho_projection(0, str_dim[0], str_dim[1], 0))
        self._font_program.use()

        rt = target.RenderTarget(str_dim[0], str_dim[1])

        reset = graphics.active_target
        graphics.bind_buffer(rt)
        graphics.clear(0, 0, 0, 0)

        x = 0
        y = str_dim[2]
        for c in message:
            char: sprite._SpriteChar = font.chars[ord(c)]
            xpos = x + char.bearing_x
            ypos = y - (char.height - char.bearing_y)

            width = char.width
            height = char.height

            verts = [
                vertices.VertexPosition3Texture2(pg.Vector3(xpos, ypos, 0), pg.Vector2(0, 1)),
                vertices.VertexPosition3Texture2(pg.Vector3(xpos + width, ypos, 0), pg.Vector2(1, 1)),
                vertices.VertexPosition3Texture2(pg.Vector3(xpos + width, ypos - height, 0), pg.Vector2(1, 0)),
                vertices.VertexPosition3Texture2(pg.Vector3(xpos, ypos - height, 0), pg.Vector2(0, 0)),
            ]

            indices = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32)

            vertex_buf = vertices.VertexArrayObject(verts)
            vertex_buf.bind()
            index_buf = OpenGL.arrays.vbo.VBO(indices, target = GL.GL_ELEMENT_ARRAY_BUFFER)
            index_buf.bind()

            GL.glBindTexture(GL.GL_TEXTURE_2D, char._gl_id)
            
            GL.glDrawElements(GL.GL_TRIANGLES, len(indices), GL.GL_UNSIGNED_INT, None)
            x += (char.advance >> 6)

        graphics.bind_buffer(reset)
        self.draw(rt, pos, pg.Vector2(str_dim[0], str_dim[1]), depth)
        self.temp_rts.append(rt)

    def flush(self):
        self.program.use()
        
        for batch in self.batches.values():
            indices = np.array(batch.indices, dtype=np.uint32)
            index_buffer = OpenGL.arrays.vbo.VBO(indices, target = GL.GL_ELEMENT_ARRAY_BUFFER)
            index_buffer.bind()

            vertex_buffer = vertices.VertexArrayObject(batch.vertices)
            vertex_buffer.bind()

            batch.texture.bind(min_filter=GL.LINEAR)

            GL.glDrawElements(GL.GL_TRIANGLES, len(indices), GL.GL_UNSIGNED_INT, None)

            batch.vertices = []
            batch.indices = []
        
        self.batches = {}

        for rt in self.temp_rts:
            rt.unload()
        self.temp_rts = []