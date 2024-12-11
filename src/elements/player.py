from deck import Deck
import loader
import animals
import elements.card as card
import pygame as pg
import input
import game_actions
import graphics.batcher

class Player:
    deck: Deck
    name: str

    cards: dict[str, card.Card]
    
    def __init__(self, name: str, deck: Deck = None):
        self.name = name
        self.deck = deck
        self._dock_ref = None
        self.cards = None

    def load_cards(self, card_size: pg.Vector2, loader: loader.ContentLoader):
        """Create a list of visual cards from the player deck and load their assets
        """
        self.cards = card.Card.from_deck(self.deck, card_size)
        for c in self.cards.values():
            c.load(loader)

    def update(self, clock: pg.time.Clock, inputs: input.InputSet[game_actions.CardGameActions]):
        if self.cards:
            for c in self.cards.values():
                c.update(clock, inputs)

    def shuffle(self):
        if self.deck:
            self.deck.shuffle()

    def top_card(self) -> card.Card:
        card = self.get_card(self.deck.deal_one())
        card.set_active(True)
        card.set_visible(True)
        return card

    def get_card(self, animal: str | animals.Animals) -> card.Card:
        if isinstance(animal, animals.Animals):
            animal = animal.AnimalName
        if animal in self.cards.keys():
            return self.cards[animal]
        return None
    
    def get_cards_in_state(self, state: card.CardState) -> list[card.Card]:
        out = []
        for c in self.cards.values():
            if c.current_state == state:
                out.append(c)
        return out
 
    def build_deck(self, animal_types: list[animals.AnimalType]):
        registered_list = [animals.Animals.CreateFrom(type, self.name) for type in animal_types]
        self.deck = Deck(registered_list, self.name)

    def prerender_cards(self, batcher: graphics.batcher.SpriteBatcher):
        for c in self.cards.values():
            c.prerender(batcher)

    def draw_cards(self, batcher: graphics.batcher.SpriteBatcher):
        for c in self.cards.values():
            c.draw(batcher, 1, 0)