import random
from types import NoneType
import numpy as np
import animals

class Deck:
    cards: list[animals.Animals]
    player: str

    def __init__(self, card_array: np.ndarray[animals.Animals] | list[animals.Animals], player: str):
        self.cards = card_array.tolist() if isinstance(card_array, np.ndarray) else card_array
        self.player = player

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_one(self) -> animals.Animals | NoneType:
        """Remove and return the top card from the deck."""
        top_card = None
        if len(self.cards) > 0:
            top_card = self.cards.pop(0)
        return top_card
    
    def empty(self) -> bool:
        return len(self.cards) == 0

    def __len__(self):
        """Return the number of cards remaining in the deck."""
        return len(self.cards)

    def __str__(self):
        return f"Deck of {self.player}:\n{self.cards}"
