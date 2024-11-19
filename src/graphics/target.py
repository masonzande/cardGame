import OpenGL.GL as GL
import graphics.sprite as sprite

class RenderTarget:
    _gl_loaded: bool
    _gl_location: int
    _internal_texture: sprite.Texture
    _internal_depth: sprite.Texture


    width: int
    height : int

    def __init__(self, width, height):
        self._gl_location = 0
        self._gl_loaded = False
        self.width = width
        self.height = height
        self._internal_texture = sprite.Texture(width, height)
        self._internal_depth = sprite.Texture(width, height)

    def gl_load(self):
        if self._gl_loaded:
            return True
        
        self._gl_loaded = True

        self._gl_location = GL.glGenFramebuffers(1)
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self._gl_location)

        self._internal_texture.gl_load()
        GL.glFramebufferTexture2D(GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0, GL.GL_TEXTURE_2D, self._internal_texture._gl_location, 0)
        self._internal_depth.gl_load(format=GL.GL_DEPTH_COMPONENT, internal_format=GL.GL_DEPTH_COMPONENT, dtype=GL.GL_UNSIGNED_BYTE)
        GL.glFramebufferTexture2D(GL.GL_FRAMEBUFFER, GL.GL_DEPTH_ATTACHMENT, GL.GL_TEXTURE_2D, self._internal_depth._gl_location, 0)

        if GL.glCheckFramebufferStatus(GL.GL_FRAMEBUFFER) != GL.GL_FRAMEBUFFER_COMPLETE:
            print("GLERR: Framebuffer binding was incomplete!")

        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)


    def get_texture(self) -> sprite.Texture:
        return self._internal_texture
        