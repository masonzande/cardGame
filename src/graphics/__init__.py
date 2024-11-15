import OpenGL.GL as _GL
import numpy as _np

def clear(r: float, g: float, b: float, a: float = 1):
    _GL.glClearColor(r, g, b, a)
    _GL.glClear(_GL.GL_COLOR_BUFFER_BIT | _GL.GL_DEPTH_BUFFER_BIT)

def create_ortho_projection(left: float, right: float, top: float, bottom: float):
    n = -1.0
    f = 1.0
    r_l = right - left
    t_b = top - bottom
    n_f = n - f
    rpl = right + left
    tpb = top + bottom
    npf = n + f
    scale = _np.array([
        [2 / r_l, 0, 0, 0],
        [0, 2 / t_b, 0, 0],
        [0, 0, 2 / n_f, 0],
        [0, 0, 0, 1],
    ], dtype=_np.float32)
    translation = _np.array([
        [1, 0, 0, -rpl / 2],
        [0, 1, 0, -tpb / 2],
        [0, 0, 1, -npf / 2],
        [0, 0, 0, 1]
    ], dtype=_np.float32)
    p = scale @ translation
    return p

if __name__ == "__main__":
    pass