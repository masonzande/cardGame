'''
Abilities/StatusEffects:
    Fear = Subtracts attack from opposing animal (1 per size difference).
    OnSight = Ability happens on sight of the animal.
    Paralysis = Immobilization of animal. Chance 1-3 turns of no movement (50% chance of paralysis during that time).
    Flinch = Skip turn (Affects Lower Size Animals).
    Intellect = Able to use tools.
    Grouping = Animal is stronger in larger groups. Up to 5.
    Venom = Being bitten by the animal causes toxic damage. Max 2.
    Poison = Touching the animal causes toxic damage. Max 2.
    Bleed = Lose 1 health per level of bleed per turn. Max 3.
    Camoflauge = Unable to be seen easily. Visibility of animal is within one "space" distance. Enemy player knows that the card exists on the battlefield.
    ColdBlooded = Gains 1 HP per turn in sun (not over maximum), -1 HP per turn in wildfire, drought. Decreased speed in blizzard, tundra.
    Exhaustion = Level 1: Lose half speed, rounded down. Level 2: Paralysis. Max 2.
    Night Vision = Decreased loss of vision in the dark.
    Rations = +1 HP per turn (not over maximum).
    Scavenger = +1 HP (not over maximum) when resting on a square where an animal has died (one turn use per death on square).
'''

'''
Map of Animals to Abilities/Movesets/Movements:
    (All Animals Subject to Movement Exhaustion)
    (Animals From a Certain Biome do Not Receive Negative Status Effects From That Biome)
    (All Animals Can Double Movement of Any Time For One Additional Exhaustion Level)

    Natural Disaster = 1 Per Deck
    Legendary = 1 Per Deck
    Epic = 3 Per Deck
    Rare = 5 Per Deck
    Common = Any # Per Deck
    Weather = Any # Per Deck

    Rattlesnake Legendary
        Movement: Slither
        Bite: Venom, Paralysis
        ColdBlooded
        Camoflauge
        Rattle: Fear (All), Lowered Camoflauge
        Smell: Night Vision

    Camel Epic
        Movement: Walk
        Night Vision
        Stomp: Flinch
        Rations

    Scorpion Rare
        Movement: Walk
        OnSight: Fear (Larger)
        Tail Strike: Venom
        Night Vision
        ColdBlooded

    Silver Ant Common
        Movement: Walk
        Grouping
        ColdBlooded (+1 in Wildfire, Drought)
        Exhaustion: Halved
        Speed: HIGH (Exchange For 1 Attack Dmg)
        Scavenger
        Bite

    Wolf Rare
        Movement: Walk
        OnSight: Fear (All)
        Grouping
        Bite: Bleed
        Claw: Bleed
        Night Vision
        Smell: Reduces Camoflauge

    Grizzly Bear Legendary
        Movement: Walk
        OnSight: Fear (All)
        Immune to Fear
        Bite: Bleed
        Claw: Bleed
        Night Vision
        Smell: Reduces Camoflauge

    Black Bear Epic
        Movement: Walk, Climb
        Night Vision
        Smell: Reduces Camoflauge
        Bite: Bleed
        Claw: Bleed

    Deer Common
        Movement: Walk, Jump
        Night Vision
        Stomp: Flinch

    Rabbit Common
        Movement: Walk, Jump
        Stomp: Flinch

    Moose Epic
        Movement: Walk
        Stomp: Flinch
        Night Vision

    Eagle Rare
        Movement: Walk, Fly
        Claw

    Hawk Rare
        Movement: Walk, Fly
        Claw

    Shark
    Dolphin
    Orca
    Plankton
    Octopus
    Crab

    Lion
    Giraffe
    Elephant
        Body Slam: Paralysis

    Zebra
    Hyena
    Gazelle
    Bison
    Vulture

    Monkey
    Ape
    Alligator
    Crocodile
    Poison Frog

    Polar Bear
    Arctic Fox
    Penguin
    Seal
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
    Types (Slither, Climb, Fly, Walk, Swim).
        "Running" is possible for each type for double movement, but grants a level of exhaustion each use.
    Distance ranges, larger and faster animals get more range.
    Animals can have more than one method of movement.

    Jump = Able to Jump Over Obstacles. Jumps can happen right before attacks. 1 Level of Exhaustion.
    Climb = Able to Climb on/Off Obstacles.
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
    #Rank Relative to Environment

    #Legendary = 1 Per Deck
    #Epic = 3 Per Deck
    #Rare = 5 Per Deck
    #Common = Any # Per Deck

    #Natural Disaster = 1 Per Deck
    #Weather = Any # Per Deck

    Desert:
        Rattlesnake Legendary
        Camel Epic
        Scorpion Rare
        Silver Ant Common

    Forest:
        Wolf Rare
        Grizzly Bear Legendary
        Black Bear Epic
        Deer Common
        Rabbit Common
        Moose Epic
        Eagle Rare
        Hawk Rare

    Ocean:
        Shark Epic
        Dolphin Epic
        Orca Legendary
        Plankton Common
        Octopus Rare
        Crab Rare

    Grasslands:
        Lion Legendary
        Giraffe Epic
        Elephant Legendary
        Zebra Common
        Hyena Rare
        Gazelle Common
        Bison Epic
        Vulture Rare

    Rainforest:
        Monkey Rare
        Ape Rare
        Alligator Epic
        Crocodile Epic
        Poison Frog Common

    Tundra:
        Polar Bear Legendary
        Arctic Fox Rare
        Penguin Common
        Seal Common

Weather Cards:
    Rain, Sun, Clouds, Snow, Thunderstorm

    Natural Disasters (1 card per deck):
        Tsunami, Drought, Tornado, Earthquake, Meteor, Blizzard, Wildfire, Hail

Day / Night Cycle
    Some animals have night vision and see better than others at night
    Animals with camouflage get further reduced visibility at night. 
'''