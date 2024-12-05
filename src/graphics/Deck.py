import random
import numpy as np


class Deck:
    def __init__(self, card_queue, player):
        self.card_queue = card_queue  # numpy array
        self.player = player  # string

    # randomizes the deck
    def shuffle(self):
        np.random.shuffle(self.card_queue)

    # removes top card from the deck
    def deal_one(self):
        if len(self.card_queue) == 0:
            raise ValueError("No cards left in deck")
        drawn_card = self.card_queue[0]
        self.card_queue = self.card_queue[1:]  # Remove the top card from the array

    # returns deck size
    def __len__(self):
        return self.card_queue.size

    def __str__(self):
        return f"Player {self.player} list of cards:\n{self.card_queue}"
