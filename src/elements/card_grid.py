import pygame as pg
from graphics import batcher
from elements import card
import input
import game_actions

class CardGrid:
    docks: list[list[card.CardDock]]
    
    def __init__(self, pos: pg.Vector2, width: int, height: int, dock_size: pg.Vector2):
        self.docks = [[None for _ in range(width)] for _ in range(height)]
        for j in range(height):
            for i in range(width):
                x_pos = pos.x + i * dock_size.x
                y_pos = pos.y + j * dock_size.y
                self.docks[j][i] = card.CardDock(pg.Vector2(x_pos, y_pos), dock_size)

    def update(self, clock: pg.time.Clock, inputs: input.InputSet[game_actions.CardGameActions]):
        for row in self.docks:
            for dock in row:
                dock.pre_update(inputs)
        for row in self.docks:
            for dock in row:
                dock.update(clock, inputs)

    def update_cards(self, cards: list[card.Card], inputs: input.InputSet[game_actions.CardGameActions]):
        for row in self.docks:
            for dock in row:
                dock.card_above(cards, inputs)

    def draw(self, batcher: batcher.SpriteBatcher, depth: float):
        for row in self.docks:
            for dock in row:
                dock.draw(batcher, depth)
    