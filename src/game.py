import numpy as np
import pygame as pg
from engine import Engine
from graphics import clear, create_ortho_projection, bind_buffer
from graphics.batcher import SpriteBatcher
from graphics.shader import Shader
from graphics.sprite import Sprite, SpriteFont
from OpenGL.GL import *
from loader import ContentLoader
from graphics.target import RenderTarget

from input import Cursor, InputSet, Key, Button

class CardGame(Engine):
    def __init__(self):
        super().__init__()

    def init(self):
        # Prefer this to logic in __init__, as this logic is called before load but after engine setup
        pg.display.set_caption("Card Game")
        self.dummy = 0
        self.b = True
        self.batcher = SpriteBatcher()
        self.content = ContentLoader()
        self.target = RenderTarget(800, 600)
        self.target.gl_load()

        self.inputset = InputSet()
        
    def load(self):
        self.shader = self.content.load_custom("./shaders/basic_vp3t2.sl", Shader)
        self.font_shader = self.content.load_custom("./shaders/text_vp3t2.sl", Shader)
        winx, winy = pg.display.get_window_size()
        self.shader.set_uniform('mvp', create_ortho_projection(0, winx, 0, winy))
        self.texture0 = self.content.load_custom("./card_portraits/Legendary - Giraffe.jpg", Sprite)
        self.texture1 = self.content.load_custom("./card_portraits/Common - Deer.png", Sprite)
        self.font0 = self.content.load_custom("./fonts/OpenSans-Regular.ttf", SpriteFont)
        self.font0.set_font_size(48)
        self.font0.generate_font()

    def update(self, clock: pg.time.Clock):
        self.inputset.update(self.event_queue)
        # Main Game Logic goes here!


        self.dummy += 32 * clock.get_time() / 1000

    def draw(self):
        # Drawing logic goes here
        bind_buffer(self.target)
        clear(0.0, 0.0, 1.0)
        self.batcher.begin(self.shader, font_program=self.font_shader)
        self.batcher.draw(self.texture0, pg.Vector2(32, 32), pg.Vector2(256, 128+64), 0)
        self.batcher.draw(self.texture1, pg.Vector2(92, 63), pg.Vector2(256, 256), 0)
        self.batcher.flush()

        bind_buffer(None)
        clear(0.0, 0.0, 0.0)
        self.batcher.begin(self.shader, font_program=self.font_shader)
        self.batcher.draw(self.target, pg.Vector2(32, 32), pg.Vector2(256, 128+64), 0.5)
        self.batcher.draw(self.target, pg.Vector2(287, 67), pg.Vector2(256, 128+64), 0.5)
        self.batcher.draw_string(self.font0, "Hello!", pg.Vector2(5, 5), 0)
        self.batcher.flush()

    def unload(self):
        self.dummy = 0

# TODO | Next steps for windowing:
# - Camera and Gridworld setup
# - Two-click or drag and drop moveable elements

if __name__ == "__main__":
    game = CardGame()