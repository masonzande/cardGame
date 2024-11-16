from typing import Literal
import pygame as pg
import OpenGL.GL as GL

from loader import ILoadable

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