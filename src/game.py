import pygame as pg
from engine import Engine
from graphics import clear, create_ortho_projection, bind_buffer
from graphics.batcher import ShapeBatcher, SpriteBatcher
from graphics.shader import Shader, VERTEX_DEFAULT, FRAGMENT_DEFAULT
from graphics.sprite import Sprite, SpriteFont
from graphics.vertices import VertexPosition2Color4
from OpenGL.GL import *
from loader import ContentLoader
from graphics.target import RenderTarget


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
        
    def load(self):
        self.shader = self.content.load_custom("./shaders/basic_vp3t2.sl", Shader)
        self.font_shader = self.content.load_custom("./shaders/text_vp3t2.sl", Shader)
        winx, winy = pg.display.get_window_size()
        self.shader.set_uniform('mvp', create_ortho_projection(0, winx, 0, winy))
        self.texture0 = self.content.load_custom("./card_portraits/Legendary - Giraffe.jpg", Sprite)
        self.texture1 = self.content.load_custom("./card_portraits/Common - Deer.png", Sprite)
        self.font0 = self.content.load_custom("./fonts/OpenSans-Regular.ttf", SpriteFont)
        self.font0.generate_font()

    def update(self, clock: pg.time.Clock):
        # Main Game Logic goes here!
        for event in self.event_queue:
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.TEXTINPUT:
                print(event.text, end="")
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    print("\n")
            # print(pg.event.event_name(event.type))
        self.dummy += 32 * clock.get_time() / 1000

    def draw(self):
        # Drawing logic goes here
        bind_buffer(self.target)
        clear(0.0, 0.0, 0.0)
        self.batcher.begin(self.shader)
        self.batcher.draw(self.texture0, pg.Vector2(32, 32), pg.Vector2(256, 128+64), 0)
        self.batcher.draw(self.texture1, pg.Vector2(92, 63), pg.Vector2(256, 256), 0)
        self.batcher.flush()

        bind_buffer(None)
        clear(0.0, 0.0, 0.0)
        self.batcher.begin(self.shader, font_program=self.font_shader)
        self.batcher.draw(self.target, pg.Vector2(32, 32), pg.Vector2(256, 128+64), 0.5)
        self.batcher.draw(self.target, pg.Vector2(287, 67), pg.Vector2(256, 128+64), 0.5)
        self.batcher.draw_string(self.font0, "Hello!", pg.Vector2(0, 0), 0)
        self.batcher.flush()

    def unload(self):
        self.dummy = 0

# TODO | Next steps for windowing:
# - Text Rendering
#     - Font loading and texture generation already handled
#     - Need to add a render target system and a text batcher for handling actually drawing text
# - Camera and Gridworld setup
# - Two-click or drag and drop moveable elements

if __name__ == "__main__":
    game = CardGame()