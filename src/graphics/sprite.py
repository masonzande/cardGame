from typing import Literal
import pygame as pg
import OpenGL.GL as GL

from loader import ILoadable

import freetype as FT

_im_formats = Literal[
    "P", "RGB", "RGBX", "RGBA", "ARGB", "BGRA", "RGBA_PREMULT", "ARGB_PREMULT", "DEPTH_STENCIL"
]

_im_format_to_gl_format: dict[_im_formats, int] = {
    "P": GL.GL_R,
    "RGB": GL.GL_RGB,
    "RGBA": GL.GL_RGBA,
    "RGBX": GL.GL_RGBA,
    "ARGB": None,
    "BGRA": GL.GL_BGRA,
    "RGBA_PREMULT": None,
    "ARGB_PREMULT": None,
    "DEPTH_STENCIL": GL.GL_DEPTH24_STENCIL8
}

class TextureLike:
    _id_index = 0
    texture_id: int
    def __init__(self):
        self.texture_id = TextureLike._id_index
        TextureLike._id_index += 1

class Texture(TextureLike):
    width: int
    height: int

    _gl_loaded: bool
    _gl_location: int
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._gl_loaded = False
        self._gl_location = 0
        super().__init__()
        
    def gl_load(self, format: int = GL.GL_RGBA, internal_format: int = GL.GL_RGBA, dtype: int = GL.GL_UNSIGNED_BYTE, data: bytes = None) -> bool:
        if self._gl_loaded:
            return True
        self._gl_loaded = True
        
        self._gl_location = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._gl_location)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, internal_format, self.width, self.height, 0, format, dtype, data)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

    def bind(self, 
             format: int = GL.GL_RGBA,
             internal_format: int = GL.GL_RGBA,
             dtype: int = GL.GL_UNSIGNED_BYTE, 
             min_filter = GL.GL_LINEAR, 
             max_filter = GL.GL_LINEAR, 
             wrap_s = GL.GL_REPEAT, 
             wrap_t = GL.GL_REPEAT
            ):
        if not self._gl_loaded:
            self.gl_load(format=format, internal_format=internal_format, dtype=dtype)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._gl_location)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, wrap_s)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, wrap_t)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, min_filter)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, max_filter)
        GL.glActiveTexture(GL.GL_TEXTURE0)

    def unload(self):
        if self._gl_loaded:
            GL.glDeleteTextures(1, int(self._gl_location))

class Sprite(Texture, ILoadable):
    surface: pg.Surface

    def __init__(self, surface: pg.Surface):
        self.surface = surface
        super().__init__(self.surface.get_width(), self.surface.get_height())
    
    def im_data(self, format: _im_formats) -> bytes:
        return pg.image.tobytes(self.surface, format)
    
    def gl_load(self, format: _im_formats = "RGBA", internal_format = None, dtype: int = GL.GL_UNSIGNED_BYTE) -> bool:
        gl_format = _im_format_to_gl_format[format]
        if internal_format == None:
            internal_format = gl_format
        return super().gl_load(gl_format, internal_format, dtype, self.im_data(format))

    def bind(self, format: _im_formats = "RGBA", min_filter = GL.GL_LINEAR, max_filter = GL.GL_LINEAR, wrap_s = GL.GL_REPEAT, wrap_t = GL.GL_REPEAT):
        return super().bind(format=format, min_filter=min_filter, max_filter=max_filter, wrap_s=wrap_s, wrap_t=wrap_t)

    def load_from_file(path) -> "Sprite":
        try:
            surface = pg.image.load(path)
            return Sprite(surface)
        except Exception() as e:
            raise e

class _SpriteChar(TextureLike):
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
        super().__init__()

    def bind(self):
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._gl_id)

class SpriteFont(TextureLike, ILoadable):
    width: int
    height : int

    _gl_loaded: bool
    _gl_location: int

    font_face: FT.Face
    chars: list[_SpriteChar]

    def __init__(self, font_face: FT.Face):
        self.font_face = font_face
        self.font_face.set_pixel_sizes(0, 12)
        self.chars = [None for _ in range(128)]
        super().__init__()

    def set_font_size(self, size: int):
        self.font_face.set_pixel_sizes(0, size)

    def generate_font(self):
        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
        for c in range(128):
            self.font_face.load_char(c)
            glyph: FT.GlyphSlot = self.font_face.glyph
            bitmap: FT.Bitmap = glyph.bitmap
            
            width = bitmap.width
            height = bitmap.rows
            bearing_x = glyph.bitmap_left
            bearing_y = glyph.bitmap_top

            tex_id = 0
            tex_id = GL.glGenTextures(1)
            GL.glBindTexture(GL.GL_TEXTURE_2D, tex_id)
            GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RED, width, height, 0, GL.GL_RED, GL.GL_UNSIGNED_BYTE, bitmap.buffer)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)

            self.chars[c] = _SpriteChar(tex_id, width, height, bearing_x, bearing_y, glyph.advance.x)

    def string_dims(self, string: str) -> tuple[int, int, int]:
        width = 0
        bottom = 0
        top = 0
        for char in string:
            self.font_face.load_char(ord(char))
            glyph: FT.GlyphSlot = self.font_face.glyph
            width += glyph.advance.x >> 6
            top = glyph.bitmap.rows if glyph.bitmap.rows > top else top
            bottom = glyph.bitmap.rows - glyph.bitmap_top if glyph.bitmap.rows - glyph.bitmap_top < bottom else bottom
            
        return width, top - bottom, top

    def load_from_file(path):
        face = FT.Face(path)
        return SpriteFont(face)