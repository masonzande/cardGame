import numpy as np
import pygame as pg

def pg_color_to_numpy_array(color: pg.Color):
    return np.array([color.r, color.g, color.b, color.a], dtype=np.float32) / 255