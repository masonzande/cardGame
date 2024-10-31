#Class For Every Animal in The Game.
class Animals:

    AnimalList = [] #List of Every Animal.

    #Define an Animal Object.
    #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.
    def __init__(Animal, AnimalName, Rarity, Health, Armor, AttackTypes, MovementTypes, AbilityTypes):

        #Animal Name/Rarity/Health/Armor.
        Animal.AnimalName = AnimalName #String Name of The Animal. Unique.
        Animal.Rarity = Rarity #String Rarity of The Animal. (Common/Rare/Epic/Legendary)
        Animal.Health = Health #Integer. The Health of an Animal. Reaching 0 Means The Card is Removed From The Battlefield.
        Animal.Armor = Armor #Integer. Damage Done Affects Armor First. Health Cannot be Damaged When Armor Has Not Broken.
        Animals.AnimalList.append(Animal) #The Animals Class Contains a List of Every Animal

        #Animal Movement.
        Animal.MovementTypes = MovementTypes #Dictionary of String Movement Types For This Animal Mapped to Integer Movement Radii.

        #Animal Attacks/Abilities.
        Animal.AttackTypes = AttackTypes #{AttackType: Damage, AttackType: Damage}. {ClassObject: Damage}.
        Animal.AbilityTypes = AbilityTypes #{Condition: Ability}.

    #Animal Attacks a Defender. Object Method.
    def Attack(Animal, Defender, Damage, Defenders, AttackType):

        #Default Damage to Armor Before Health.
        if Defender.Armor > 0:
            #Remove Damage From Armor.
            Defender.Armor -= Damage

            #Animals Cannot Have Armor Below Zero.
            if Defender.Armor < 0:
                Defender.Armor = 0

        else:
            #Remove Damage From Health.
            Defender.Health -= Damage

            #Animals Cannot Have Health Below Zero.
            if Defender.Health <= 0:
                Defender.Health = 0

                #Remove Dead Animal From AnimalList.
                Defenders.remove(Defender)

        return Defenders

    #Print The Stats of an Animal. Object Mathod.
    def PrintAnimal(Animal, Tabs = ""):

        print(f"\n{Tabs}{Animal}:")
        print(f"\t{Tabs}Health: {Animal.Health}")
        print(f"\t{Tabs}Armor: {Animal.Armor}")

    #Print The Stats of All Animals. Class Mathod.
    def PrintAllAnimals():

        print("\nStatistics of All Animals:")
        for Animal in Animals.AnimalList:
            Animal.PrintAnimal("\t")

    #Print Animal.AnimalName When print(Animal).
    def __str__(Animal):

        return Animal.AnimalName

#Class For Every Attack Type in The Game.
class AttackTypes:

    AttackTypeList = [] #List of Every AttackType.

    #Define an Attack Type Object.
    def __init__(AttackType, AttackName, AttackRadius, SplashDamage):

        AttackType.AttackName = AttackName  #String Name of The Attack. Unique.
        AttackType.AttackRadius = AttackRadius #Integer. Number of Squares That The Attack Can Reach Without Being Hindered.
        AttackType.SplashDamage = SplashDamage #(Boolean, Damage). Whether or Not The Attack Has Splash Damage, The Damage to Add to Splashed Targets.
        AttackTypes.AttackTypeList.append(AttackType) #The AttackTypes Class Contains a List of Every AttackType

