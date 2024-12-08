from deck import Deck
import loader
import numpy as np
from player_dock import PlayerDock
import animals
import elements.card as card
import pygame as pg
import input
import game_actions

class Player:
    deck: Deck
    _dock_ref: PlayerDock
    name: str

    cards: list[card.Card]
    
    def __init__(self, name: str, deck: Deck = None):
        self.name = name
        self.deck = deck
        self._dock_ref = None
        self.cards = None

    def load_cards(self, card_size: pg.Vector2, loader: loader.ContentLoader):
        """Create a list of visual cards from the player deck and load their assets
        """
        self.cards = card.Card.from_deck(self.deck, card_size)
        for c in self.cards:
            c.load(loader)

    def update(self, clock: pg.time.Clock, inputs: input.InputSet[game_actions.CardGameActions]):
        if self.cards:
            for c in self.cards:
                c.update(clock, inputs)

    def shuffle(self):
        if self.deck:
            self.deck.shuffle()

    def assign_to_dock(self, dock: PlayerDock):
        self._dock_ref = dock
        self._dock_ref.set_deck(self.deck)
    
    def build_deck(self, animal_types: list[animals.AnimalType]):
        registered_list = [animals.Animals.CreateFrom(type, self.name) for type in animal_types]
        self.deck = Deck(registered_list, self.name)
        if self._dock_ref:
            self._dock_ref.set_deck(self.deck)