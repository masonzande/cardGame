import numpy as np
import pygame as pg
import elements.card_grid
import elements.player_dock
from engine import Engine
from graphics import clear, create_ortho_projection, bind_buffer
from graphics.batcher import SpriteBatcher
from graphics.shader import Shader
from graphics.sprite import Sprite, SpriteFont
from OpenGL.GL import *
from loader import ContentLoader
from graphics.target import RenderTarget
import elements.card
from game_actions import CardGameActions

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
        self.target = RenderTarget(1280, 720)
        self.target.gl_load()

        self.display = pg.display.set_mode((1280, 720), pg.OPENGL | pg.DOUBLEBUF)

        self.card = elements.card.Card(None, pg.Vector2(75, 105))
        self.card.flip()
        self.grid = elements.card_grid.CardGrid(pg.Vector2(320, 64), 10, 8, pg.Vector2(64, 64))
        self.p1_dock = elements.player_dock.PlayerDock(pg.Vector2(0, 0), pg.Vector2(194, 720), 4)

        self.inputset = InputSet()
        CardGameActions.bind_defaults(self.inputset)        
        
    def load(self):
        self.shader = self.content.load_custom("./shaders/basic_vp3t2.sl", Shader)
        self.copy_shader = self.content.load_custom("./shaders/basic_vp3t2.sl", Shader)
        self.font_shader = self.content.load_custom("./shaders/text_vp3t2.sl", Shader)

        self.texture0 = self.content.load_custom("./card_portraits/Legendary - Giraffe.jpg", Sprite)
        self.texture1 = self.content.load_custom("./card_portraits/Common - Deer.png", Sprite)
        self.font0 = self.content.load_custom("./fonts/OpenSans-Regular.ttf", SpriteFont)
        self.font0.set_font_size(48)
        self.font0.generate_font()

        self.card.load(self.content)
        
        elements.card.CardDock.load(None, self.content)

    def update(self, clock: pg.time.Clock):
        self.inputset.update(self.event_queue)
        # Main Game Logic goes here!

        self.card.update(clock, self.inputset)
        self.grid.update_cards([self.card], self.inputset)
        self.grid.update(clock, self.inputset)
        self.p1_dock.show_hand()
        self.p1_dock.update_card([self.card], self.inputset)
        self.p1_dock.update(clock, self.inputset)

        self.dummy += 32 * clock.get_time() / 1000

    def draw(self):
        # Drawing logic goes here
        bind_buffer(self.target)
        clear(0.0, 0.0, 0.0)

        self.batcher.begin(self.copy_shader, font_program=self.font_shader)
        self.card.prerender(self.batcher)
        self.batcher.flush()

        self.batcher.begin(self.shader, font_program=self.font_shader)
        self.shader.set_uniform('mvp', create_ortho_projection(0, self.target.width, self.target.height, 0))
        self.grid.draw(self.batcher, 0)
        self.card.draw(self.batcher, 1, 0)
        self.p1_dock.draw(self.batcher, 0)
        self.batcher.flush()

        bind_buffer(None)
        clear(0.0, 0.0, 0.0)
        winx, winy = pg.display.get_window_size()
        self.shader.set_uniform('mvp', create_ortho_projection(0, winx, 0, winy))
        self.batcher.begin(self.shader, font_program=self.font_shader)
        self.batcher.draw(self.target, pg.Vector2(0, 0), pg.Vector2(self.target.width, self.target.height), 0)
        self.batcher.flush()

    def unload(self):
        self.dummy = 0

if __name__ == "__main__":
    game = CardGame()