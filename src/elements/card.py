import pygame as pg
import graphics.sprite
from InitAnimals import Animals as Animal
from loader import ContentLoader

# TODO: Convert all Assets to png
# ID any missing drawings and replace them with something stock

class Card:
    animal: Animal
    sprite: graphics.sprite.Sprite

    def __init__(self, animal: Animal):
        self.animal = animal

    def load(self, loader: ContentLoader):
        f_name = f"{self.animal.AnimalName} - {self.animal.Rarity}"
        self.sprite = loader.load_custom(f_name, graphics.sprite.Sprite)

  
        
