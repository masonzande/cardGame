import OpenGL.GL as GL
import graphics.sprite as sprite

class RenderTarget:
    _gl_loaded: bool
    _gl_location: int
    _internal_texture: sprite.Texture
    _internal_depth_stencil: sprite.Texture


    width: int
    height : int

    def __init__(self, width, height):
        self._gl_location = 0
        self._gl_loaded = False
        self.width = width
        self.height = height
        self._internal_texture = sprite.Texture(width, height)
        self._internal_depth_stencil = sprite.Texture(width, height)

    def gl_load(self):
        if self._gl_loaded:
            return True
        
        GL.glGenFramebuffers(1, self._gl_location)
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self._gl_location)

        self._internal_texture.gl_load()
        GL.glFramebufferTexture2D(GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0, GL.GL_TEXTURE_2D, self._internal_texture._gl_location, 0)
        self._internal_depth_stencil.gl_load(format="DEPTH_STENCIL")
        GL.glFramebufferTexture2D(GL.GL_FRAMEBUFFER, GL.GL_DEPTH_STENCIL_ATTACHMENT, GL.GL_TEXTURE_2D, self._internal_depth_stencil._gl_location, 0)

        if GL.glCheckFramebufferStatus(GL.GL_FRAMEBUFFER) != GL.GL_FRAMEBUFFER_COMPLETE:
            print("GLERR: Framebuffer binding was incomplete!")

        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, None)

    def get_texture(self) -> sprite.Texture:
        return self._internal_texture
        