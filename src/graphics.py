import OpenGL
from OpenGL.GL import glClearColor, glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT

def clear(r: float, g: float, b: float, a: float = 1):
    glClearColor(r, g, b, a)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)