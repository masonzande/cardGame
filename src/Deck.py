import random
import numpy as np


class Deck:
    def __init__(self, card_array, player):
        self.cards = card_array
        self.player = player

    def shuffle(self):
        np.random.shuffle(self.cards)

    def deal_one(self):
        """Remove and return the top card from the deck."""
        if len(self.cards) == 0:
            raise ValueError("No cards left in deck")
        top_card = self.cards[0]
        self.cards = self.cards[1:]  # Remove the top value from the array
        return top_card

    def __len__(self):
        """Return the number of cards remaining in the deck."""
        return self.cards.size

    def __str__(self):
        return f"Deck of {self.player}:\n{self.cards}"
