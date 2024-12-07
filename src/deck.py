import random
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

    def deal_one(self):
        """Remove and return the top card from the deck."""
        if len(self.cards) == 0:
            raise ValueError("No cards left in deck")
        top_card = self.cards.pop(0)
        return top_card

    def __len__(self):
        """Return the number of cards remaining in the deck."""
        return len(self.cards)

    def __str__(self):
        return f"Deck of {self.player}:\n{self.cards}"
