import random as r
from copy import deepcopy

#Class For Every Animal in The Game.
class Animals:

    AnimalList = [] #List of Every Animal.
    AnimalSizes = ["Tiny", "Small", "Medium", "Large", "Giant"]

    #Define an Animal Object.
    #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.
    def __init__(Animal, AnimalName, Size, PredPrey, Rarity, Health, Armor, AttackTypes, MovementTypes, AbilityTypes):

        #Animal Name/Rarity/Health/Armor.
        Animal.AnimalName = AnimalName #String Name of The Animal.
        Animal.AnimalID = len([Animal2 for Animal2 in Animals.AnimalList if Animal2.AnimalName == AnimalName]) + 1 #Give a Unique ID to an Animal.
        Animal.Rarity = Rarity #String Rarity of The Animal. (Common/Rare/Epic/Legendary).
        Animal.PredPrey = PredPrey #String "Predator" or "Prey" Classification of The Animal
        Animal.MaxHealth = Health #Integer. The Maximum Health of an Animal. Reaching 0 Means The Card is Removed From The Battlefield.
        Animal.Health = Health #Integer. The Health of an Animal. Reaching 0 Means The Card is Removed From The Battlefield.
        Animal.Armor = Armor #Integer. Damage Done Affects Armor First. Health Cannot be Damaged When Armor Has Not Broken.
        Animal.MaxArmor = Armor #Integer. Maximum Value For Armor. Damage Done Affects Armor First. Health Cannot be Damaged When Armor Has Not Broken.
        Animal.Size = Size #String Size of The Animal. (Tiny/Small/Medium/Large/Giant).
        Animals.AnimalList.append(Animal) #The Animals Class Contains a List of Every Animal.

        #Animal Movement.
        Animal.MovementTypes = MovementTypes #Dictionary of String Movement Types For This Animal Mapped to Integer Movement Radii.
        Animal.OriginalMovementTypes = deepcopy(MovementTypes) #Dictionary of String Movement Types For This Animal Mapped to Integer Movement Radii.

        #Animal Attacks/Abilities.
        Animal.AttackTypes = AttackTypes #{AttackType: Damage, AttackType: Damage}. {ClassObject: Damage}.
        Animal.AbilityTypes = AbilityTypes #{Condition: AbilityObjects}. "None" is Active at All Times.
        Animal.CurrentAbilities = {
            "Venom": 0, #Level of Venom Currently Applied to The Animal
            "Paralysis": (False, 0), #Whether The Animal is Paralyzed, Number of Turns Paralyzed
            "ColdBlooded": False, #Whether The Animal Has The Ability ColdBlooded
            "Camoflauge": 9999, #How Many Tiles Away The Animal Can be Seen
            "Night Vision": 1, #How Many Tiles Away The Animal Can See in The Dark
            "Flinch": False, #Whether The Animal is Flinched
            "Rations": False, #Whether The Animal Has The Ability Rations
            "Grouping": 0, #Level of Grouping Currently Applied to The Animal
            "Bleed": 0, #Level of Bleed Currently Applied to The Animal
            "Intellect": False, #Whether The Animal Has The Ability Intellect
            "Scavenger": False, #Whether The Animal Has The Ability Scavenger
            "Poison": 0, #Level of Poison Currently Applied to The Animal
            "Fear": 0, #Level of Fear Currently Applied to The Animal
            "Exhaustion": (0, (False, 0)) #Level of Exhaustion + Exhaustion Paralysis Currently Applied to The Animal
        }

        #Set Defaults to Current Abilities
        for Ability in AbilityTypes["None"]:
            if not(isinstance(Ability, tuple)):
                Ability = (Ability, "")

            #Animal Has This Ability
            if isinstance(Animal.CurrentAbilities[Ability[0].AbilityName], bool):
                Animal.CurrentAbilities[Ability[0].AbilityName] = True

            #Update's Animal's Default Night Vision
            elif Animal.CurrentAbilities[Ability[0].AbilityName] == 1:

                if Ability[1] == "SelfReduced":
                    Animal.CurrentAbilities[Ability[0].AbilityName] = 2

                else:
                    Animal.CurrentAbilities[Ability[0].AbilityName] = 3

            #Update's Animal's Default Camoflauge
            elif Animal.CurrentAbilities[Ability[0].AbilityName] == 9999:

                if Ability[1] == "SelfReduced":
                    Animal.CurrentAbilities[Ability[0].AbilityName] = 2

                else:
                    Animal.CurrentAbilities[Ability[0].AbilityName] = 1

        #Save Original Camoflauge, Night Vision, CurrentLocation.
        Animal.OriginalCamoflauge = Animal.CurrentAbilities["Camoflauge"]
        Animal.OriginalNightVision = Animal.CurrentAbilities["Night Vision"]
        Animal.CurrentLocation = ("", "") #(X, Y) Coordinates. Integer Numbers After Grid Initialization.

    #Find an Ability in a Dictionary of Animal's Abilities.
    def FindAbility(AbilityName, Dictionary = None, Key = None):

        FoundAbility = None
        Ability = 0
        if Dictionary is not None:
            if Key in Dictionary.keys():
                while FoundAbility == None and Ability in range(len(Dictionary[Key])):
                    #Ignore Ability == 0 When The Dictionary is For AttackTypes
                    if not(isinstance(Dictionary[Key][Ability], int)):
                        if not(isinstance(Dictionary[Key][Ability], tuple)):
                            if Dictionary[Key][Ability].AbilityName == AbilityName:
                                FoundAbility = (Dictionary[Key][Ability], None)

                        else:
                            if Dictionary[Key][Ability][0].AbilityName == AbilityName:
                                FoundAbility = Dictionary[Key][Ability]

                    Ability += 1

        else:
            while FoundAbility == None and Ability in range(len(AbilityTypes.AbilityTypeList)):
                if AbilityTypes.AbilityTypeList[Ability].AbilityName == AbilityName:
                    FoundAbility = AbilityTypes.AbilityTypeList[Ability]

                Ability += 1

        #Returns None if Ability is Not Found.
        return FoundAbility

    '''Apply Attack Effects to Those Not Dead.'''
    def AttackEffects(Animal, Defender, AttackObject):

        #Poison
        FoundAbility = Animals.FindAbility("Poison", Defender.AbilityTypes, "Hurt")
        if FoundAbility is not None:
            FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1])

        if Defender.Health > 0:
            #Venom
            FoundAbility = Animals.FindAbility("Venom", Animal.AttackTypes, AttackObject)
            if FoundAbility is not None:
                FoundAbility[0].AbilityFunction(FoundAbility[0], Defender, FoundAbility[1])

            #Paralysis
            FoundAbility = Animals.FindAbility("Paralysis", Animal.AttackTypes, AttackObject)
            if FoundAbility is not None and Animals.AnimalSizes.index(Animal.Size) > Animals.AnimalSizes.index(Defender.Size):
                FoundAbility[0].AbilityFunction(FoundAbility[0], Defender, FoundAbility[1])

            #Flinch
            FoundAbility = Animals.FindAbility("Flinch", Animal.AttackTypes, AttackObject)
            if FoundAbility is not None and Animals.AnimalSizes.index(Animal.Size) > Animals.AnimalSizes.index(Defender.Size):
                FoundAbility[0].AbilityFunction(FoundAbility[0], Defender, FoundAbility[1])

            #Bleed
            FoundAbility = Animals.FindAbility("Bleed", Animal.AttackTypes, AttackObject)
            if FoundAbility is not None:
                FoundAbility[0].AbilityFunction(FoundAbility[0], Defender, FoundAbility[1])

    #Animal Attacks a Defender. Object Method.
    def Attack(Animal, Defender, Damage, Defenders, AttackObject):

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
            if Defender.Health < 0:
                Defender.Health = 0

        '''Apply Attack Effects to Those Not Dead.'''
        print(f"{Defender.AnimalName} Was Attacked by {Animal.AnimalName} Using The Attack {AttackObject.AttackName}.")
        Animals.AttackEffects(Animal, Defender, AttackObject)

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

    #Add Movement to All Movements That an Animal Has
    def AddMovement(Animal, Addition):

        for MovementType, MovementRadius in Animal.MovementTypes.items():
            Animal.MovementTypes[MovementType] = MovementRadius + Addition

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

    #Add Damage to All Attacks That an Animal Has
    def AddDamage(Animal, Addition):

        for AttackType in Animal.AttackTypes.keys():
            if len(Animal.AttackTypes[AttackType]) > 1:
                Animal.AttackTypes[AttackType] = tuple([Animal.AttackTypes[AttackType][0] + Addition] + list(Animal.AttackTypes[AttackType][1:]))

            else:
                Animal.AttackTypes[AttackType] = tuple([Animal.AttackTypes[AttackType][0] + Addition])

