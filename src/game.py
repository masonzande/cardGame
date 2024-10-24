import pygame as pg
from engine import Engine
from graphics import clear
from OpenGL.GL import *

class CardGame(Engine):
    def __init__(self):
        super().__init__()
    
    def init(self):
        # Prefer this to logic in __init__, as this logic is called before load but after engine setup
        pg.display.set_caption("Card Game")

    def load(self):
        self.dummy = 0
        self.b = True

    def update(self, clock):
        # Main Game Logic goes here!
        self.dummy = 0
    
    def draw(self):
        clear(self.dummy, 0.0, 0.0)
        # Drawing logic goes here
        pg.draw.rect(self.display, (0.0, 0.0, 1.0, 1.0), pg.Rect(12, 12, 12, 12))

    def unload(self):
        self.dummy = 0

if __name__ == "__main__":
    game = CardGame()