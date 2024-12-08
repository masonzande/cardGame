import pygame as pg
from deck import Deck
import graphics
import graphics.sprite
import graphics.batcher
import graphics.target
from animals import Animals as Animal
from loader import ContentLoader
import input
from game_actions import CardGameActions
import loader
from enum import IntEnum

# TODO: Convert all Assets to png

_CARD_SIZE: tuple[int, int] = (1500, 2100)
_PORTRAIT_HEIGHT: int = 1125

class Card:
    _loaded: bool
    _prerender_complete: bool
    _rerender: bool

    _up: bool
    _actual_size: pg.Vector2

    _dock: "CardDock"
    _travel_back: bool

    _active: bool
    _visible: bool

    animal: Animal

    border_sprite: graphics.sprite.Sprite
    background_sprite: graphics.sprite.Sprite
    portrait_sprite: graphics.sprite.Sprite

    card_render: graphics.target.RenderTarget

    bounds: pg.Rect

    mouse_holding: bool

    def __init__(self, animal: Animal, size: pg.Vector2, active: bool = True):
        self.animal = animal
        self._loaded = False
        self._prerender_complete = False
        self._rerender = False
        self._up = False
        self._actual_size = size
        self._dock = None
        self._travel_back = False
        self._active = active
        self._visible = self._active

        self.mouse_holding = False
    
        self.bounds = pg.Rect(pg.Vector2(0), size)

        self.card_render = graphics.target.RenderTarget(_CARD_SIZE[0], _CARD_SIZE[1])

    def load(self, loader: ContentLoader):
        if self._loaded:
            return
        try:
            f_name = f"./card_portraits/{self.animal.Rarity} - {self.animal.animal_type}.png"
            #f_name = "./card_portraits/Legendary - Giraffe.jpg"
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

    def flip(self):
        self._up = not self._up
        self._rerender = True

    def update(self, time: pg.time.Clock, inputs: input.InputSet[CardGameActions]):
        if not self._active:
            return
        mouse_data = inputs.get_cursor_button(CardGameActions.PICK_UP, CardGameActions.CURSOR)

        if mouse_data == None:
            return

        if mouse_data["pressed"] and self.bounds.contains(mouse_data["position"], (0, 0)):
            mouse_pos = pg.Vector2(mouse_data["position"])

            self.lerp_to(mouse_pos - pg.Vector2(self.bounds.size) / 2, 0.75)
            self._travel_back = False
            self.mouse_holding = True

        if self.mouse_holding:
            mouse_pos = pg.Vector2(mouse_data["position"])
            self.lerp_to(mouse_pos - pg.Vector2(self.bounds.size) / 2, 0.75)
        elif self._dock:
            self._travel_back = True
            self.lerp_to(pg.Vector2(self._dock.bounds.center) - pg.Vector2(self.bounds.size) / 2, 0.4)

        if mouse_data["released"]:
            self.mouse_holding = False


    def prerender(self, batcher: graphics.batcher.SpriteBatcher):
        old = graphics.active_target

        batcher.program.set_uniform('mvp', graphics.create_ortho_projection(0, _CARD_SIZE[0], _CARD_SIZE[1], 0)) 

        batcher.flush()
        graphics.bind_buffer(self.card_render)
        graphics.clear(0.6, 0.72, 0.36, 1)

        if self._up:
            batcher.draw(self.portrait_sprite, pg.Vector2(0, 0), pg.Vector2(_CARD_SIZE[0], _PORTRAIT_HEIGHT), 0)
            batcher.draw(self.border_sprite, pg.Vector2(0, 0), pg.Vector2(_CARD_SIZE[0], _CARD_SIZE[1]), 0)
        else:
            batcher.draw(self.background_sprite, pg.Vector2(0, 0), pg.Vector2(_CARD_SIZE[0], _CARD_SIZE[1]), 0)
        
        batcher.flush()
        graphics.bind_buffer(old)

        self._prerender_complete = True
        self._rerender = False

    def nudge(self, diff: pg.Vector2):
        self.bounds.move_ip(diff.x, diff.y)

    def move_to(self, dest: pg.Vector2):
        curr = pg.Vector2(self.bounds.topleft)
        self.bounds.move_ip(dest - curr)

    def lerp_to(self, dest: pg.Vector2, t: float):
        curr = pg.Vector2(self.bounds.topleft)
        rdest = curr.lerp(dest, t)
        if (rdest - curr).length_squared() < 1:
            rdest = dest
        self.bounds.move_ip(rdest - curr)

    def resize(self, new_size: pg.Vector2):
        if new_size == None:
            new_size = self._actual_size
        
        adjust = (pg.Vector2(self.bounds.size) - new_size)
        self.nudge(adjust / 2)
        self.bounds = pg.Rect(self.bounds.topleft, pg.Vector2(self.bounds.size) - adjust)

    def draw(self, batcher: graphics.batcher.SpriteBatcher, render_scale: float, depth: float):
        if (not self._prerender_complete) or self._rerender:
            self.prerender(batcher)
        
        size_x, size_y = self.bounds.size
        pos_x, pos_y = self.bounds.topleft

        batcher.draw(self.card_render, pg.Vector2(pos_x, pos_y), pg.Vector2(size_x, size_y) * render_scale, depth)
    
    def set_active(self, state: bool):
        self._active = state

    def set_visible(self, state: bool):
        self._visible = state

    @classmethod
    def from_deck(cls, deck: Deck, size: pg.Vector2) -> list["Card"]:
        """Create the card objects for a deck.

        Create visual card objects for a given deck. 
        Cards generated in this way default to inactive so that they can be manually enabled when drawn from a dock

        @param deck: The deck to create card objects for
        @param size: The default size of the cards to generate
        @return: A list of Card objects
        """
        return [Card(animal, size, False) for animal in deck.animals]

class DockType(IntEnum):
    DECK = 0
    HAND = 1
    TILE = 2

class CardDock:
    Sprite: graphics.sprite.Sprite = None 

    bounds: pg.Rect
    holding: Card
    above: list[Card]

    dock_type: DockType

    def __init__(self, position: pg.Vector2, size: pg.Vector2, type: DockType = DockType.TILE):
        self.bounds = pg.Rect(position, size)
        self.above = []
        self.holding = None

        self.dock_type = type

    def load(self, loader: loader.ContentLoader):
        if CardDock.Sprite == None:
            CardDock.Sprite = loader.load_custom("./game_elements/Dock_Border.png", graphics.sprite.Sprite)

    def pre_update(self, inputs: input.InputSet):
        pass

    def update(self, clock: pg.time.Clock, inputs: input.InputSet):
        for card in self.above:
            if inputs.get_action_released(CardGameActions.PICK_UP):
                card._dock = self
                self.holding = card
            card.resize(self.bounds.size)
            card.lerp_to(pg.Vector2(self.bounds.center) - pg.Vector2(card.bounds.size) / 2, 0.7)    

    def card_above(self, cards: list[Card], inputs: input.InputSet) -> list[Card] :
        for card in self.above:
            card.resize(None)
        self.above = []
        for card in cards:
            if self.bounds.contains(card.bounds.center, (0, 0)):
                self.above.append(card)
        return self.above
    
    def draw(self, batcher: graphics.batcher.SpriteBatcher, depth: float):
        batcher.draw(CardDock.Sprite, pg.Vector2(self.bounds.topleft), pg.Vector2(self.bounds.size), depth)