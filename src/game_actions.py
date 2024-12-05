from enum import StrEnum
from input import InputSet, Cursor, Button, Key
import pygame as pg

class CardGameActions(StrEnum):
    CURSOR = "CURSOR"
    PICK_UP = "PICK_UP"

    @staticmethod
    def bind_defaults(input_set: InputSet):
        input_set.register_input(CardGameActions.PICK_UP, Button(pg.BUTTON_LEFT))
        input_set.register_cursor(CardGameActions.CURSOR, Cursor())