#Class For Every Animal in The Game.
class Animals:

    AnimalList = [] #List of Every Animal.

    #Define an Animal Object.
    #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.
    def __init__(Animal, AnimalName, Rarity, Health, Armor, AttackTypes, MovementTypes, AbilityTypes):

        #Animal Name/Rarity/Health/Armor.
        Animal.AnimalName = AnimalName #String Name of The Animal. Unique.
        Animal.Rarity = Rarity #String Rarity of The Animal. (Common/Rare/Epic/Legendary).
        Animal.Health = Health #Integer. The Health of an Animal. Reaching 0 Means The Card is Removed From The Battlefield.
        Animal.Armor = Armor #Integer. Damage Done Affects Armor First. Health Cannot be Damaged When Armor Has Not Broken.
        Animals.AnimalList.append(Animal) #The Animals Class Contains a List of Every Animal.

        #Animal Movement.
        Animal.MovementTypes = MovementTypes #Dictionary of String Movement Types For This Animal Mapped to Integer Movement Radii.

        #Animal Attacks/Abilities.
        Animal.AttackTypes = AttackTypes #{AttackType: Damage, AttackType: Damage}. {ClassObject: Damage}.
        Animal.AbilityTypes = AbilityTypes #{Condition: AbilityObjects}. "None" is Active at All Times.

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
        AttackTypes.AttackTypeList.append(AttackType) #The AttackTypes Class Contains a List of Every AttackType.

#Class For Every Ability Type in The Game.
class AbilityTypes:

    AbilityTypeList = [] #List of Every AbilityType.

    #Define an Ability Type Object.
    def __init__(AbilityType, AbilityName, SubEffects = []):

        AbilityType.AbilityName = AbilityName #String Name of The Ability. Unique.
        AbilityType.SubEffects = SubEffects #List of String Effects From This Ability.
        AbilityTypes.AbilityTypeList.append(AbilityType) #The AbilityTypes Class Contains a List of Every AbilityType.

    #Define The Effects of All Abilities (by Ability Name).
    def Effects(AbilityType):

        #Check Which Ability This Ability is. Perform The Ability's Effects.
        if AbilityType.AbilityName == "Venom":
            #Venom = Being bitten by the animal causes toxic damage. Max 2.
            pass

        elif AbilityType.AbilityName == "Paralysis":
            #Paralysis = Immobilization of animal. Chance 1-3 turns of no movement (50% chance of paralysis during that time).
            pass

        elif AbilityType.AbilityName == "ColdBlooded":
            #ColdBlooded = Gains 1 HP per turn in sun (not over maximum), -1 HP per turn in wildfire, drought. Decreased speed in blizzard, tundra.
            pass

        elif AbilityType.AbilityName == "Camoflauge":
            #Camoflauge = Unable to be seen easily. Visibility and attackability of animal is within one "space" distance. Enemy player knows that the card exists on the battlefield.
            pass

        elif AbilityType.AbilityName == "Night Vision":
            #Night Vision = Decreased loss of vision in the dark.
            pass

        elif AbilityType.AbilityName == "Flinch":
            #Flinch = Skip turn (Affects Lower Size Animals).
            pass

        elif AbilityType.AbilityName == "Rations":
            #Rations = +1 HP per turn (not over maximum).
            pass

        elif AbilityType.AbilityName == "Grouping":
            #Grouping = Animal is stronger in larger groups. +1 HP for Prey, +1 Attack For Predators. Up to 3.
            pass

        elif AbilityType.AbilityName == "Bleed":
            #Bleed = Lose 1 health per level of bleed per turn. Max 3.
            pass

        elif AbilityType.AbilityName == "Intellect":
            #Intellect = Able to use tools.
            pass

        elif AbilityType.AbilityName == "Scavenger":
            #Scavenger = +1 HP (not over maximum) when resting on a square where an animal has died (one turn use per death on square).
            pass

        elif AbilityType.AbilityName == "Poison":
            #Poison = Touching the animal causes toxic damage. Max 2.
            pass

        elif AbilityType.AbilityName == "Fear":
            #Fear = Subtracts attack from opposing animal (1 per size difference).
            pass

        elif AbilityType.AbilityName == "Exhaustion":
            #Exhaustion = Level 1: Lose half speed, rounded down. Level 2: Paralysis. Max 2.
            pass