#Create The Animals + Attack Types.
def CreateAnimalsAndAttackTypes():

    #Create AttackTypes: "AttackName", AttackRadius, [SplashBool, SplashDamage (Added to Damage, Minimum 1)]
    AttackTypes("Bite", 1, (False, 0))
    AttackTypes("Stomp", 1, (False, 0))
    AttackTypes("Tail Strike", 1, (False, 0))
    AttackTypes("Claw", 1, (True, -1))
    AttackTypes("Horns", 2, (True, -1))
    AttackTypes("Tail Slam", 2, (True, -1))
    AttackTypes("Punch", 1, (False, 0))
    AttackTypes("Grab", 1, (False, 0))
    AttackTypes("Body Slam", 2, (True, 0))
    AttackTypes("Bite Spin", 1, (False, 0))


    #Create Rattlesnake (Legendary).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[0]: (1, "Venom", "Paralysis")
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("ColdBlooded", "Camoflauge"),
        "Rattle": ("Fear All", "Lower Camoflauge"),
        "Smell": ("Night Vision")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Slither": 3
    }

    Animals("Rattlesnake", "Legendary", 10, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Camel (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[1]: (2, "Flinch")
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Night Vision", "Rations")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2
    }

    Animals("Camel", "Rare", 20, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Scorpion (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[2]: (1, "Venom")
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Night Vision", "ColdBlooded"),
        "OnSight": ("Fear Larger")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2
    }

    Animals("Scorpion", "Rare", 8, 1, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Silver Ant (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[0]: tuple([1])
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Grouping", "ColdBlooded (+1 in Wildfire, Drought)", "Exhaustion Halved", "Scavenger")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 6
    }

    Animals("Silver Ant", "Rare", 5, 2, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Wolf (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[0]: (2, "Bleed"),
        AttackTypes.AttackTypeList[3]: (1, "Bleed")
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Grouping", "Night Vision"),
        "OnSight": ("Fear All"),
        "Smell": ("Reduces Camoflauge")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3
    }

    Animals("Wolf", "Rare", 12, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Grizzly Bear (Legendary).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[0]: (3, "Bleed"),
        AttackTypes.AttackTypeList[3]: (2, "Bleed")
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Immune to Fear", "Night Vision"),
        "OnSight": ("Fear All"),
        "Smell": ("Reduces Camoflauge")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3
    }

    Animals("Grizzly Bear", "Legendary", 20, 1, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Black Bear (Epic).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[0]: (2, "Bleed"),
        AttackTypes.AttackTypeList[3]: (2, "Bleed")
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Night Vision"),
        "Smell": ("Reduces Camoflauge")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3,
        "Climb": 1
    }

    Animals("Black Bear", "Epic", 17, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Deer (Common).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[1]: (1, "Flinch"),
        AttackTypes.AttackTypeList[4]: (2, "Bleed")
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Night Vision")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3,
        "Jump": 2
    }

    Animals("Deer", "Common", 10, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Rabbit (Common).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[1]: (1, "Flinch")
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ()
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 4,
        "Jump": 2
    }

    Animals("Rabbit", "Common", 6, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Moose (Epic).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[1]: (2, "Flinch"),
        AttackTypes.AttackTypeList[4]: (3, "Bleed")
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Night Vision")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3,
        "Swim": 2
    }

    Animals("Moose", "Epic", 15, 3, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Eagle (Common).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[3]: tuple([2]),
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ()
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 1,
        "Fly": 4
    }

    Animals("Eagle", "Common", 6, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Hawk (Common).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[3]: tuple([2]),
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ()
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 1,
        "Fly": 3
    }

    Animals("Hawk", "Common", 7, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Shark (Epic).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[0]: (3, "Bleed"),
        AttackTypes.AttackTypeList[5]: (2, "Flinch")
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Night Vision"),
        "OnSight": ("Fear Smaller")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Swim": 3
    }

    Animals("Shark", "Epic", 14, 4, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Dolphin (Epic).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[5]: (1, "Flinch")
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Intellect", "Grouping", "Night Vision"),
        "Echo Location": ("Removes Camoflauge")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Swim": 4
    }

    Animals("Dolphin", "Epic", 12, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Orca (Legendary).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[0]: (3, "Bleed"),
        AttackTypes.AttackTypeList[5]: (3, "Flinch")
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Intellect", "Grouping"),
        "OnSight": ("Fear All"),
        "Echo Location": ("Night Vision", "Removes Camoflauge")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Swim": 3
    }

    Animals("Orca", "Legendary", 20, 5, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Plankton (Common).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Grouping", "Rations")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Swim": 1
    }

    Animals("Plankton", "Common", 2, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Octopus (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[6]: tuple([1]),
        AttackTypes.AttackTypeList[7]: (0, "Paralysis")
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Night Vision", "Intellect", "Camoflauge")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Swim": 2
    }

    Animals("Octopus", "Rare", 9, 1, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Crab (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[3]: tuple([2])
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Night Vision Reduced", "Camoflauge")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2,
        "Swim": 1
    }

    Animals("Crab", "Rare", 3, 6, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Lion (Legendary).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[0]: (3, "Bleed"),
        AttackTypes.AttackTypeList[3]: (2, "Bleed")
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Night Vision", "Grouping"),
        "OnSight": ("Fear All")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3
    }

    Animals("Lion", "Legendary", 16, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Giraffe (Legendary).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[1]: (3, "Flinch")
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ()
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2
    }

    Animals("Giraffe", "Legendary", 25, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Elephant (Legendary).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[8]: (3, "Paralysis"),
        AttackTypes.AttackTypeList[7]: (0, "Paralysis"),
        AttackTypes.AttackTypeList[1]: (2, "Flinch")
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ()
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2
    }

    Animals("Elephant", "Legendary", 20, 4, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Zebra (Common).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[1]: (1, "Flinch")
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Night Vision", "Grouping")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3
    }

    Animals("Zebra", "Common", 12, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Hyena (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[0]: (2, "Bleed"),
        AttackTypes.AttackTypeList[3]: (1, "Bleed")
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Night Vision", "Grouping", "Scavenger", "Camoflauge")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3
    }

    Animals("Hyena", "Rare", 12, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Gazelle (Common).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[1]: (1, "Flinch"),
        AttackTypes.AttackTypeList[4]: (2, "Bleed")
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Grouping", "Camoflauge")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3,
        "Jump": 2
    }

    Animals("Gazelle", "Common", 10, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Bison (Epic).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[1]: (2, "Flinch"),
        AttackTypes.AttackTypeList[8]: (3, "Flinch")
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Grouping"),
        "Grouping": ("Stomp Paralysis")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3
    }

    Animals("Bison", "Epic", 15, 2, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Vulture (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[3]: tuple([2])
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Scavenger", "Night Vision Reduced"),
        "Grouping": ("Stomp Paralysis")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 1,
        "Fly": 3
    }

    Animals("Vulture", "Rare", 8, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Monkey (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[6]: tuple([1])
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Intellect")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2,
        "Climb": 2
    }

    Animals("Monkey", "Rare", 9, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Ape (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[6]: tuple([2]),
        AttackTypes.AttackTypeList[7]: (0, "Paralysis")
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Intellect")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2
    }

    Animals("Ape", "Rare", 13, 1, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Alligator (Epic).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[0]: (3, "Bleed"),
        AttackTypes.AttackTypeList[9]: (4, "Bleed"),
        AttackTypes.AttackTypeList[5]: (2, "Flinch")
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Night Vision", "Camoflauge"),
        "OnSight": ("Fear All")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2,
        "Swim": 2
    }

    Animals("Alligator", "Epic", 17, 6, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Crocodile (Epic).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[0]: (3, "Bleed"),
        AttackTypes.AttackTypeList[9]: (4, "Bleed"),
        AttackTypes.AttackTypeList[5]: (2, "Flinch")
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Night Vision", "Camoflauge"),
        "OnSight": ("Fear All")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2,
        "Swim": 2
    }

    Animals("Crocodile", "Epic", 21, 2, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Poison Frog (Common).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": (),
        "Hurt": ("Poison")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 1,
        "Jump": 2
    }

    Animals("Poison Frog", "Common", 7, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Polar Bear (Legendary).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[0]: (4, "Bleed"),
        AttackTypes.AttackTypeList[3]: (3, "Bleed")
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Night Vision", "Camoflauge"),
        "OnSight": ("Fear All")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3,
        "Swim": 3
    }

    Animals("Polar Bear", "Legendary", 20, 5, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Arctic Fox (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[0]: tuple([2]),
        AttackTypes.AttackTypeList[3]: tuple([1])
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Night Vision", "Camoflauge"),
        "Bark": ("Fear Smaller")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2
    }

    Animals("Arctic Fox", "Rare", 8, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Penguin (Common).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[0]: tuple([1])
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Night Vision")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 1,
        "Swim": 2
    }

    Animals("Penguin", "Common", 8, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Seal (Common).
    AnimalAttacks = { #AttackType Object: (Damage, "Abilities")
        AttackTypes.AttackTypeList[8]: (1, "Paralysis"),
    }

    AnimalAbilities = { #"Activation": ("Abilities")
        "None": ("Night Vision", "Camoflauge")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Swim": 2
    }

    Animals("Seal", "Common", 12, 1, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.