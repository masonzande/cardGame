import pygame as pg
from engine import Engine
from graphics import clear, Batcher, Shader, VERTEX_DEFAULT, FRAGMENT_DEFAULT, create_ortho_projection
from OpenGL.GL import *

from graphics.vertices import VertexPosition2Color4

class CardGame(Engine):
    def __init__(self):
        super().__init__()

    def init(self):
        # Prefer this to logic in __init__, as this logic is called before load but after engine setup
        pg.display.set_caption("Card Game")
        self.dummy = 0
        self.b = True
        self.batcher = Batcher[VertexPosition2Color4]()
        self.shader = Shader(VERTEX_DEFAULT, FRAGMENT_DEFAULT)
        winx, winy = pg.display.get_window_size()
        self.shader.set_uniform('mvp', create_ortho_projection(0, winx, 0, winy))

    def load(self):
        pass

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
        #self.dummy += 0.25 * clock.get_time() / 1000

    def draw(self):
        clear(0.2, 0.0, 0.0)
        # Drawing logic goes here
        self.batcher.begin(self.shader)
        self.batcher.draw_indexed([VertexPosition2Color4(pg.Vector2(0, 0), pg.Color('white')), VertexPosition2Color4(pg.Vector2(32, 0), pg.Color('white')), VertexPosition2Color4(pg.Vector2(32, 32), pg.Color('white'))], [0, 1, 2])
        self.batcher.flush()
    def unload(self):
        self.dummy = 0

if __name__ == "__main__":
    game = CardGame()