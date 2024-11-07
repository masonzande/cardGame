import pygame as pg
from engine import Engine
from graphics import clear, Batcher2D
from OpenGL.GL import *

class CardGame(Engine):
    def __init__(self):
        super().__init__()
    
    def init(self):
        # Prefer this to logic in __init__, as this logic is called before load but after engine setup
        pg.display.set_caption("Card Game")
        self.dummy = 0
        self.b = True
        self.batcher = Batcher2D()

    def load(self):
        pass

    def update(self, clock):
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
        self.dummy = 0
    
    def draw(self):
        clear(0.2, 0.0, 0.0)
        # Drawing logic goes here
        self.batcher.draw_rect(pg.Vector2(0, 0), pg.Vector2(0.5, 0.5))
        self.batcher.draw_rect(pg.Vector2(-1, -1), pg.Vector2(0.6, 0.8))
        self.batcher.flush()
    def unload(self):
        self.dummy = 0

if __name__ == "__main__":
    game = CardGame()