#Create The Animals + Attack Types.
def CreateAnimalsAndAttackTypes():

    #Create AbilityTypes: "AbilityName", ["SubEffects"]
    AbilityTypes("Venom")
    AbilityTypes("Paralysis")
    AbilityTypes("ColdBlooded", ["+1 in Wildfire, Drought"])
    AbilityTypes("Camoflauge", ["Reduced", "Removed", "SelfReduced"])
    AbilityTypes("Night Vision", ["SelfReduced"])
    AbilityTypes("Flinch")
    AbilityTypes("Rations")
    AbilityTypes("Grouping")
    AbilityTypes("Bleed")
    AbilityTypes("Intellect")
    AbilityTypes("Scavenger")
    AbilityTypes("Poison")
    AbilityTypes("Fear", ["All", "Larger", "Smaller", "Immune"])
    AbilityTypes("Exhaustion", ["Halved"])


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
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[0]: (1, AbilityTypes.AbilityTypeList[0], AbilityTypes.AbilityTypeList[1])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[2], AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[13]),
        "Rattle": (AbilityTypes.AbilityTypeList[12].SubEffects[0], AbilityTypes.AbilityTypeList[3].SubEffects[2]),
        "Smell": (AbilityTypes.AbilityTypeList[4])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Slither": 3
    }

    Animals("Rattlesnake", "Legendary", 10, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Camel (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[1]: (2, AbilityTypes.AbilityTypeList[5])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[6], AbilityTypes.AbilityTypeList[13])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2
    }

    Animals("Camel", "Rare", 20, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Scorpion (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[2]: (1, AbilityTypes.AbilityTypeList[0])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[2], AbilityTypes.AbilityTypeList[13]),
        "OnSight": (AbilityTypes.AbilityTypeList[12].SubEffects[1])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2
    }

    Animals("Scorpion", "Rare", 8, 1, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Silver Ant (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[0]: tuple([1])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[7], AbilityTypes.AbilityTypeList[2].SubEffects[0], AbilityTypes.AbilityTypeList[13].SubEffects[0], AbilityTypes.AbilityTypeList[10])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 6
    }

    Animals("Silver Ant", "Rare", 5, 2, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Wolf (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[0]: (2, AbilityTypes.AbilityTypeList[8]),
        AttackTypes.AttackTypeList[3]: (1, AbilityTypes.AbilityTypeList[8])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[7], AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[13]),
        "OnSight": (AbilityTypes.AbilityTypeList[12].SubEffects[0]),
        "Smell": (AbilityTypes.AbilityTypeList[3].SubEffects[0])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3
    }

    Animals("Wolf", "Rare", 12, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Grizzly Bear (Legendary).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[0]: (3, AbilityTypes.AbilityTypeList[8]),
        AttackTypes.AttackTypeList[3]: (2, AbilityTypes.AbilityTypeList[8])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[12].SubEffects[3], AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[13]),
        "OnSight": (AbilityTypes.AbilityTypeList[12].SubEffects[0]),
        "Smell": (AbilityTypes.AbilityTypeList[3].SubEffects[0])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3
    }

    Animals("Grizzly Bear", "Legendary", 20, 1, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Black Bear (Epic).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[0]: (2, AbilityTypes.AbilityTypeList[8]),
        AttackTypes.AttackTypeList[3]: (2, AbilityTypes.AbilityTypeList[8])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[13]),
        "Smell": (AbilityTypes.AbilityTypeList[3].SubEffects[0])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3,
        "Climb": 1
    }

    Animals("Black Bear", "Epic", 17, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Deer (Common).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[1]: (1, AbilityTypes.AbilityTypeList[5]),
        AttackTypes.AttackTypeList[4]: (2, AbilityTypes.AbilityTypeList[8])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[13])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3,
        "Jump": 2
    }

    Animals("Deer", "Common", 10, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Rabbit (Common).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[1]: (1, AbilityTypes.AbilityTypeList[5])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[13])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 4,
        "Jump": 2
    }

    Animals("Rabbit", "Common", 6, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Moose (Epic).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[1]: (2, AbilityTypes.AbilityTypeList[5]),
        AttackTypes.AttackTypeList[4]: (3, AbilityTypes.AbilityTypeList[8])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[13])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3,
        "Swim": 2
    }

    Animals("Moose", "Epic", 15, 3, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Eagle (Common).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[3]: tuple([2]),
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[13])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 1,
        "Fly": 4
    }

    Animals("Eagle", "Common", 6, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Hawk (Common).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[3]: tuple([2]),
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[13])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 1,
        "Fly": 3
    }

    Animals("Hawk", "Common", 7, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Shark (Epic).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[0]: (3, AbilityTypes.AbilityTypeList[8]),
        AttackTypes.AttackTypeList[5]: (2, AbilityTypes.AbilityTypeList[5])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[13]),
        "OnSight": (AbilityTypes.AbilityTypeList[12].SubEffects[2])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Swim": 3
    }

    Animals("Shark", "Epic", 14, 4, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Dolphin (Epic).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[5]: (1, AbilityTypes.AbilityTypeList[5])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[9], AbilityTypes.AbilityTypeList[7], AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[13]),
        "Echo Location": (AbilityTypes.AbilityTypeList[3].SubEffects[1])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Swim": 4
    }

    Animals("Dolphin", "Epic", 12, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Orca (Legendary).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[0]: (3, AbilityTypes.AbilityTypeList[8]),
        AttackTypes.AttackTypeList[5]: (3, AbilityTypes.AbilityTypeList[5])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[9], AbilityTypes.AbilityTypeList[7], AbilityTypes.AbilityTypeList[13]),
        "OnSight": (AbilityTypes.AbilityTypeList[12].SubEffects[0]),
        "Echo Location": (AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[3].SubEffects[1])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Swim": 3
    }

    Animals("Orca", "Legendary", 20, 5, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Plankton (Common).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[7], AbilityTypes.AbilityTypeList[6], AbilityTypes.AbilityTypeList[13])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Swim": 1
    }

    Animals("Plankton", "Common", 2, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Octopus (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[6]: tuple([1]),
        AttackTypes.AttackTypeList[7]: (0, AbilityTypes.AbilityTypeList[1])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[9], AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[13])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Swim": 2
    }

    Animals("Octopus", "Rare", 9, 1, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Crab (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[3]: tuple([2])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[4].SubEffects[0], AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[13])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2,
        "Swim": 1
    }

    Animals("Crab", "Rare", 3, 6, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Lion (Legendary).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[0]: (3, AbilityTypes.AbilityTypeList[8]),
        AttackTypes.AttackTypeList[3]: (2, AbilityTypes.AbilityTypeList[8])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[7], AbilityTypes.AbilityTypeList[13]),
        "OnSight": (AbilityTypes.AbilityTypeList[12].SubEffects[0])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3
    }

    Animals("Lion", "Legendary", 16, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Giraffe (Legendary).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[1]: (3, AbilityTypes.AbilityTypeList[5])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[13])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2
    }

    Animals("Giraffe", "Legendary", 25, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Elephant (Legendary).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[8]: (3, AbilityTypes.AbilityTypeList[1]),
        AttackTypes.AttackTypeList[7]: (0, AbilityTypes.AbilityTypeList[1]),
        AttackTypes.AttackTypeList[1]: (2, AbilityTypes.AbilityTypeList[5])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[13])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2
    }

    Animals("Elephant", "Legendary", 20, 4, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Zebra (Common).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[1]: (1, AbilityTypes.AbilityTypeList[5])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[7], AbilityTypes.AbilityTypeList[13])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3
    }

    Animals("Zebra", "Common", 12, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Hyena (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[0]: (2, AbilityTypes.AbilityTypeList[8]),
        AttackTypes.AttackTypeList[3]: (1, AbilityTypes.AbilityTypeList[8])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[7], AbilityTypes.AbilityTypeList[10], AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[13])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3
    }

    Animals("Hyena", "Rare", 12, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Gazelle (Common).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[1]: (1, AbilityTypes.AbilityTypeList[5]),
        AttackTypes.AttackTypeList[4]: (2, AbilityTypes.AbilityTypeList[8])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[7], AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[13])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3,
        "Jump": 2
    }

    Animals("Gazelle", "Common", 10, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Bison (Epic).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[1]: (2, AbilityTypes.AbilityTypeList[5]),
        AttackTypes.AttackTypeList[8]: (3, AbilityTypes.AbilityTypeList[5])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[7], AbilityTypes.AbilityTypeList[13]),
        "Grouping": ("AttackTypes.AttackTypeList[1] : AbilityTypes.AbilityTypeList[1]")
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3
    }

    Animals("Bison", "Epic", 15, 2, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Vulture (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[3]: tuple([2])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[10], AbilityTypes.AbilityTypeList[4].SubEffects[0], AbilityTypes.AbilityTypeList[13])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 1,
        "Fly": 3
    }

    Animals("Vulture", "Rare", 8, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Monkey (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[6]: tuple([1])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[9], AbilityTypes.AbilityTypeList[13])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2,
        "Climb": 2
    }

    Animals("Monkey", "Rare", 9, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Ape (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[6]: tuple([2]),
        AttackTypes.AttackTypeList[7]: (0, AbilityTypes.AbilityTypeList[1])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[9], AbilityTypes.AbilityTypeList[13])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2
    }

    Animals("Ape", "Rare", 13, 1, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Alligator (Epic).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[0]: (3, AbilityTypes.AbilityTypeList[8]),
        AttackTypes.AttackTypeList[9]: (4, AbilityTypes.AbilityTypeList[8]),
        AttackTypes.AttackTypeList[5]: (2, AbilityTypes.AbilityTypeList[5])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[13]),
        "OnSight": (AbilityTypes.AbilityTypeList[12].SubEffects[0])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2,
        "Swim": 2
    }

    Animals("Alligator", "Epic", 17, 6, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Crocodile (Epic).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[0]: (3, AbilityTypes.AbilityTypeList[8]),
        AttackTypes.AttackTypeList[9]: (4, AbilityTypes.AbilityTypeList[8]),
        AttackTypes.AttackTypeList[5]: (2, AbilityTypes.AbilityTypeList[5])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[13]),
        "OnSight": (AbilityTypes.AbilityTypeList[12].SubEffects[0])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2,
        "Swim": 2
    }

    Animals("Crocodile", "Epic", 21, 2, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Poison Frog (Common).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[13]),
        "Hurt": (AbilityTypes.AbilityTypeList[11])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 1,
        "Jump": 2
    }

    Animals("Poison Frog", "Common", 7, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Polar Bear (Legendary).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[0]: (4, AbilityTypes.AbilityTypeList[8]),
        AttackTypes.AttackTypeList[3]: (3, AbilityTypes.AbilityTypeList[8])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[13]),
        "OnSight": (AbilityTypes.AbilityTypeList[12].SubEffects[0])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3,
        "Swim": 3
    }

    Animals("Polar Bear", "Legendary", 20, 5, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Arctic Fox (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[0]: tuple([2]),
        AttackTypes.AttackTypeList[3]: tuple([1])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[13]),
        "Bark": (AbilityTypes.AbilityTypeList[12].SubEffects[2])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2
    }

    Animals("Arctic Fox", "Rare", 8, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Penguin (Common).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[0]: tuple([1])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[13])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 1,
        "Swim": 2
    }

    Animals("Penguin", "Common", 8, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Seal (Common).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[8]: (1, AbilityTypes.AbilityTypeList[1]),
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[13])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Swim": 2
    }

    Animals("Seal", "Common", 12, 1, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.