#Class For Every Ability Type in The Game.
class AbilityTypes():

    AbilityTypeList = [] #List of Every AbilityType.

    #Define an Ability Type Object.
    def __init__(AbilityType, AbilityName, AbilityFunction, SubEffects = []):

        AbilityType.AbilityName = AbilityName #String Name of The Ability. Unique.
        AbilityType.SubEffects = SubEffects #List of String Effects From This Ability.
        AbilityTypes.AbilityTypeList.append(AbilityType) #The AbilityTypes Class Contains a List of Every AbilityType.
        AbilityType.AbilityFunction = AbilityFunction #Function Pointer For This Ability

    #Apply Venom to Animal. Assume Conditions Met.
    #Venom = Being Bitten by The Animal Causes Toxic Damage. Ignores Armor. Max 2.
    def Venom(VenomObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        if Animal Attacked:
            FoundAbility = Animals.FindAbility("Venom", OtherAnimal.AttackTypes, AttackObject)
            if FoundAbility is not None:
                FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1])

        if Animal's Turn Ending:
            if Animal.CurrentAbilities["Venom"] > 0:
                #The Animal Takes Toxic Damage. Ignores Armor.
                FoundAbility = Animals.FindAbility("Venom")
                FoundAbility.AbilityFunction(FoundAbility, Animal, Reverse = True)
        '''

        #Check if This is a SubEffect
        if SubEffect is not None:
            pass #SubEffects do Not Exist For Venom

        #Not a SubEffect
        else:
            #Change The Level of Venom That The Animal Has Applied to The Animal. This Damages The Animal Over Time.
            #Each Time The Venom Damages The Animal (Equal to Level Damage), The Level of Venom Decreases.
            if Reverse:
                Animal.Health -= Animal.CurrentAbilities["Venom"] if Animal.Health - Animal.CurrentAbilities["Venom"] > 0 else 0
                print(f"Venom Damaged {Animal.AnimalName} by {Animal.CurrentAbilities['Venom']}.")
                Animal.CurrentAbilities["Venom"] -= 1 if Animal.CurrentAbilities["Venom"] > 0 else 0
                print(f"Venom in {Animal.AnimalName} is Reversed to Level {Animal.CurrentAbilities['Venom']}.")

            else:
                Animal.CurrentAbilities["Venom"] += 1 if Animal.CurrentAbilities["Venom"] < 2 else 0
                print(f"Venom Level {Animal.CurrentAbilities['Venom']} Applied to {Animal.AnimalName}.")

    #Apply Paralysis to Animal. Assume Conditions Met.
    #Paralysis = Immobilization of Smaller Animals. Chance 1-3 Turns of no Movement (50% Chance of Attack Paralysis During That Time).
    def Paralysis(ParalysisObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        if Animal Attacked:
            FoundAbility = Animals.FindAbility("Paralysis", OtherAnimal.AttackTypes, AttackObject)
            if FoundAbility is not None and Animals.AnimalSizes.index(OtherAnimal.Size) > Animals.AnimalSizes.index(Animal.Size):
                FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1])

        if Animal's Turn Starting:
            if Animal.CurrentAbilities["Paralysis"][0] or Animal.CurrentAbilities["Exhaustion"][1][0]:
                if r.random() < 0.5:
                    Turn Continues, Cannot Move
                else:
                    Skip Turn

        if Animal's Turn Ending:
            if Animal.CurrentAbilities["Paralysis"][0]:
                FoundAbility = Animals.FindAbility("Paralysis")
                FoundAbility.AbilityFunction(FoundAbility, Animal, Reverse = True)

        Can Also Get Paralysis From Exhaustion Level 2
        '''

        #Check if This is a SubEffect
        if SubEffect == ParalysisObject.SubEffects[0]: #SubEffect == "Exhaustion"
            #Set Whether The Animal Has Paralysis Applied to The Animal to True or False. This Cuts Off Movement
            #For The Animal For 1 Turn. During This Time, There is a 50% Chance of Paralysis Each Turn.
            if Reverse:
                NewTime = (Animal.CurrentAbilities["Exhaustion"][1][1] - 1) if Animal.CurrentAbilities["Exhaustion"][1][1] > 0 else 0
                Animal.CurrentAbilities["Exhaustion"] = (Animal.CurrentAbilities["Exhaustion"][0], (False if NewTime == 0 else True, NewTime))
                print(f"{ParalysisObject.SubEffects[0]} Paralysis For {Animal.AnimalName} is in Effect For {Animal.CurrentAbilities['Exhaustion'][1][1]} More Turn{'s' if Animal.CurrentAbilities['Exhaustion'][1][1] != 1 else ''}.")

            else:
                Animal.CurrentAbilities["Exhaustion"] = (Animal.CurrentAbilities["Exhaustion"][0], (True, 1))
                print(f"{ParalysisObject.SubEffects[0]} Paralysis Applied to {Animal.AnimalName} For {Animal.CurrentAbilities['Exhaustion'][1][1]} Turn{'s' if Animal.CurrentAbilities['Exhaustion'][1][1] != 1 else ''}.")

        #Not a SubEffect
        else:
            #Set Whether The Animal Has Paralysis Applied to The Animal to True or False. This Cuts Off Movement
            #For The Animal For 1-3 Turns. During This Time, There is a 50% Chance of Paralysis Each Turn.
            if Reverse:
                NewTime = (Animal.CurrentAbilities["Paralysis"][1] - 1) if Animal.CurrentAbilities["Paralysis"][1] > 0 else 0
                Animal.CurrentAbilities["Paralysis"] = (False if NewTime == 0 else True, NewTime)
                print(f"Paralysis For {Animal.AnimalName} is in Effect For {Animal.CurrentAbilities['Paralysis'][1]} More Turn{'s' if Animal.CurrentAbilities['Paralysis'][1] != 1 else ''}.")

            else:
                Animal.CurrentAbilities["Paralysis"] = (True, r.randint(1, 3))
                print(f"Paralysis Applied to {Animal.AnimalName} For {Animal.CurrentAbilities['Paralysis'][1]} Turn{'s' if Animal.CurrentAbilities['Paralysis'][1] != 1 else ''}.")

    #Apply ColdBlooded to Animal. Assume Conditions Met.
    #ColdBlooded = Gains 1 HP Per Turn in Sun (Not Over Maximum), -1 HP Per Turn in Wildfire, Drought. Half Speed Rounded Down in Blizzard, Tundra.
    def ColdBlooded(ColdBloodedObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        Weather Takes Effect Over Environment

        if Animal.CurrentAbilities["ColdBlooded"]:
            if Animal's Turn Starting:
                FoundAbility = Animals.FindAbility("ColdBlooded", Animal.AbilityTypes, "None")
                if FoundAbility[1] is not None and Weather in ["Wildfire", "Drought"]:
                    #SubEffect == "+1 in Wildfire, Drought"
                    FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1])

                elif Weather in ["Wildfire", "Drought", "Blizzard", "Sun"]:
                    FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, Weather)

                elif Environment in ["Tundra"]:
                    FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, Environment)

            if Animal's Turn Ending:
                if Weather in ["Blizzard"]:
                    FoundAbility = Animals.FindAbility("ColdBlooded")
                    FoundAbility.AbilityFunction(FoundAbility, Animal, Weather, True)

                elif Environment in ["Tundra"]:
                    FoundAbility = Animals.FindAbility("ColdBlooded")
                    FoundAbility.AbilityFunction(FoundAbility, Animal, Environment, True)
        '''

        #Check if This is a SubEffect
        if SubEffect == ColdBloodedObject.SubEffects[0]: #SubEffect == "+1 HP in Wildfire, Drought"
            #The Animal Heals From Being in a Wildfire or Drought
            if Animal.Health < Animal.MaxHealth:
                Animal.Health += 1
                print(f"{Animal.AnimalName} is Cold Blooded, Gaining 1 Health From The Environmental Condition {SubEffect}.")

        #Not a SubEffect
        else:

            #The Animal Heals One Health Per Turn in The Sun
            if SubEffect == "Sun":
                if Animal.Health < Animal.MaxHealth:
                    Animal.Health += 1
                    print(f"{Animal.AnimalName} is Cold Blooded, Gaining 1 Health From The Environmental Condition {SubEffect}.")

            #The Animal Loses One Health Per Turn in a Wildfire or Drought
            elif SubEffect in ["Wildfire", "Drought"]:
                    if Animal.Health > 0:
                        Animal.Health -= 1
                        print(f"{Animal.AnimalName} is Cold Blooded, Losing 1 Health From The Environmental Condition {SubEffect}.")

            elif SubEffect in ["Blizzard", "Tundra"]:
                if Reverse:
                    Animal.MovementTypes = deepcopy(Animal.OriginalMovementTypes)
                    print(f"{Animal.AnimalName} is Cold Blooded, Regaining Half Speed For Ending Turn in The Environmental Condition {SubEffect}.")

                else:
                    for MovementType, MovementRadius in Animal.MovementTypes.items():
                        Animal.MovementTypes[MovementType] = MovementRadius // 2
                    print(f"{Animal.AnimalName} is Cold Blooded, Losing Half Speed For Starting Turn in The Environmental Condition {SubEffect}.")

    #Apply Camoflauge to Animal. Assume Conditions Met.
    #Camoflauge = Unable to be Seen Easily. Visibility & Attackability of Animal is Within One "Space" Distance. Enemy Player Knows That The Card Exists on The Battlefield. Camoflauge Effects Stack Until 0 or 9999.
    def Camoflauge(CamoflaugeObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        if Animal's Turn Starting:
            if Action == "Rattle" and Animal.CurrentAbilities["Camoflauge"] != 9999:
                FoundAbility = Animals.FindAbility("Camoflauge", Animal.AbilityTypes, Action)
                if FoundAbility is not None:
                    FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1])

            elif Action in ["Smell", "Echo Location"] and OtherAnimal.CurrentAbilities["Camoflauge"] != 9999:
                FoundAbility = Animals.FindAbility("Camoflauge", Animal.AbilityTypes, Action)
                if FoundAbility is not None:
                    FoundAbility[0].AbilityFunction(FoundAbility[0], OtherAnimal, FoundAbility[1])

        if Animal's Turn Ending:
            #Undo Animal's Own Camoflauge Reduction
            if Action == "Rattle" and Animal.CurrentAbilities["Camoflauge"] != Animal.OriginalCamoflauge:
                FoundAbility = Animals.FindAbility("Camoflauge", Animal.AbilityTypes, Action)
                if FoundAbility is not None:
                    FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1], True)

            #Reverse Other Camoflauge Reductions on Animal
            if Animal.CurrentAbilities["Camoflauge"] != Animal.OriginalCamoflauge:
                FoundAbility = Animals.FindAbility("Camoflauge")
                FoundAbility.AbilityFunction(FoundAbility, Animal, "Removed" if Animal.CurrentAbilities["Camoflauge"] == 9999 else "Reduced", True) #Assume Camoflauge Reductions Not at 9999
        '''

        #Check if This is a SubEffect
        if SubEffect == CamoflaugeObject.SubEffects[0] or SubEffect == CamoflaugeObject.SubEffects[2]: #SubEffect == "Reduced" or SubEffect == "SelfReduced"
            #The Animal Reduces Another Animal's Camoflauge or The Animal's Own Camoflauge
            if Reverse:
                Animal.CurrentAbilities["Camoflauge"] = Animal.CurrentAbilities["Camoflauge"] - 2 if Animal.CurrentAbilities["Camoflauge"] - 2 > 0 else 0
                print(f"{Animal.AnimalName}'s Camoflauge is Increased to a Visual Radius of {Animal.CurrentAbilities['Camoflauge']}.")

            else:
                Animal.CurrentAbilities["Camoflauge"] = Animal.CurrentAbilities["Camoflauge"] + 2 if Animal.CurrentAbilities["Camoflauge"] + 2 < 9999 else 9999
                print(f"{Animal.AnimalName}'s Camoflauge is Reduced to a Visual Radius of {Animal.CurrentAbilities['Camoflauge']}.")

        elif SubEffect == CamoflaugeObject.SubEffects[1]: #SubEffect == "Removed"
            #Camoflauge is Removed From This Animal
            if Reverse:
                Animal.CurrentAbilities["Camoflauge"] = Animal.OriginalCamoflauge
                print(f"{Animal.AnimalName}'s Camoflauge is Increased to a Visual Radius of {Animal.CurrentAbilities['Camoflauge']}.")

            else:
                Animal.CurrentAbilities["Camoflauge"] = 9999
                print(f"{Animal.AnimalName}'s Camoflauge is Reduced to a Visual Radius of {Animal.CurrentAbilities['Camoflauge']}.")

        #Not a SubEffect
        else:
            pass #Default Camoflauge Already Applied at Animal Creation

    #Apply Night Vision to Animal. Assume Conditions Met.
    #Night Vision = Decreased Loss of Vision in The Dark.
    def NightVision(NightVisionObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        if DayNight == "Night":
            Less Loss of Vision

        if Animal's Turn Starting:
            if Action in [Smell, Echo Location] and Animal.CurrentAbilities["NightVision"] != 1:
                FoundAbility = Animals.FindAbility("Night Vision", Animal.AbilityTypes, Action)
                if FoundAbility is not None:
                    FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1])

        if Animal's Turn Ending:
            if Animal.CurrentAbilities["Night Vision"] != Animal.OriginalNightVision:
                FoundAbility = Animals.FindAbility("Night Vision")
                FoundAbility[0].AbilityFunction(FoundAbility, Animal, Reverse = True)
        '''

        #Check if This is a SubEffect
        if SubEffect == NightVisionObject.SubEffects[0]: #SubEffect = "SelfReduced"
            #Animal Reduces Animal's Own Night Vision
            if Reverse:
                Animal.CurrentAbilities["Night Vision"] += 1
                print(f"{Animal.AnimalName}'s Night Vision is Increased to a Visual Radius of {Animal.CurrentAbilities['Night Vision']}.")

            else:
                Animal.CurrentAbilities["Night Vision"] -= 1
                print(f"{Animal.AnimalName}'s Night Vision is Decreased to a Visual Radius of {Animal.CurrentAbilities['Night Vision']}.")

        #Not a SubEffect
        else:
            #Animal Increases Animal's Own Night Vision
            if Reverse:
                Animal.CurrentAbilities["Night Vision"] -= 1
                print(f"{Animal.AnimalName}'s Night Vision is Decreased to a Visual Radius of {Animal.CurrentAbilities['Night Vision']}.")

            else:
                Animal.CurrentAbilities["Night Vision"] += 1
                print(f"{Animal.AnimalName}'s Night Vision is Increased to a Visual Radius of {Animal.CurrentAbilities['Night Vision']}.")

    #Apply Flinch to Animal. Assume Conditions Met.
    #Flinch = Skip Turn (Affects Lower Size Animals).
    def Flinch(FlinchObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        if Animal Attacked:
            FoundAbility = Animals.FindAbility("Flinch", OtherAnimal.AttackTypes, AttackObject)
            if FoundAbility is not None and Animals.AnimalSizes.index(OtherAnimal.Size) > Animals.AnimalSizes.index(Animal.Size):
                FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1])

        if Animal.CurrentAbilities["Flinch"]:
            if Animal's Turn Starting:
                Skip Turn

            if Animal's Turn Ending:
                FoundAbility = Animals.FindAbility("Flinch")
                FoundAbility.AbilityFunction(FoundAbility, Animal, Reverse = True)
        '''

        #Check if This is a SubEffect
        if SubEffect is not None:
            pass #SubEffects do Not Exist For Flinch

        #Not a SubEffect
        else:
            if Reverse:
                Animal.CurrentAbilities["Flinch"] = False
                print(f"Flinch Removed From {Animal.AnimalName}.")

            else:
                Animal.CurrentAbilities["Flinch"] = True
                print(f"Flinch Applied to {Animal.AnimalName}.")

    #Apply Rations to Animal. Assume Conditions Met.
    #Rations = +1 HP Per Turn (Not Over Maximum).
    def Rations(RationsObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        if Animal's Turn Starting:
            if Animal.CurrentAbilities["Rations"]:
                FoundAbility = Animals.FindAbility("Rations", Animal.AbilityTypes, "None")
                FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1])
        '''

        #Check if This is a SubEffect
        if SubEffect is not None:
            pass #SubEffects do Not Exist For Rations

        #Not a SubEffect
        else:
            if Animal.Health < Animal.MaxHealth:
                Animal.Health += 1
                print(f"{Animal.AnimalName} Used {Animal.AnimalName}'s Rations, Gaining 1 Health.")

    #Apply Grouping to Animal. Assume Conditions Met.
    #Grouping = Animal is Stronger in Larger Groups. The More of The Same Animals on The Battlefield For The Start of
    #Animal's Turn, The More Grouping Bonuses For That Turn. +1 HP For Prey, +1 Attack For Predators. Up to 3.
    def Grouping(GroupingObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        #Assuming All Animals in AnimalList Are on The Battlefield
        AllBattlefieldAnimalsWithThisType = [Animal2 for Animal2 in Animals.AnimalList if Animal2.AnimalName == Animal.AnimalName]
        if len(AllBattlefieldAnimalsWithThisType) > 1:
            if The Same Animal is Added to The Battlefield:
                for SameAnimal in AllBattlefieldAnimalsWithThisType:
                    FoundAbility = Animals.FindAbility("Grouping", SameAnimal.AbilityTypes, "None")
                    if FoundAbility is not None:
                        FoundAbility[0].AbilityFunction(FoundAbility[0], SameAnimal, FoundAbility[1])

            if The Same Animal is Removed From The Battlefield (Dies):
                for SameAnimal in AllBattlefieldAnimalsWithThisType:
                    FoundAbility = Animals.FindAbility("Grouping", SameAnimal.AbilityTypes, "None")
                    if FoundAbility is not None:
                        FoundAbility[0].AbilityFunction(FoundAbility[0], SameAnimal, FoundAbility[1], Reverse = True)
        '''

        #Check if This is a SubEffect
        if SubEffect == GroupingObject.SubEffects[0]: #SubEffect == "AttackTypes.AttackTypeList[1] : AbilityTypes.AbilityTypeList[1]"
            if Reverse:
                Animal.CurrentAbilities["Grouping"] -= 1
                if Animal.CurrentAbilities["Grouping"] == 0:
                    Animal.AttackTypes[AttackTypes.AttackTypeList[1]] = (Animal.AttackTypes[AttackTypes.AttackTypeList[1]][0], AbilityTypes.AbilityTypeList[5])
                    print(f"{Animal.AnimalName}'s {AttackTypes.AttackTypeList[1].AttackName} Attack Now Has {AbilityTypes.AbilityTypeList[5].AbilityName} Instead of {AbilityTypes.AbilityTypeList[1].AbilityName} After One Group Member Left The Battlefield.")

            else:
                Animal.CurrentAbilities["Grouping"] += 1
                if Animal.CurrentAbilities["Grouping"] == 1:
                    Animal.AttackTypes[AttackTypes.AttackTypeList[1]] = (Animal.AttackTypes[AttackTypes.AttackTypeList[1]][0], AbilityTypes.AbilityTypeList[1])
                    print(f"{Animal.AnimalName}'s {AttackTypes.AttackTypeList[1].AttackName} Attack Now Has {AbilityTypes.AbilityTypeList[1].AbilityName} Instead of {AbilityTypes.AbilityTypeList[5].AbilityName} After One Group Member Joined The Battlefield.")

        #Not a SubEffect
        else:
            if Reverse:
                if Animal.CurrentAbilities["Grouping"] > 0:
                    Animal.CurrentAbilities["Grouping"] -= 1

                    #Reverse +1 Attack For Predators
                    if Animal.PredPrey == "Predator":
                        AttackTypes.AddDamage(Animal, -1)
                        print(f"Being a Predator, {Animal.AnimalName}'s Attack Decreased by 1 After One Group Member Left The Battlefield.")

                    #Reverse +1 HP For Prey
                    else: #Animal.PredPrey == "Prey"
                        Animal.Health -= 1 if Animal.Health > 0 else 0
                        Animal.MaxHealth -= 1
                        print(f"Being a Prey, {Animal.AnimalName}'s Maximum Health (+ Current Health) Decreased by 1 After One Group Member Left The Battlefield.")

            else:
                if Animal.CurrentAbilities["Grouping"] < 3:
                    Animal.CurrentAbilities["Grouping"] += 1

                    #+1 Attack For Predators
                    if Animal.PredPrey == "Predator":
                        AttackTypes.AddDamage(Animal, 1)
                        print(f"Being a Predator, {Animal.AnimalName}'s Attack Increased by 1 After One Group Member Joined The Battlefield.")

                    #+1 HP For Prey
                    else: #Animal.PredPrey == "Prey"
                        Animal.Health += 1
                        Animal.MaxHealth += 1
                        print(f"Being a Prey, {Animal.AnimalName}'s Maximum Health (+ Current Health) Increased by 1 After One Group Member Joined The Battlefield.")

    #Apply Bleed to Animal. Assume Conditions Met.
    #Bleed = Lose 1 Health Ignoring Armor Per Level of Bleed Per Turn. Max 3.
    def Bleed(BleedObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        if Animal Attacked:
            FoundAbility = Animals.FindAbility("Bleed", OtherAnimal.AttackTypes, AttackObject)
            if FoundAbility is not None:
                FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1])

        if Animal's Turn Ending:
            if Animal.CurrentAbilities["Bleed"] > 0:
                FoundAbility = Animals.FindAbility("Bleed")
                if FoundAbility is not None:
                    FoundAbility.AbilityFunction(FoundAbility, Animal, Reverse = True)
        '''

        #Check if This is a SubEffect
        if SubEffect is not None:
            pass #SubEffects do Not Exist For Bleed

        #Not a SubEffect
        else:
            if Reverse:
                Animal.Health -= Animal.CurrentAbilities["Bleed"] if Animal.Health - Animal.CurrentAbilities["Bleed"] > 0 else 0
                print(f"Bleed Damaged {Animal.AnimalName} by {Animal.CurrentAbilities['Bleed']}.")
                Animal.CurrentAbilities["Bleed"] -= 1 if Animal.CurrentAbilities["Bleed"] > 0 else 0
                print(f"Bleed in {Animal.AnimalName} is Reversed to Level {Animal.CurrentAbilities['Bleed']}.")

            else:
                Animal.CurrentAbilities["Bleed"] += 1 if Animal.CurrentAbilities["Bleed"] < 3 else 0
                print(f"Bleed Level {Animal.CurrentAbilities['Bleed']} Applied to {Animal.AnimalName}.")

    #Apply Intellect to Animal. Assume Conditions Met.
    #Intellect = Able to Use Tools. (Axe For +1 Attack & Able to Cut Trees in Forest, Sword + Shield For +1 Attack & +1 Armor in Grasslands,
    #Boots For +1 to All Speeds in Tundra).
    def Intellect(IntellectObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        if Animal's Turn Starts:
            if Animal.CurrentAbilities["Intellect"] and Environment in [Forest, Grasslands, Tundra]:
                FoundAbility = Animals.FindAbility("Intellect", Animal.AbilityTypes, "None")
                FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, Environment)

        if Animal's Turn Ends:
            if Animal.CurrentAbilities["Intellect"] and Environment in [Forest, Grasslands, Tundra]:
                FoundAbility = Animals.FindAbility("Intellect", Animal.AbilityTypes, "None")
                FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, Environment, True)
        '''

        #Check if This is a SubEffect
        if SubEffect not in IntellectObject.SubEffects:
            pass #SubEffects do Not Exist For Intellect

        #Not a SubEffect
        else:
            if SubEffect == "Forest":
                #Axe
                if Reverse:
                    #Reverse +1 Attack
                    AttackTypes.AddDamage(Animal, -1)
                    print(f"{Animal.AnimalName}'s Attack Reverses in The {SubEffect}, Removing 1 Attack.")

                    #Reverse Can Cut Trees
                    del Animal.AbilityTypes["Cut Trees"]
                    print(f"{Animal.AnimalName} Can no Longer Cut Trees.")

                else:
                    #+1 Attack
                    AttackTypes.AddDamage(Animal, 1)
                    print(f"{Animal.AnimalName}'s Intellect Allows For Greater Attack in The {SubEffect}, Gaining 1 Attack.")

                    #Can Cut Trees
                    Animal.AbilityTypes["Cut Trees"] = tuple([])
                    print(f"{Animal.AnimalName} Can Cut Trees.")

            elif SubEffect == "Grasslands":
                #Sword + Shield
                if Reverse:
                    #Reverse +1 Attack
                    AttackTypes.AddDamage(Animal, -1)
                    print(f"{Animal.AnimalName}'s Attack Reverses in The {SubEffect}, Removing 1 Attack.")

                    #Reverse +1 Armor
                    Animal.Armor -= 1 if Animal.Armor > 0 else 0
                    Animal.MaxArmor -= 1
                    print(f"{Animal.AnimalName}'s Defense Reverses in The {SubEffect}, Removing 1 From Maximum Armor (+ Current Armor).")

                else:
                    #+1 Attack
                    AttackTypes.AddDamage(Animal, 1)
                    print(f"{Animal.AnimalName}'s Intellect Allows For Greater Attack in The {SubEffect}, Gaining 1 Attack.")

                    #+1 Armor
                    Animal.Armor += 1
                    Animal.MaxArmor += 1
                    print(f"{Animal.AnimalName}'s Intellect Allows For Greater Defense in The {SubEffect}, Gaining 1 Maximum Armor (+ Current Armor).")

            elif SubEffect == "Tundra":
                #Boots For +1 Speed in Tundra
                if Reverse:
                    Animals.AddMovement(Animal, -1)
                    print(f"{Animal.AnimalName}'s Travel of The {SubEffect} Comes to a Halt, Removing 1 Speed.")

                else:
                    Animals.AddMovement(Animal, 1)
                    print(f"{Animal.AnimalName}'s Intellect Allows Faster Traversal of The {SubEffect}, Gaining 1 Speed.")

    #Apply Scavenger to Animal. Assume Conditions Met.
    #Scavenger = +1 HP (Not Over Maximum) When Ending Turn on a Square Where an Animal Has Died (One Turn Use Per Death on Square).
    def Scavenger(ScavengerObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        Each Square in DeathGrid2D Needs a Count of Deaths on That Square.

        if Animal's Turn Ending:
            if Animal.CurrentAbilities["Scavenger"] and DeathGrid2D[Animal.CurrentLocation[0]][Animal.CurrentLocation[1]] > 0:
                DeathGrid2D[Animal.CurrentLocation[0]][Animal.CurrentLocation[1]] -= 1
                FoundAbility = Animals.FindAbility("Scavenger", Animal.AbilityTypes, "None")
                FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1])
        '''

        #Check if This is a SubEffect
        if SubEffect is not None:
            pass #SubEffects do Not Exist For Scavenger

        #Not a SubEffect
        else:
            Animal.Health += 1 if Animal.Health < Animal.MaxHealth else 0
            print(f"{Animal.AnimalName}'s Scavenging Gained {Animal.AnimalName} 1 Health.")

    #Apply Poison to Animal. Assume Conditions Met.
    #Poison = Touching The Animal Causes Toxic Damage. Max 2.
    def Poison(PoisonObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        if Animal Attacked:
            FoundAbility = Animals.FindAbility("Poison", Animal.AbilityTypes, "Hurt")
            if FoundAbility is not None:
                FoundAbility[0].AbilityFunction(FoundAbility[0], OtherAnimal, FoundAbility[1])

        if Animal's Turn Ending:
            if Animal.CurrentAbilities["Poison"] > 0:
                #The Animal Takes Toxic Damage. Ignores Armor.
                FoundAbility = Animals.FindAbility("Poison")
                FoundAbility.AbilityFunction(FoundAbility, Animal, Reverse = True)
        '''

        #Check if This is a SubEffect
        if SubEffect is not None:
            pass #SubEffects do Not Exist For Poison

        #Not a SubEffect
        else:
            #Change The Level of Poison That The Animal Has Applied to The Animal. This Damages The Animal Over Time.
            #Each Time The Poison Damages The Animal (Equal to Level Damage), The Level of Poison Decreases.
            if Reverse:
                Animal.Health -= Animal.CurrentAbilities["Poison"] if Animal.Health - Animal.CurrentAbilities["Poison"] > 0 else 0
                print(f"Poison Damaged {Animal.AnimalName} by {Animal.CurrentAbilities['Poison']}.")
                Animal.CurrentAbilities["Poison"] -= 1 if Animal.CurrentAbilities["Poison"] > 0 else 0
                print(f"Poison in {Animal.AnimalName} is Reversed to Level {Animal.CurrentAbilities['Poison']}.")

            else:
                Animal.CurrentAbilities["Poison"] += 1 if Animal.CurrentAbilities["Poison"] < 2 else 0
                print(f"Poison Level {Animal.CurrentAbilities['Poison']} Applied to {Animal.AnimalName}.")

    #Apply Fear to Animal. Assume Conditions Met.
    #Fear = Subtracts Attack From Opposing Animal (1 Per Size Difference).
    def Fear(FearObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        #Assume Animal Seeing Other Animals Means The Other Animals See Animal
        if Animal Seen by Other Animals:
            FoundAbility = Animals.FindAbility("Fear", Animal.AbilityTypes, "OnSight")
            if FoundAbility is not None:
                for OtherAnimal in CanSeeAnimal:
                    FoundAbility[0].AbilityFunction(FoundAbility[0], OtherAnimal, FoundAbility[1])

        if Action in [Rattle, Bark]:
            FoundAbility = Animals.FindAbility("Fear", Animal.AbilityTypes, Action)
            if FoundAbility is not None:
                for OtherAnimal in CanSeeAnimal:
                    FoundAbility[0].AbilityFunction(FoundAbility[0], OtherAnimal, FoundAbility[1])

        if Animal's Turn Ending:
            if Animal.CurrentAbilities["Fear"] > 0:
                FoundAbility = Animals.FindAbility("Fear")
                FoundAbility.AbilityFunction(FoundAbility, Animal, Reverse = True)
        '''

        if Reverse:
            #Remove All Fear
            Animal.CurrentAbilities["Fear"] = 0
            print(f"All Fear Removed From {Animal.AnimalName}.")

        else:
            #Fear Immune, Nothing Happens
            FoundAbility = Animals.FindAbility("Fear", Animal.AbilityTypes, "None")
            if FoundAbility is None:

                #Check if This is a SubEffect
                if SubEffect[0] == FearObject.SubEffects[0]:
                    #Two Fear Levels Equally Added to All That See Animal
                    FearLevel = -2

                elif SubEffect[0] == FearObject.SubEffects[1]:
                    #Fear Larger
                    FearLevel = Animals.AnimalSizes.index(SubEffect[1]) - Animals.AnimalSizes.index(Animal.Size)

                elif SubEffect[0] == FearObject.SubEffects[2]:
                    #Fear Smaller
                    FearLevel = Animals.AnimalSizes.index(Animal.Size) - Animals.AnimalSizes.index(SubEffect[1])

                elif SubEffect[0] == FearObject.SubEffects[3]:
                    #Fear Immune, Nothing Happens
                    FearLevel = 0
                    pass

                #Not a SubEffect
                else:
                    FearLevel = 0
                    pass #Default Fear Already Applied at Animal Creation

                #Apply Fear
                if FearLevel != 0:
                    Animal.CurrentAbilities["Fear"] = abs(FearLevel)
                    print(f"Fear Level {Animal.CurrentAbilities['Fear']} Applied to {Animal.AnimalName}.")
                    AttackTypes.AddDamage(Animal, min(0, FearLevel))
                    print(f"{Animal.AnimalName}'s Attack is Reduced by {Animal.CurrentAbilities['Fear']}.")

            else:
                print(f"{Animal.AnimalName} is Immune to Fear.")

    #Apply Exhaustion to Animal. Assume Conditions Met.
    #Exhaustion = Level 1: Lose Half Speed, Rounded Down. Level 2: Paralysis, Cannot Move. Max 2.
    def Exhaustion(ExhaustionObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        if Animal's Turn Ending + Animal Moved 2x Movement This Turn:
            FoundAbility = Animals.FindAbility("Exhaustion", Animal.AbilityTypes, "None")
            FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1])

        elif Animal's Turn Ending + Animal Did Not Move 2x Movement This Turn:
            FoundAbility = Animals.FindAbility("Exhaustion", Animal.AbilityTypes, "None")
            FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1], True)
        '''

        if not(Reverse):
            Animal.CurrentAbilities["Exhaustion"] = (Animal.CurrentAbilities["Exhaustion"][0] + 1 if Animal.CurrentAbilities["Exhaustion"][0] < 2 else 0, Animal.CurrentAbilities["Exhaustion"][1])
            print(f"Exhaustion Level {Animal.CurrentAbilities['Exhaustion'][0]} Applied to {Animal.AnimalName}.")

        #Level 1 Exhaustion, Speed Drop.
        if Animal.CurrentAbilities["Exhaustion"][0] == 1:
            if Reverse:
                Animal.CurrentAbilities["Exhaustion"] = (Animal.CurrentAbilities["Exhaustion"][0] - 1, Animal.CurrentAbilities["Exhaustion"][1])
                Animal.MovementTypes = deepcopy(Animal.OriginalMovementTypes)
                print(f"{Animal.AnimalName}'s Exhaustion Decreased to Level {Animal.CurrentAbilities['Exhaustion'][0]}. No Negative Effects.")

            else:
                #Check if This is a SubEffect
                if SubEffect == ExhaustionObject.SubEffects[0]:
                    #Speed Drops by Half, Halved
                    for MovementType, MovementRadius in Animal.MovementTypes.items():
                        Animal.MovementTypes[MovementType] = MovementRadius * 3 // 4
                    print(f"{Animal.AnimalName}'s Movement Reduced to 3/4.")

                #Not a SubEffect
                else:
                    #Speed Drops by Half
                    for MovementType, MovementRadius in Animal.MovementTypes.items():
                        Animal.MovementTypes[MovementType] = MovementRadius // 2
                    print(f"{Animal.AnimalName}'s Movement Reduced to 1/2.")

        #Level 2 Exhaustion, Paralysis.
        elif Animal.CurrentAbilities["Exhaustion"][0] == 2:
            if Reverse:
                Animal.CurrentAbilities["Exhaustion"] = (Animal.CurrentAbilities["Exhaustion"][0] - 1, Animal.CurrentAbilities["Exhaustion"][1])
                print(f"{Animal.AnimalName}'s Exhaustion Decreased to Level {Animal.CurrentAbilities['Exhaustion'][0]}. Exhaustion Paralysis Removed.")

                #Remove Exhaustion Paralysis
                FoundAbility = Animals.FindAbility("Paralysis")
                while Animal.CurrentAbilities["Exhaustion"][1][0]:
                    FoundAbility.AbilityFunction(FoundAbility, Animal, "Exhaustion", Reverse = True)

            else:
                print("Exhaustion Paralysis Applied.")
                FoundAbility = Animals.FindAbility("Paralysis")
                FoundAbility.AbilityFunction(FoundAbility, Animal, "Exhaustion")

def CreateGrid(Environment):

    #Create a 2D Grid With Animals Placed Diagonally
    Grid2D = [[["", ""] for _ in range(len(Animals.AnimalList))] for _ in range(len(Animals.AnimalList))] #(Original, Current)
    DeathGrid2D = [[0 for _ in range(len(Animals.AnimalList))] for _ in range(len(Animals.AnimalList))]
    for i in range(len(Animals.AnimalList)):
        #Place Animal on Grid
        Grid2D[i][i][1] = Animals.AnimalList[i]
        Animals.AnimalList[i].CurrentLocation = (i, i)

        #Place Some Obstacles Above Animals
        if i % 2 == 1:
            if Environment in ["Forest", "Rainforest"]:
                Grid2D[i - 1][i] = ["T", "T"] #Trees

            elif Environment in ["Grasslands"]:
                Grid2D[i - 1][i] = ["R", "R"] #Rocks

    print("Grid Created.\n")

    return Grid2D, DeathGrid2D

def OnSightFear(Animal, AnimalsSeen):

    '''Animal's Sight Changed, Update Effects.'''
    #Fear (Assuming if Animal Sees Other Animals, The Other Animals See Animal).
    FoundAbility = Animals.FindAbility("Fear", Animal.AbilityTypes, "OnSight")
    if FoundAbility is not None:
        for OtherAnimal in AnimalsSeen:
            FoundAbility[0].AbilityFunction(FoundAbility[0], OtherAnimal, FoundAbility[1])

#Create The Animals + Attack Types.
def CreateAnimalsAndAttackTypes():

    #Create AbilityTypes: "AbilityName", ["SubEffects"]
    AbilityTypes("Venom", AbilityTypes.Venom)
    AbilityTypes("Paralysis", AbilityTypes.Paralysis, ["Exhaustion"])
    AbilityTypes("ColdBlooded", AbilityTypes.ColdBlooded, ["+1 HP in Wildfire, Drought"])
    AbilityTypes("Camoflauge", AbilityTypes.Camoflauge, ["Reduced", "Removed", "SelfReduced"])
    AbilityTypes("Night Vision", AbilityTypes.NightVision, ["SelfReduced"])
    AbilityTypes("Flinch", AbilityTypes.Flinch)
    AbilityTypes("Rations", AbilityTypes.Rations)
    AbilityTypes("Grouping", AbilityTypes.Grouping, ["AttackTypes.AttackTypeList[1] : AbilityTypes.AbilityTypeList[1]"])
    AbilityTypes("Bleed", AbilityTypes.Bleed)
    AbilityTypes("Intellect", AbilityTypes.Intellect)
    AbilityTypes("Scavenger", AbilityTypes.Scavenger)
    AbilityTypes("Poison", AbilityTypes.Poison)
    AbilityTypes("Fear", AbilityTypes.Fear, ["All", "Larger", "Smaller", "Immune"])
    AbilityTypes("Exhaustion", AbilityTypes.Exhaustion, ["Halved"])

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

    for _ in range(2):
        #Create Rattlesnake (Legendary).
        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[0]: (1, AbilityTypes.AbilityTypeList[0], AbilityTypes.AbilityTypeList[1])
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": (AbilityTypes.AbilityTypeList[2], AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[13]),
            "Rattle": ((AbilityTypes.AbilityTypeList[12], AbilityTypes.AbilityTypeList[12].SubEffects[0]), (AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[3].SubEffects[2])),
            "Smell": tuple([AbilityTypes.AbilityTypeList[4]])
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Slither": 3
        }

        Animals("Rattlesnake", "Small", "Predator", "Legendary", 10, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


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

    Animals("Camel", "Large", "Prey", "Rare", 20, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Scorpion (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[2]: (1, AbilityTypes.AbilityTypeList[0])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[2], AbilityTypes.AbilityTypeList[13]),
        "OnSight": tuple([(AbilityTypes.AbilityTypeList[12], AbilityTypes.AbilityTypeList[12].SubEffects[1])])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2
    }

    Animals("Scorpion", "Small", "Predator", "Rare", 8, 1, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Silver Ant (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[0]: tuple([1])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[7], (AbilityTypes.AbilityTypeList[2], AbilityTypes.AbilityTypeList[2].SubEffects[0]), (AbilityTypes.AbilityTypeList[13], AbilityTypes.AbilityTypeList[13].SubEffects[0]), AbilityTypes.AbilityTypeList[10])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 6
    }

    Animals("Silver Ant", "Tiny", "Prey", "Rare", 5, 2, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Wolf (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[0]: (2, AbilityTypes.AbilityTypeList[8]),
        AttackTypes.AttackTypeList[3]: (1, AbilityTypes.AbilityTypeList[8])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[7], AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[13]),
        "OnSight": tuple([(AbilityTypes.AbilityTypeList[12], AbilityTypes.AbilityTypeList[12].SubEffects[0])]),
        "Smell": tuple([(AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[3].SubEffects[0])])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3
    }

    Animals("Wolf", "Medium", "Predator", "Rare", 12, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Grizzly Bear (Legendary).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[0]: (3, AbilityTypes.AbilityTypeList[8]),
        AttackTypes.AttackTypeList[3]: (2, AbilityTypes.AbilityTypeList[8])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": ((AbilityTypes.AbilityTypeList[12], AbilityTypes.AbilityTypeList[12].SubEffects[3]), AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[13]),
        "OnSight": tuple([(AbilityTypes.AbilityTypeList[12], AbilityTypes.AbilityTypeList[12].SubEffects[0])]),
        "Smell": tuple([(AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[3].SubEffects[0])])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3
    }

    Animals("Grizzly Bear", "Large", "Predator", "Legendary", 20, 1, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Black Bear (Epic).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[0]: (2, AbilityTypes.AbilityTypeList[8]),
        AttackTypes.AttackTypeList[3]: (2, AbilityTypes.AbilityTypeList[8])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[13]),
        "Smell": tuple([(AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[3].SubEffects[0])])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3,
        "Climb": 1
    }

    Animals("Black Bear", "Large", "Predator", "Epic", 17, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


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

    Animals("Deer", "Medium", "Prey", "Common", 10, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Rabbit (Common).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[1]: (1, AbilityTypes.AbilityTypeList[5])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": tuple([AbilityTypes.AbilityTypeList[13]])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 4,
        "Jump": 2
    }

    Animals("Rabbit", "Small", "Prey", "Common", 6, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


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

    Animals("Moose", "Large", "Prey", "Epic", 15, 3, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Eagle (Common).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[3]: tuple([2]),
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": tuple([AbilityTypes.AbilityTypeList[13]])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 1,
        "Fly": 4
    }

    Animals("Eagle", "Medium", "Predator", "Common", 6, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Hawk (Common).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[3]: tuple([2]),
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": tuple([AbilityTypes.AbilityTypeList[13]])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 1,
        "Fly": 3
    }

    Animals("Hawk", "Medium", "Predator", "Common", 7, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Shark (Epic).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[0]: (3, AbilityTypes.AbilityTypeList[8]),
        AttackTypes.AttackTypeList[5]: (2, AbilityTypes.AbilityTypeList[5])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[13]),
        "OnSight": tuple([(AbilityTypes.AbilityTypeList[12], AbilityTypes.AbilityTypeList[12].SubEffects[2])])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Swim": 3
    }

    Animals("Shark", "Large", "Predator", "Epic", 14, 4, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Dolphin (Epic).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[5]: (1, AbilityTypes.AbilityTypeList[5])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[9], AbilityTypes.AbilityTypeList[7], AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[13]),
        "Echo Location": tuple([(AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[3].SubEffects[1])])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Swim": 4
    }

    Animals("Dolphin", "Medium", "Prey", "Epic", 12, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    for _ in range(2):
        #Create Orca (Legendary).
        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[0]: (3, AbilityTypes.AbilityTypeList[8]),
            AttackTypes.AttackTypeList[5]: (3, AbilityTypes.AbilityTypeList[5])
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": (AbilityTypes.AbilityTypeList[9], AbilityTypes.AbilityTypeList[7], AbilityTypes.AbilityTypeList[13]),
            "OnSight": tuple([(AbilityTypes.AbilityTypeList[12], AbilityTypes.AbilityTypeList[12].SubEffects[0])]),
            "Echo Location": (AbilityTypes.AbilityTypeList[4], (AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[3].SubEffects[1]))
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Swim": 3
        }

        Animals("Orca", "Large", "Predator", "Legendary", 20, 5, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Plankton (Common).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[7], AbilityTypes.AbilityTypeList[6], AbilityTypes.AbilityTypeList[13])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Swim": 1
    }

    Animals("Plankton", "Tiny", "Prey", "Common", 2, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


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

    Animals("Octopus", "Small", "Prey", "Rare", 9, 1, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Crab (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[3]: tuple([2])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": ((AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[4].SubEffects[0]), AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[13])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2,
        "Swim": 1
    }

    Animals("Crab", "Small", "Prey", "Rare", 3, 6, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Lion (Legendary).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[0]: (3, AbilityTypes.AbilityTypeList[8]),
        AttackTypes.AttackTypeList[3]: (2, AbilityTypes.AbilityTypeList[8])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[7], AbilityTypes.AbilityTypeList[13]),
        "OnSight": tuple([(AbilityTypes.AbilityTypeList[12], AbilityTypes.AbilityTypeList[12].SubEffects[0])])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3
    }

    Animals("Lion", "Medium", "Predator", "Legendary", 16, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Giraffe (Legendary).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[1]: (3, AbilityTypes.AbilityTypeList[5])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": tuple([AbilityTypes.AbilityTypeList[13]])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2
    }

    Animals("Giraffe", "Giant", "Prey", "Legendary", 25, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Elephant (Legendary).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[8]: (3, AbilityTypes.AbilityTypeList[1]),
        AttackTypes.AttackTypeList[7]: (0, AbilityTypes.AbilityTypeList[1]),
        AttackTypes.AttackTypeList[1]: (2, AbilityTypes.AbilityTypeList[5])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": tuple([AbilityTypes.AbilityTypeList[13]])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2
    }

    Animals("Elephant", "Giant", "Prey", "Legendary", 20, 4, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


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

    Animals("Zebra", "Medium", "Prey", "Common", 12, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


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

    Animals("Hyena", "Medium", "Predator", "Rare", 12, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


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

    Animals("Gazelle", "Medium", "Prey", "Common", 10, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    for _ in range(2):
        #Create Bison (Epic).
        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[1]: (2, AbilityTypes.AbilityTypeList[5]),
            AttackTypes.AttackTypeList[8]: (3, AbilityTypes.AbilityTypeList[5])
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": ((AbilityTypes.AbilityTypeList[7], AbilityTypes.AbilityTypeList[7].SubEffects[0]), AbilityTypes.AbilityTypeList[13])
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 3
        }

        Animals("Bison", "Large", "Prey", "Epic", 15, 2, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Vulture (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[3]: tuple([2])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[10], (AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[4].SubEffects[0]), AbilityTypes.AbilityTypeList[13])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 1,
        "Fly": 3
    }

    Animals("Vulture", "Medium", "Prey", "Rare", 8, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


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

    Animals("Monkey", "Medium", "Prey", "Rare", 9, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


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

    Animals("Ape", "Large", "Predator", "Rare", 13, 1, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Alligator (Epic).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[0]: (3, AbilityTypes.AbilityTypeList[8]),
        AttackTypes.AttackTypeList[9]: (4, AbilityTypes.AbilityTypeList[8]),
        AttackTypes.AttackTypeList[5]: (2, AbilityTypes.AbilityTypeList[5])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[13]),
        "OnSight": tuple([(AbilityTypes.AbilityTypeList[12], AbilityTypes.AbilityTypeList[12].SubEffects[0])])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2,
        "Swim": 2
    }

    Animals("Alligator", "Medium", "Predator", "Epic", 17, 6, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Crocodile (Epic).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[0]: (3, AbilityTypes.AbilityTypeList[8]),
        AttackTypes.AttackTypeList[9]: (4, AbilityTypes.AbilityTypeList[8]),
        AttackTypes.AttackTypeList[5]: (2, AbilityTypes.AbilityTypeList[5])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[13]),
        "OnSight": tuple([(AbilityTypes.AbilityTypeList[12], AbilityTypes.AbilityTypeList[12].SubEffects[0])])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2,
        "Swim": 2
    }

    Animals("Crocodile", "Medium", "Predator", "Epic", 21, 2, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Poison Frog (Common).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": tuple([AbilityTypes.AbilityTypeList[13]]),
        "Hurt": tuple([AbilityTypes.AbilityTypeList[11]])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 1,
        "Jump": 2
    }

    Animals("Poison Frog", "Small", "Prey", "Common", 7, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Polar Bear (Legendary).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[0]: (4, AbilityTypes.AbilityTypeList[8]),
        AttackTypes.AttackTypeList[3]: (3, AbilityTypes.AbilityTypeList[8])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[13]),
        "OnSight": tuple([(AbilityTypes.AbilityTypeList[12], AbilityTypes.AbilityTypeList[12].SubEffects[0])])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 3,
        "Swim": 3
    }

    Animals("Polar Bear", "Large", "Predator", "Legendary", 20, 5, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Arctic Fox (Rare).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[0]: tuple([2]),
        AttackTypes.AttackTypeList[3]: tuple([1])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[13]),
        "Bark": tuple([(AbilityTypes.AbilityTypeList[12], AbilityTypes.AbilityTypeList[12].SubEffects[2])])
    }

    AnimalMovements = { #"MovementType": MovementRadius
        "Walk": 2
    }

    Animals("Arctic Fox", "Medium", "Predator", "Rare", 8, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


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

    Animals("Penguin", "Medium", "Prey", "Common", 8, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


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

    Animals("Seal", "Medium", "Prey", "Common", 12, 1, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.

    print("Animals Initialized.")