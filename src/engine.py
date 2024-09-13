import pygame as pg     # Using PyGame primarily for windowing and other framework style tasks
from OpenGL.GL import *

class Engine:
    def __init__(self):
        pg.init()
        pg.display.set_mode((680, 480), pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()

        glClearColor(0.5, 0.0, 0.8, 1.0) # Set a default clear color

        self.load()
        self.tickLoop()
    
    def tickLoop(self):
        running = True
        while running:
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    running = False
            self.clock.tick(60)
            self.update(self.clock)
            self.draw()
            pg.display.flip() # Equivalent to swapping backbuffer and displaybuffer in raw OpenGL
        self.quit() # Unload

    def update(self, clock):
        raise NotImplementedError("Implement 'update' in super class.")

    def draw(self):
        raise NotImplementedError("Implement 'draw' in super class.")

    def load(self):
        raise NotImplementedError("Implement 'load' in super class.")

    def unload(self):
        raise NotImplementedError("Implement 'unload' in super class.")

    def quit(self):
        self.unload()
        pg.quit()

if __name__ == "__main__":
    game = Engine()