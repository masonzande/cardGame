from engine import Engine
from OpenGL.GL import *

class CardGame(Engine):
    def __init__(self):
        super().__init__()

    def load(self):
        self.dummy = 0

    def update(self, clock):
        # Main Game Logic goes here!
        self.dummy = 0
    
    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        # Drawing logic goes here

    def unload(self):
        self.dummy = 0

if __name__ == "__main__":
    game = CardGame()