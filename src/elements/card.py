import pygame as pg
import graphics
import graphics.sprite
import graphics.batcher
import graphics.target
from InitAnimals import Animals as Animal
from loader import ContentLoader

# TODO: Convert all Assets to png
# ID any missing drawings and replace them with something stock

_CARD_SIZE: tuple[int, int] = (1500, 2100)
_PORTRAIT_HEIGHT: int = 1125

class Card:
    _loaded: bool
    _prerender_complete: bool

    animal: Animal

    border_sprite: graphics.sprite.Sprite
    background_sprite: graphics.sprite.Sprite
    portrait_sprite: graphics.sprite.Sprite

    card_render: graphics.target.RenderTarget

    bounds: pg.Rect

    def __init__(self, animal: Animal, size: pg.Vector2):
        self.animal = animal
        self._loaded = False
        self._prerender_complete = False

        self.bounds = pg.Rect(pg.Vector2(0), size)

        self.card_render = graphics.target.RenderTarget(_CARD_SIZE[0], _CARD_SIZE[1])

    def load(self, loader: ContentLoader):
        if self._loaded:
            return
        try:
            #f_name = f"./card_portraits/{self.animal.Rarity} - {self.animal.AnimalName}.png"
            f_name = "./card_portraits/Legendary - Giraffe.jpg"
            self.portrait_sprite = loader.load_custom(f_name, graphics.sprite.Sprite)
        except Exception as e:
            print("Failed to load animal image:", e)
            self.portrait_sprite = loader.load_custom("./card_portraits/Missing_Portrait.png", graphics.sprite.Sprite)

        f_name = f"./card_backgrounds/{"Grassland"}.png"
        self.background_sprite = loader.load_custom(f_name, graphics.sprite.Sprite)

        f_name = f"./card_backgrounds/{"Grassland"}_Border.png"
        self.border_sprite = loader.load_custom(f_name, graphics.sprite.Sprite)

        self.portrait_sprite.gl_load()
        self.background_sprite.gl_load()
        self.card_render.gl_load()
        
        self._loaded = True

    def prerender(self, batcher: graphics.batcher.SpriteBatcher):
        old = graphics.active_target

        batcher.program.set_uniform('mvp', graphics.create_ortho_projection(0, _CARD_SIZE[0], _CARD_SIZE[1], 0)) 

        batcher.flush()
        graphics.bind_buffer(self.card_render)
        graphics.clear(0.6, 0.72, 0.36, 1)

        batcher.draw(self.portrait_sprite, pg.Vector2(0, 0), pg.Vector2(_CARD_SIZE[0], _PORTRAIT_HEIGHT), 0)
        batcher.draw(self.border_sprite, pg.Vector2(0, 0), pg.Vector2(_CARD_SIZE[0], _CARD_SIZE[1]), 0)
        
        batcher.flush()
        graphics.bind_buffer(old)

        self._prerender_complete = True

    def nudge(self, diff: pg.Vector2):
        self.bounds = self.bounds.move(diff.x, diff.y)

    def draw(self, batcher: graphics.batcher.SpriteBatcher, render_scale: float, depth: float):
        if not self._prerender_complete:
            self.prerender(batcher)
        
        size_x, size_y = self.bounds.size
        pos_x, pos_y = self.bounds.topleft

        batcher.draw(self.card_render, pg.Vector2(pos_x, pos_y), pg.Vector2(size_x, size_y) * render_scale, depth)