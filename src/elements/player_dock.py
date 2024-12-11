from typing import Callable
import pygame as pg
from graphics import batcher
from elements import card, player as _player
import input
import game_actions
from deck import Deck
    
class PlayerDock:
    hand: list[card.CardDock]
    player: _player.Player
    deck_dock: card.CardDock
    pos: pg.Vector2

    _top_card: card.Card

    def __init__(self, pos: pg.Vector2, size: pg.Vector2, hand_size: int, player: _player.Player):
        self.pos = pos
        dock_size = pg.Vector2(size.x / 3, size.x * 7 / 15)
        deck_size = pg.Vector2(size.x / 2, size.x * 7 / 10)
        base_dock_pos = pos + pg.Vector2(size.x / 3, (size.y - dock_size.y * hand_size - deck_size.y) / 3)
        deck_pos = pos + pg.Vector2(size.x / 4, 2 * base_dock_pos.y + hand_size * dock_size.y)
        self.hand = [card.CardDock(base_dock_pos + pg.Vector2(0, dock_size.y * i), dock_size) for i in range(hand_size)]
        self.deck_dock = card.CardDock(deck_pos, deck_size)
        self._top_card = None
        self.player = player
    
    def init_cards(self):
        for c in self.player.cards.values():
            c.move_to(pg.Vector2(self.deck_dock.bounds.center))
            c.set_state(card.CardState.IN_DECK)

    def update(self, clock: pg.time.Clock, inputs: input.InputSet[game_actions.CardGameActions]):
        for dock in self.hand:
            dock.pre_update(inputs)
            dock.card_above(self.player.cards.values(), inputs)
        self.deck_dock.pre_update(inputs)

        for dock in self.hand:
            dock.update(clock, inputs)
        self.deck_dock.update(clock, inputs)

        if self.deck_dock.holding == None: 
            if self._top_card:
                self._top_card.flip()
                self._top_card.set_state(card.CardState.IN_HAND)
            if not self.player.deck.empty():
                self.player.top_card().set_dock(self.deck_dock)
            self._top_card = self.deck_dock.holding

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
