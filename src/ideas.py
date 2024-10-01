'''
Abilities/StatusEffects:
    Fear = Subtracts attack from opposing animal (1 per size difference).
    OnSight = Ability happens on sight of the animal.
    Paralysis = Immobilization of animal. Chance 1-3 turns of no movement (50% chance of paralysis during that time).
    Intellect = Able to use tools.
    Grouping = Animal is stronger in larger groups. Up to 5.
    Venom = Being bitten by the animal causes toxic damage. Max 2.
    Poison = Touching the animal causes toxic damage. Max 2.
    Bleed = Lose 1 health per level of bleed per turn. Max 3.
    Camoflauge = Unable to be seen easily. Visibility of animal is within one "space" distance. Enemy player knows that the card exists on the battlefield.
    ColdBlooded = Gains 1 HP per turn in sun.
    Exhaustion = Level 1: Lose half speed, rounded down. Level 2: Paralysis. Max 2.
'''

'''
Attacks:
    Attacking any animal with poison will cause the attacker to receive poison damage.

    BiteSpin = Bite and spin around to deal bleed damage.
    Bite = Attack an animal using teeth. Possible venom/bleed damage.
    Claw = Attack an animal using claws/talons. Possible bleed damage.
    TailSpin = Attack nearby animals using a tail. Possible poison damage if animal has poison.
    Punch = Attack an animal using a fist. Possible poison damage if animal has poison.
'''

'''
Tool Cards:
    Can only be used by animals with Intellect.

    Axe (+1 damage to a punch attack, no posion damage for punching if animal has poison, can cut trees)
    Sword (+2 damage to a punch attack, no posion damage for punching if animal has poison)
    pickaxe (+1 damage to a punch attack, no posion damage for punching if animal has poison, can break rocks)
'''

'''
Movements:
    Types (Slither, Fly, Walk, Swim).
        "Running" is possible for each type for double movement, but grants a level of exhaustion each use.
    Distance ranges, larger and faster animals get more range.
    Animals can have more than one method of movement.

    Amphibians can both walk and swim.
    Birds can both walk and fly.
    Fly can go over obstructions.
    Slither/Fly can perch on obstructions.
    Swim cannot move on land.
    Only swim can move in water.
    Only Fly can move in the air.
    Fly can only move/perch one "space" away in a cave.
'''

'''
Game Design:
    Environment:
        Desert, Forest, Ocean, Savannah, Plains, Cave, Tundra.
        Each environment buffs the animals from that respective environment and nerfs one other environment's animals.
        A random environment is chosen for every match with some environmental obstacles randomly assigned.
            A random weather event is chosen to start a match and it changes every 5 turns.
            Every 15th turn, a weather event happens as a natural disaster corresponding to the last weather type.
                Examples:
                    (sunny == drought, wildfire, or meteor as these are all possible)
                    (cloudy == tornado or metero as these are both possible)
        Any animal can be played in any environment.

    Objective:
        Kill all the opponent's animals. Loss happens when the opponent does not have any animal on the field.

    Player Card Usage:
        There is a set of cards in the game and the player may have one deck of a subset of these cards.
        The decks are randomized into a queued list of length 25.
        The player can have a hand of 5 cards from the top of the deck (front of list).
        There can be up to 6 animals on the battlefield per side.
        Cards can have duplicates in the deck (based on rarity).
            Legendary 1-2, Rare 3, Common 4-5
'''

'''
Animals:
    Desert:
        Rattlesnake
        Scorpion
        Silver Ant
        Camel

    Forest:
        Wolf
        Grizzly Bear
        Black Bear
        Deer
        Rabbit
        Moose
        Monkey
        Ape

    Ocean:
        Shark
        Dolphin
        Orca
        Plankton
        Octopus
        Crab

    Savannah:
        Lion
        Giraffe
        Elephant
        Zebra
        Hyena
        Gazelle

    Plains:
        Bison

    Cave:
        Neanderthal

    Swamp:
        Alligator
        Crocodile

    Sky:
        Vulture
        Eagle
        Hawk

    Tundra:
        Polar Bear
        Arctic Fox
        Penguin

Weather Cards:
    Rain, Sun, Clouds, Snow, Thunderstorm

    Natural Disasters (1 card per deck):
        Tsunami, Drought, Tornado, Earthquake, Meteor, Blizzard, Wildfire, Hail
'''