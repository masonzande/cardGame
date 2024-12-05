import pygame as pg     # Using PyGame primarily for windowing and other framework style tasks
from OpenGL.GL import glGetString, GL_VERSION
import OpenGL.GL as GL

class Engine:
    def __init__(self):
        pg.init()
        self.display = pg.display.set_mode((680, 480), pg.OPENGL | pg.DOUBLEBUF)
        print(glGetString(GL_VERSION) )
        self.clock = pg.time.Clock()
        self.event_queue = None
        self.init()
        self.load()
        self.tickLoop()
        
    def tickLoop(self):
        running = True
        while running:
            self.clock.tick(60)
            for ev in pg.event.get(eventtype=pg.QUIT):
                if ev.type == pg.QUIT:
                    running = False
            if running:
                self.event_queue = pg.event.get()
                self.update(self.clock)
                self.draw()
                pg.display.flip() # Equivalent to swapping backbuffer and displaybuffer in raw OpenGL
        self.quit()           # Unload

    def init(self):
        raise NotImplementedError("Implement 'init' in super class.")

    def update(self, clock: pg.time.Clock):
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