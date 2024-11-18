from typing import Literal
import pygame as pg
import OpenGL.GL as GL

from loader import ILoadable

import freetype as FT

_pg_im_formats = Literal[
    "P", "RGB", "RGBX", "RGBA", "ARGB", "BGRA", "RGBA_PREMULT", "ARGB_PREMULT"
]

_im_format_to_gl_format: dict[_pg_im_formats, int] = {
    "P": GL.GL_R,
    "RGB": GL.GL_RGB,
    "RGBA": GL.GL_RGBA,
    "RGBX": GL.GL_RGBA,
    "ARGB": None,
    "BGRA": GL.GL_BGRA,
    "RGBA_PREMULT": None,
    "ARGB_PREMULT": None
}

class Sprite(ILoadable):
    _id_index = 0

    surface: pg.Surface
    width: int
    height : int
    sprite_id: int

    _gl_loaded: bool
    _gl_location: int

    def __init__(self, surface: pg.Surface):
        self.surface = surface
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.sprite_id = Sprite._id_index
        Sprite._id_index += 1
        self._gl_loaded = False
        self._gl_location = 0

    
    def im_data(self, format: _pg_im_formats) -> bytes:
        return pg.image.tobytes(self.surface, format)
    
    def gl_load(self, format: _pg_im_formats = "RGBA") -> bool:
        if self._gl_loaded:
            return True
        
        gl_format = _im_format_to_gl_format[format]

        GL.glGenTextures(1, self._gl_location)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._gl_location)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, gl_format, self.width, self.height, 0, gl_format, GL.GL_UNSIGNED_BYTE, self.im_data(format)) # TODO: Finish this function call

    def bind(self, format: _pg_im_formats = "RGBA", min_filter = GL.GL_LINEAR, max_filter = GL.GL_LINEAR, wrap_s = GL.GL_REPEAT, wrap_t = GL.GL_REPEAT):
        if not self._gl_loaded:
            self.gl_load(format)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._gl_location)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, wrap_s)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, wrap_t)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, min_filter)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, max_filter)
        GL.glActiveTexture(GL.GL_TEXTURE0)

    def load_from_file(path) -> "Sprite":
        try:
            surface = pg.image.load(path)
            return Sprite(surface)
        except Exception() as e:
            raise e

class _SpriteChar:
    _gl_id: int
    width: int
    height: int
    bearing_x: int
    bearing_y: int
    advance: int

    def __init__(self, tex_id, width, height, bearing_x, bearing_y, advance):
        self._gl_id = tex_id
        self.width = width
        self.height = height
        self.bearing_x = bearing_x
        self.bearing_y = bearing_y
        self.advance = advance

class SpriteFont(ILoadable):
    width: int
    height : int
    sprite_id: int

    _gl_loaded: bool
    _gl_location: int

    font_face: FT.Face

    chars: list[_SpriteChar]

    def __init__(self, font_face: FT.Face):
        self.font_face = font_face
        self.font_face.set_char_size(0, 12)
        self.chars = [None for _ in range(128)]

    def set_font_size(self, size: int):
        self.font_face.set_char_size(0, size)

    def generate_font(self):
        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
        for c in range(128):
            self.font_face.load_char(chr(c))
            glyph: FT.GlyphSlot = self.font_face.glyph
            bitmap: FT.Bitmap = glyph.bitmap
            
            width = bitmap.width
            height = bitmap.rows
            data = bitmap.buffer
            bearing_x = glyph.bitmap_left
            bearing_y = glyph.bitmap_top

            tex_id = None
            GL.glGenTextures(1, tex_id)
            GL.glBindTexture(GL.GL_TEXTURE_2D, tex_id)
            GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RED, width, height, 0, GL.GL_RED, GL.GL_UNSIGNED_BYTE, bitmap.buffer)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)

            self.chars[c] = _SpriteChar(tex_id, width, height, bearing_x, bearing_y, glyph.advance.x)

    def determine_string_width(self, string: str) -> int:
        width = 0
        for char in string:
            self.font_face.load_char(chr(char))
            glyph: FT.GlyphSlot = self.font_face.glyph
            width += glyph.advance.x
        return width

    def load_from_file(path):
        face = FT.Face(path)
        return SpriteFont(face)
        