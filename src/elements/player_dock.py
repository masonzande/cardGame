import pygame as pg
from graphics import batcher
from elements import card
import input
import game_actions
import deck

class PlayerDock:
    hand: list[card.CardDock]
    deck_dock: card.CardDock
    a_deck: deck.Deck

    def __init__(self, pos: pg.Vector2, size: pg.Vector2, hand_size: int):
        dock_size = pg.Vector2(size.x / 3, size.x * 7 / 15)
        deck_size = pg.Vector2(size.x / 2, size.x * 7 / 10)
        base_dock_pos = pg.Vector2(size.x / 3, (size.y - dock_size.y * hand_size - deck_size.y) / 3)
        deck_pos = pg.Vector2(size.x / 4, 2 * base_dock_pos.y + hand_size * dock_size.y)
        self.hand = [card.CardDock(base_dock_pos + pg.Vector2(0, dock_size.y * i), dock_size) for i in range(hand_size)]
        self.deck_dock = card.CardDock(deck_pos, deck_size)
    
    def set_deck(self, deck: deck.Deck):
        self.a_deck = deck

    def update(self, clock: pg.time.Clock, inputs: input.InputSet[game_actions.CardGameActions]):
        for dock in self.hand:
            dock.pre_update(inputs)
        self.deck_dock.pre_update(inputs)

        for dock in self.hand:
            dock.update(clock, inputs)
        self.deck_dock.update(clock, inputs)

    def update_card(self, cards: list[card.Card], inputs: input.InputSet[game_actions.CardGameActions]):
        for dock in self.hand:
            dock.card_above(cards, inputs)

    def hide_hand(self):
        pass
    def show_hand(self):
        pass

    def draw(self, batcher: batcher.SpriteBatcher, depth: float):
        for dock in self.hand:
            dock.draw(batcher, depth)
        self.deck_dock.draw(batcher, depth)
