import numpy as np
from copy import deepcopy

#Class For Every Animal in The Game.
class Animals:

    AnimalList = np.array([], dtype = object) #List of Every Animal.
    InBattle = np.array([], dtype = object) #List of Every Animal in Battle.
    AnimalSizes = ("Tiny", "Small", "Medium", "Large", "Giant")
    AnimalRarities = ("Common", "Rare", "Epic", "Legendary")

    #Define an Animal Object.
    #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.
    def __init__(Animal, AnimalName, Size, PredPrey, Rarity, Player, Health, Armor, AttackTypes, MovementTypes, AbilityTypes):

        #Animal Name/Rarity/Health/Armor.
        Animal.Player = Player #Player ID That is Using This Animal
        Animal.AnimalID = len([OtherAnimal for OtherAnimal in Animals.AnimalList if OtherAnimal.AnimalName.split(" ")[0] == AnimalName]) + 1 #Give a Unique ID to an Animal.
        Animal.AnimalName = f"{AnimalName} {Animal.AnimalID}" #String Name of The Animal.
        Animal.Rarity = Rarity #String Rarity of The Animal. (Common/Rare/Epic/Legendary).
        Animal.PredPrey = PredPrey #String "Predator" or "Prey" Classification of The Animal
        Animal.MaxHealth = Health #Integer. The Maximum Health of an Animal. Reaching 0 Means The Card is Removed From The Battlefield.
        Animal.Health = Health #Integer. The Health of an Animal. Reaching 0 Means The Card is Removed From The Battlefield.
        Animal.Armor = Armor #Integer. Damage Done Affects Armor First. Health Cannot be Damaged When Armor Has Not Broken.
        Animal.MaxArmor = Armor #Integer. Maximum Value For Armor. Damage Done Affects Armor First. Health Cannot be Damaged When Armor Has Not Broken.
        Animal.Size = Size #String Size of The Animal. (Tiny/Small/Medium/Large/Giant).
        Animals.AnimalList = np.append(Animals.AnimalList, Animal) #The Animals Class Contains a List of Every Animal.

        #Animal Movement.
        Animal.MovementTypes = MovementTypes #Dictionary of String Movement Types For This Animal Mapped to Integer Movement Radii.
        Animal.OriginalMovementTypes = deepcopy(MovementTypes) #Dictionary of String Movement Types For This Animal Mapped to Integer Movement Radii.

        #Animal Attacks/Abilities.
        Animal.AttackTypes = AttackTypes #{AttackType: Damage, AttackType: Damage}. {ClassObject: Damage}.
        Animal.AbilityTypes = AbilityTypes #{Condition: AbilityObjects}. "None" is Active at All Times.
        Animal.CurrentAbilities = {
            "Venom": 0, #Level of Venom Currently Applied to The Animal
            "Paralysis": np.array([False, 0], dtype = object), #Whether The Animal is Paralyzed, Number of Turns Paralyzed
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
            "Exhaustion": np.array([0, [False, 0]], dtype = object) #Level of Exhaustion + Exhaustion Paralysis Currently Applied to The Animal
        }

        #Set Defaults to Current Abilities
        for Ability in AbilityTypes["None"]:
            if not(isinstance(Ability, np.ndarray)):
                Ability = np.array([Ability, ""], dtype = object)

            #Animal Has This Ability
            if isinstance(Animal.CurrentAbilities[Ability[0].AbilityName], bool):
                Animal.CurrentAbilities[Ability[0].AbilityName] = True

            #Update's Animal's Default Night Vision
            elif not(isinstance(Animal.CurrentAbilities[Ability[0].AbilityName], np.ndarray)) and Animal.CurrentAbilities[Ability[0].AbilityName] == 1:

                if Ability[1] == "SelfReduced":
                    Animal.CurrentAbilities[Ability[0].AbilityName] = 2

                else:
                    Animal.CurrentAbilities[Ability[0].AbilityName] = 3

            #Update's Animal's Default Camoflauge
            elif not(isinstance(Animal.CurrentAbilities[Ability[0].AbilityName], np.ndarray)) and Animal.CurrentAbilities[Ability[0].AbilityName] == 9999:

                if Ability[1] == "SelfReduced":
                    Animal.CurrentAbilities[Ability[0].AbilityName] = 2

                else:
                    Animal.CurrentAbilities[Ability[0].AbilityName] = 1

        #Save Original Camoflauge, Night Vision, CurrentLocation.
        Animal.OriginalCamoflauge = Animal.CurrentAbilities["Camoflauge"]
        Animal.OriginalNightVision = Animal.CurrentAbilities["Night Vision"]
        Animal.CurrentLocation = np.array([-1, -1], dtype = np.int32) #(X, Y) Coordinates. Integer Numbers After Grid Initialization.

    #Find an Ability in a Dictionary of Animal's Abilities.
    def FindAbility(AbilityName, Dictionary = None, Key = None):

        FoundAbility = None
        Ability = 0
        if Dictionary is not None:
            if Key in Dictionary.keys():
                while FoundAbility == None and Ability in range(Dictionary[Key].shape[0]):
                    #Ignore Ability == 0 When The Dictionary is For AttackTypes
                    if not(isinstance(Dictionary[Key][Ability], int)) and not(isinstance(Dictionary[Key][Ability], np.int32)):
                        if not(isinstance(Dictionary[Key][Ability], np.ndarray)):
                            if Dictionary[Key][Ability].AbilityName == AbilityName:
                                FoundAbility = (Dictionary[Key][Ability], None)

                        else:
                            if Dictionary[Key][Ability][0].AbilityName == AbilityName:
                                FoundAbility = tuple(Dictionary[Key][Ability])

                    Ability += 1

        else:
            while FoundAbility == None and Ability in range(AbilityTypes.AbilityTypeList.shape[0]):
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
        print(f"{Defender} Was Attacked by {Animal} Using The Attack {AttackObject.AttackName}.")
        Animals.AttackEffects(Animal, Defender, AttackObject)

        return Defenders

    #Print The Stats of an Animal. Object Mathod.
    def PrintAnimal(Animal, Tabs = ""):

        print(f"\n{Tabs}{Animal}:")
        print(f"\t{Tabs}Health: {Animal.Health}")
        print(f"\t{Tabs}Armor: {Animal.Armor}")

    #Print The Stats of All Animals. Class Mathod.
    def PrintAllAnimalsInBattle():

        print("\nStatistics of All Animals:")
        for Animal in Animals.InBattle:
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

    AttackTypeList = np.array([], dtype = object) #List of Every AttackType.

    #Define an Attack Type Object.
    def __init__(AttackType, AttackName, AttackRadius, SplashDamage):

        AttackType.AttackName = AttackName  #String Name of The Attack. Unique.
        AttackType.AttackRadius = AttackRadius #Integer. Number of Squares That The Attack Can Reach Without Being Hindered.
        AttackType.SplashDamage = SplashDamage #(Boolean, Damage). Whether or Not The Attack Has Splash Damage, The Damage to Add to Splashed Targets.
        AttackTypes.AttackTypeList = np.append(AttackTypes.AttackTypeList, AttackType) #The AttackTypes Class Contains a List of Every AttackType.

    #Add Damage to All Attacks That an Animal Has
    def AddDamage(Animal, Addition):

        for AttackType in Animal.AttackTypes.keys():
            if Animal.AttackTypes[AttackType].shape[0] > 1:
                Animal.AttackTypes[AttackType] = np.array([Animal.AttackTypes[AttackType][0] + Addition] + list(Animal.AttackTypes[AttackType][1:]), dtype = object)

            else:
                Animal.AttackTypes[AttackType] = np.array([Animal.AttackTypes[AttackType][0] + Addition], dtype = np.int32)

#Class For Every Ability Type in The Game.
class AbilityTypes():

    AbilityTypeList = np.array([], dtype = np.int32) #List of Every AbilityType.

    #Define an Ability Type Object.
    def __init__(AbilityType, AbilityName, AbilityFunction, SubEffects = np.array([], dtype = np.str_)):

        AbilityType.AbilityName = AbilityName #String Name of The Ability. Unique.
        AbilityType.SubEffects = SubEffects #List of String Effects From This Ability.
        AbilityTypes.AbilityTypeList = np.append(AbilityTypes.AbilityTypeList, AbilityType) #The AbilityTypes Class Contains a List of Every AbilityType.
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
                print(f"Venom Damaged {Animal} by {Animal.CurrentAbilities['Venom']}.")
                Animal.CurrentAbilities["Venom"] -= 1 if Animal.CurrentAbilities["Venom"] > 0 else 0
                print(f"Venom in {Animal} is Reversed to Level {Animal.CurrentAbilities['Venom']}.")

            else:
                Animal.CurrentAbilities["Venom"] += 1 if Animal.CurrentAbilities["Venom"] < 2 else 0
                print(f"Venom Level {Animal.CurrentAbilities['Venom']} Applied to {Animal}.")

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
                Animal.CurrentAbilities["Exhaustion"][1] = np.array([False if NewTime == 0 else True, NewTime], dtype = object)
                print(f"{ParalysisObject.SubEffects[0]} Paralysis For {Animal} is in Effect For {Animal.CurrentAbilities['Exhaustion'][1][1]} More Turn{'s' if Animal.CurrentAbilities['Exhaustion'][1][1] != 1 else ''}.")

            else:
                Animal.CurrentAbilities["Exhaustion"][1] = np.array([True, 1], dtype = object)
                print(f"{ParalysisObject.SubEffects[0]} Paralysis Applied to {Animal} For {Animal.CurrentAbilities['Exhaustion'][1][1]} Turn{'s' if Animal.CurrentAbilities['Exhaustion'][1][1] != 1 else ''}.")

        #Not a SubEffect
        else:
            #Set Whether The Animal Has Paralysis Applied to The Animal to True or False. This Cuts Off Movement
            #For The Animal For 1-3 Turns. During This Time, There is a 50% Chance of Paralysis Each Turn.
            if Reverse:
                NewTime = (Animal.CurrentAbilities["Paralysis"][1] - 1) if Animal.CurrentAbilities["Paralysis"][1] > 0 else 0
                Animal.CurrentAbilities["Paralysis"] = np.array([False if NewTime == 0 else True, NewTime], dtype = object)
                print(f"Paralysis For {Animal} is in Effect For {Animal.CurrentAbilities['Paralysis'][1]} More Turn{'s' if Animal.CurrentAbilities['Paralysis'][1] != 1 else ''}.")

            else:
                Animal.CurrentAbilities["Paralysis"] = np.array([True, np.random.randint(1, 4)], dtype = object)
                print(f"Paralysis Applied to {Animal} For {Animal.CurrentAbilities['Paralysis'][1]} Turn{'s' if Animal.CurrentAbilities['Paralysis'][1] != 1 else ''}.")

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
                print(f"{Animal} is Cold Blooded, Gaining 1 Health From The Environmental Condition {SubEffect}.")

        #Not a SubEffect
        else:

            #The Animal Heals One Health Per Turn in The Sun
            if SubEffect == "Sun":
                if Animal.Health < Animal.MaxHealth:
                    Animal.Health += 1
                    print(f"{Animal} is Cold Blooded, Gaining 1 Health From The Environmental Condition {SubEffect}.")

            #The Animal Loses One Health Per Turn in a Wildfire or Drought
            elif SubEffect in ("Wildfire", "Drought"):
                    if Animal.Health > 0:
                        Animal.Health -= 1
                        print(f"{Animal} is Cold Blooded, Losing 1 Health From The Environmental Condition {SubEffect}.")

            elif SubEffect in ("Blizzard", "Tundra"):
                if Reverse:
                    Animal.MovementTypes = deepcopy(Animal.OriginalMovementTypes)
                    print(f"{Animal} is Cold Blooded, Regaining Half Speed For Ending Turn in The Environmental Condition {SubEffect}.")

                else:
                    for MovementType, MovementRadius in Animal.MovementTypes.items():
                        Animal.MovementTypes[MovementType] = MovementRadius // 2
                    print(f"{Animal} is Cold Blooded, Losing Half Speed For Starting Turn in The Environmental Condition {SubEffect}.")

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
                print(f"{Animal}'s Camoflauge is Increased to a Visual Radius of {Animal.CurrentAbilities['Camoflauge']}.")

            else:
                Animal.CurrentAbilities["Camoflauge"] = Animal.CurrentAbilities["Camoflauge"] + 2 if Animal.CurrentAbilities["Camoflauge"] + 2 < 9999 else 9999
                print(f"{Animal}'s Camoflauge is Reduced to a Visual Radius of {Animal.CurrentAbilities['Camoflauge']}.")

        elif SubEffect == CamoflaugeObject.SubEffects[1]: #SubEffect == "Removed"
            #Camoflauge is Removed From This Animal
            if Reverse:
                Animal.CurrentAbilities["Camoflauge"] = Animal.OriginalCamoflauge
                print(f"{Animal}'s Camoflauge is Increased to a Visual Radius of {Animal.CurrentAbilities['Camoflauge']}.")

            else:
                Animal.CurrentAbilities["Camoflauge"] = 9999
                print(f"{Animal}'s Camoflauge is Reduced to a Visual Radius of {Animal.CurrentAbilities['Camoflauge']}.")

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
                print(f"{Animal}'s Night Vision is Increased to a Visual Radius of {Animal.CurrentAbilities['Night Vision']}.")

            else:
                Animal.CurrentAbilities["Night Vision"] -= 1
                print(f"{Animal}'s Night Vision is Decreased to a Visual Radius of {Animal.CurrentAbilities['Night Vision']}.")

        #Not a SubEffect
        else:
            #Animal Increases Animal's Own Night Vision
            if Reverse:
                Animal.CurrentAbilities["Night Vision"] -= 1
                print(f"{Animal}'s Night Vision is Decreased to a Visual Radius of {Animal.CurrentAbilities['Night Vision']}.")

            else:
                Animal.CurrentAbilities["Night Vision"] += 1
                print(f"{Animal}'s Night Vision is Increased to a Visual Radius of {Animal.CurrentAbilities['Night Vision']}.")

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
                print(f"Flinch Removed From {Animal}.")

            else:
                Animal.CurrentAbilities["Flinch"] = True
                print(f"Flinch Applied to {Animal}.")

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
                print(f"{Animal} Used {Animal}'s Rations, Gaining 1 Health.")

    #Apply Grouping to Animal. Assume Conditions Met.
    #Grouping = Animal is Stronger in Larger Groups. The More of The Same Animals on The Battlefield For The Start of
    #Animal's Turn, The More Grouping Bonuses For That Turn. +1 HP For Prey, +1 Attack For Predators. Up to 3.
    def Grouping(GroupingObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        AllBattlefieldAnimalsWithThisType = [Animal2 for Animal2 in Animals.InBattle if Animal2.AnimalName == Animal.AnimalName]
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
                    Animal.AttackTypes[AttackTypes.AttackTypeList[1]][1] = AbilityTypes.AbilityTypeList[5]
                    print(f"{Animal}'s {AttackTypes.AttackTypeList[1].AttackName} Attack Now Has {AbilityTypes.AbilityTypeList[5].AbilityName} Instead of {AbilityTypes.AbilityTypeList[1].AbilityName} After One Group Member Left The Battlefield.")

            else:
                Animal.CurrentAbilities["Grouping"] += 1
                if Animal.CurrentAbilities["Grouping"] == 1:
                    Animal.AttackTypes[AttackTypes.AttackTypeList[1]][1] = AbilityTypes.AbilityTypeList[1]
                    print(f"{Animal}'s {AttackTypes.AttackTypeList[1].AttackName} Attack Now Has {AbilityTypes.AbilityTypeList[1].AbilityName} Instead of {AbilityTypes.AbilityTypeList[5].AbilityName} After One Group Member Joined The Battlefield.")

        #Not a SubEffect
        else:
            if Reverse:
                if Animal.CurrentAbilities["Grouping"] > 0:
                    Animal.CurrentAbilities["Grouping"] -= 1

                    #Reverse +1 Attack For Predators
                    if Animal.PredPrey == "Predator":
                        AttackTypes.AddDamage(Animal, -1)
                        print(f"Being a Predator, {Animal}'s Attack Decreased by 1 After One Group Member Left The Battlefield.")

                    #Reverse +1 HP For Prey
                    else: #Animal.PredPrey == "Prey"
                        Animal.Health -= 1 if Animal.Health > 0 else 0
                        Animal.MaxHealth -= 1
                        print(f"Being a Prey, {Animal}'s Maximum Health (+ Current Health) Decreased by 1 After One Group Member Left The Battlefield.")

            else:
                if Animal.CurrentAbilities["Grouping"] < 3:
                    Animal.CurrentAbilities["Grouping"] += 1

                    #+1 Attack For Predators
                    if Animal.PredPrey == "Predator":
                        AttackTypes.AddDamage(Animal, 1)
                        print(f"Being a Predator, {Animal}'s Attack Increased by 1 After One Group Member Joined The Battlefield.")

                    #+1 HP For Prey
                    else: #Animal.PredPrey == "Prey"
                        Animal.Health += 1
                        Animal.MaxHealth += 1
                        print(f"Being a Prey, {Animal}'s Maximum Health (+ Current Health) Increased by 1 After One Group Member Joined The Battlefield.")

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
                print(f"Bleed Damaged {Animal} by {Animal.CurrentAbilities['Bleed']}.")
                Animal.CurrentAbilities["Bleed"] -= 1 if Animal.CurrentAbilities["Bleed"] > 0 else 0
                print(f"Bleed in {Animal} is Reversed to Level {Animal.CurrentAbilities['Bleed']}.")

            else:
                Animal.CurrentAbilities["Bleed"] += 1 if Animal.CurrentAbilities["Bleed"] < 3 else 0
                print(f"Bleed Level {Animal.CurrentAbilities['Bleed']} Applied to {Animal}.")

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
        if SubEffect in IntellectObject.SubEffects:
            pass #SubEffects do Not Exist For Intellect

        #Not a SubEffect
        else:
            if SubEffect == "Forest":
                #Axe
                if Reverse:
                    #Reverse +1 Attack
                    AttackTypes.AddDamage(Animal, -1)
                    print(f"{Animal}'s Attack Reverses in The {SubEffect}, Removing 1 Attack.")

                    #Reverse Can Cut Trees
                    del Animal.AbilityTypes["Cut Trees"]
                    print(f"{Animal} Can no Longer Cut Trees.")

                else:
                    #+1 Attack
                    AttackTypes.AddDamage(Animal, 1)
                    print(f"{Animal}'s Intellect Allows For Greater Attack in The {SubEffect}, Gaining 1 Attack.")

                    #Can Cut Trees
                    Animal.AbilityTypes["Cut Trees"] = np.array([], dtype = np.int32)
                    print(f"{Animal} Can Cut Trees.")

            elif SubEffect == "Grasslands":
                #Sword + Shield
                if Reverse:
                    #Reverse +1 Attack
                    AttackTypes.AddDamage(Animal, -1)
                    print(f"{Animal}'s Attack Reverses in The {SubEffect}, Removing 1 Attack.")

                    #Reverse +1 Armor
                    Animal.Armor -= 1 if Animal.Armor > 0 else 0
                    Animal.MaxArmor -= 1
                    print(f"{Animal}'s Defense Reverses in The {SubEffect}, Removing 1 From Maximum Armor (+ Current Armor).")

                else:
                    #+1 Attack
                    AttackTypes.AddDamage(Animal, 1)
                    print(f"{Animal}'s Intellect Allows For Greater Attack in The {SubEffect}, Gaining 1 Attack.")

                    #+1 Armor
                    Animal.Armor += 1
                    Animal.MaxArmor += 1
                    print(f"{Animal}'s Intellect Allows For Greater Defense in The {SubEffect}, Gaining 1 Maximum Armor (+ Current Armor).")

            elif SubEffect == "Tundra":
                #Boots For +1 Speed in Tundra
                if Reverse:
                    Animals.AddMovement(Animal, -1)
                    print(f"{Animal}'s Travel of The {SubEffect} Comes to a Halt, Removing 1 Speed.")

                else:
                    Animals.AddMovement(Animal, 1)
                    print(f"{Animal}'s Intellect Allows Faster Traversal of The {SubEffect}, Gaining 1 Speed.")

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
            print(f"{Animal}'s Scavenging Gained {Animal} 1 Health.")

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
                print(f"Poison Damaged {Animal} by {Animal.CurrentAbilities['Poison']}.")
                Animal.CurrentAbilities["Poison"] -= 1 if Animal.CurrentAbilities["Poison"] > 0 else 0
                print(f"Poison in {Animal} is Reversed to Level {Animal.CurrentAbilities['Poison']}.")

            else:
                Animal.CurrentAbilities["Poison"] += 1 if Animal.CurrentAbilities["Poison"] < 2 else 0
                print(f"Poison Level {Animal.CurrentAbilities['Poison']} Applied to {Animal}.")

    #Apply Fear to Animal. Assume Conditions Met.
    #Fear = Subtracts Attack From Opposing Animal (1 Per Size Difference).
    def Fear(FearObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        #Assume Animal Seeing Opposing Animals Means The Opposing Animals See Animal
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
            print(f"All Fear Removed From {Animal}.")

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
                    Animal.CurrentAbilities["Fear"] = np.abs(FearLevel)
                    print(f"Fear Level {Animal.CurrentAbilities['Fear']} Applied to {Animal}.")
                    AttackTypes.AddDamage(Animal, min(0, FearLevel))
                    print(f"{Animal}'s Attack is Reduced by {Animal.CurrentAbilities['Fear']}.")

            else:
                print(f"{Animal} is Immune to Fear.")

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
            Animal.CurrentAbilities["Exhaustion"][0] = Animal.CurrentAbilities["Exhaustion"][0] + 1 if Animal.CurrentAbilities["Exhaustion"][0] < 2 else 0
            print(f"Exhaustion Level {Animal.CurrentAbilities['Exhaustion'][0]} Applied to {Animal}.")

        #Level 1 Exhaustion, Speed Drop.
        if Animal.CurrentAbilities["Exhaustion"][0] == 1:
            if Reverse:
                Animal.CurrentAbilities["Exhaustion"][0] = Animal.CurrentAbilities["Exhaustion"][0] - 1
                Animal.MovementTypes = deepcopy(Animal.OriginalMovementTypes)
                print(f"{Animal}'s Exhaustion Decreased to Level {Animal.CurrentAbilities['Exhaustion'][0]}. No Negative Effects.")

            else:
                #Check if This is a SubEffect
                if SubEffect == ExhaustionObject.SubEffects[0]:
                    #Speed Drops by Half, Halved
                    for MovementType, MovementRadius in Animal.MovementTypes.items():
                        Animal.MovementTypes[MovementType] = MovementRadius * 3 // 4
                    print(f"{Animal}'s Movement Reduced to 3/4.")

                #Not a SubEffect
                else:
                    #Speed Drops by Half
                    for MovementType, MovementRadius in Animal.MovementTypes.items():
                        Animal.MovementTypes[MovementType] = MovementRadius // 2
                    print(f"{Animal}'s Movement Reduced to 1/2.")

        #Level 2 Exhaustion, Paralysis.
        elif Animal.CurrentAbilities["Exhaustion"][0] == 2:
            if Reverse:
                Animal.CurrentAbilities["Exhaustion"][0] = Animal.CurrentAbilities["Exhaustion"][0] - 1
                print(f"{Animal}'s Exhaustion Decreased to Level {Animal.CurrentAbilities['Exhaustion'][0]}. Exhaustion Paralysis Removed.")

                #Remove Exhaustion Paralysis
                FoundAbility = Animals.FindAbility("Paralysis")
                while Animal.CurrentAbilities["Exhaustion"][1][0]:
                    FoundAbility.AbilityFunction(FoundAbility, Animal, "Exhaustion", Reverse = True)

            else:
                print("Exhaustion Paralysis Applied.")
                FoundAbility = Animals.FindAbility("Paralysis")
                FoundAbility.AbilityFunction(FoundAbility, Animal, "Exhaustion")

def CreateGrid(Environment):

    #Create a 2D Grid of Size 10 x 10
    GridSize = 10
    MaxNumberObstacles = 3
    Grid2D = np.array([[["", ""] for _ in range(GridSize)] for _ in range(GridSize)], dtype = object) #(Original, Current)
    DeathGrid2D = np.array([[0 for _ in range(GridSize)] for _ in range(GridSize)], dtype = np.int32)
    Trees = np.array(["T", "T"], dtype = object)
    Rocks = np.array(["R", "R"], dtype = object)
    for _ in range(MaxNumberObstacles):

        #Randomly Add up to 3 Obstacles to Grid
        if Environment in ("Forest", "Rainforest"):
            Grid2D[np.random.randint(0, GridSize)][np.random.randint(0, GridSize)] = Trees #Trees

        elif Environment == "Grasslands":
            Grid2D[np.random.randint(0, GridSize)][np.random.randint(0, GridSize)] = Rocks #Rocks

    print(f"Grid Created of Size {GridSize}x{GridSize} With up to {MaxNumberObstacles} Obstacles.")

    return Grid2D, DeathGrid2D

def OnSightFear(Animal, AnimalsSeen):

    '''Animal's Sight Changed, Update Effects.'''
    #Fear (Assuming if Animal Sees Opposing Animals, The Opposing Animals See Animal).
    FoundAbility = Animals.FindAbility("Fear", Animal.AbilityTypes, "OnSight")
    if FoundAbility is not None:
        for OtherAnimal in AnimalsSeen:
            FoundAbility[0].AbilityFunction(FoundAbility[0], OtherAnimal, FoundAbility[1])

#Create Attack Types + Ability Types
def CreateAttackAbilityTypes():

    #Create AbilityTypes: "AbilityName", ["SubEffects"]
    AbilityTypes("Venom", AbilityTypes.Venom)
    AbilityTypes("Paralysis", AbilityTypes.Paralysis, np.array(["Exhaustion"], dtype = np.str_))
    AbilityTypes("ColdBlooded", AbilityTypes.ColdBlooded, np.array(["+1 HP in Wildfire, Drought"], dtype = np.str_))
    AbilityTypes("Camoflauge", AbilityTypes.Camoflauge, np.array(["Reduced", "Removed", "SelfReduced"], dtype = np.str_))
    AbilityTypes("Night Vision", AbilityTypes.NightVision, np.array(["SelfReduced"], dtype = np.str_))
    AbilityTypes("Flinch", AbilityTypes.Flinch)
    AbilityTypes("Rations", AbilityTypes.Rations)
    AbilityTypes("Grouping", AbilityTypes.Grouping, np.array(["AttackTypes.AttackTypeList[1] : AbilityTypes.AbilityTypeList[1]"], dtype = np.str_))
    AbilityTypes("Bleed", AbilityTypes.Bleed)
    AbilityTypes("Intellect", AbilityTypes.Intellect)
    AbilityTypes("Scavenger", AbilityTypes.Scavenger)
    AbilityTypes("Poison", AbilityTypes.Poison)
    AbilityTypes("Fear", AbilityTypes.Fear, np.array(["All", "Larger", "Smaller", "Immune"], dtype = np.str_))
    AbilityTypes("Exhaustion", AbilityTypes.Exhaustion, np.array(["Halved"], dtype = np.str_))

    #Create AttackTypes: "AttackName", AttackRadius, [SplashBool, SplashDamage (Added to Damage, Minimum 1)]
    AttackTypes("Bite", 1, np.array([False, 0], dtype = object))
    AttackTypes("Stomp", 1, np.array([False, 0], dtype = object))
    AttackTypes("Tail Strike", 1, np.array([False, 0], dtype = object))
    AttackTypes("Claw", 1, np.array([True, -1], dtype = object))
    AttackTypes("Horns", 2, np.array([True, -1], dtype = object))
    AttackTypes("Tail Slam", 2, np.array([True, -1], dtype = object))
    AttackTypes("Punch", 1, np.array([False, 0], dtype = object))
    AttackTypes("Grab", 1, np.array([False, 0], dtype = object))
    AttackTypes("Body Slam", 2, np.array([True, 0], dtype = object))
    AttackTypes("Bite Spin", 1, np.array([False, 0], dtype = object))

#Initialize an Animal Deck
def ChooseAnimals(Player, MaxDeckSize):

    AnimalDeck = {
        "Rattlesnake": 0,
        "Camel": 0,
        "Scorpion": 0,
        "Silver Ant": 0,
        "Wolf": 0,
        "Grizzly Bear": 0,
        "Black Bear": 0,
        "Deer": 0,
        "Rabbit": 0,
        "Moose": 0,
        "Eagle": 0,
        "Hawk": 0,
        "Shark": 0,
        "Dolphin": 0,
        "Orca": 0,
        "Plankton": 0,
        "Octopus": 0,
        "Crab": 0,
        "Lion": 0,
        "Giraffe": 0,
        "Elephant": 0,
        "Zebra": 0,
        "Hyena": 0,
        "Gazelle": 0,
        "Bison": 0,
        "Vulture": 0,
        "Monkey": 0,
        "Ape": 0,
        "Alligator": 0,
        "Crocodile": 0,
        "Poison Frog": 0,
        "Polar Bear": 0,
        "Arctic Fox": 0,
        "Penguin": 0,
        "Seal": 0
    }

    #Choose How Many of What Animals Get Added to The Player's Deck
    DeckSize = 0

    #Show The Player What Animals Could be Added to The Deck
    print(f"\nPlayer {Player}'s Deck is of Size {MaxDeckSize}.")
    print("Animals to Choose From:")
    print(list(AnimalDeck.keys()))

    #Assume Animal Rarities Have no Effect Currently
    while DeckSize < MaxDeckSize:

        #Add a Number of Animals That Player Desires
        Animal = input(f"Which Animal Would Player {Player} Like to Add to Player {Player}'s Deck? ")

        #Check That The Player Desires a Valid Animal
        if Animal in AnimalDeck.keys():
            AddAnimal = int(input(f"How Many of {Animal} Does Player {Player} Desire? "))

            #Ensure The Added Animal Count is Less Than The Maximum
            if DeckSize + AddAnimal > MaxDeckSize:
                AddAnimal = MaxDeckSize - DeckSize

            #Add The Number of Animals
            if AnimalDeck[Animal] < AddAnimal:
                AddAnimal -= AnimalDeck[Animal]
                AnimalDeck[Animal] += AddAnimal

            #Not Adding Any Animals
            else:
                AddAnimal = 0

            DeckSize += AddAnimal

    print(f"Player {Player} Animal Deck Initialized With {DeckSize} Animal Cards.")

    return AnimalDeck

#Create Decks of Animals.
def CreateAnimalDeck(Player, MaxDeckSize): #{AnimalDeck}, Player

    AnimalDeck = ChooseAnimals(Player, MaxDeckSize)

    for _ in range(AnimalDeck["Rattlesnake"]):

        #Create Rattlesnake (Legendary).
        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[0]: np.array([1, AbilityTypes.AbilityTypeList[0], AbilityTypes.AbilityTypeList[1]], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[2], AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[13]], dtype = object),
            "Rattle": np.array([np.array([AbilityTypes.AbilityTypeList[12], AbilityTypes.AbilityTypeList[12].SubEffects[0]], dtype = object), np.array([AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[3].SubEffects[2]], dtype = object)], dtype = object),
            "Smell": np.array([AbilityTypes.AbilityTypeList[4]], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Slither": 3
        }

        Animals("Rattlesnake", "Small", "Predator", "Legendary", Player, 10, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Camel (Rare).
    for _ in range(AnimalDeck["Camel"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[1]: np.array([2, AbilityTypes.AbilityTypeList[5]], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[6], AbilityTypes.AbilityTypeList[13]], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 2
        }

        Animals("Camel", "Large", "Prey", "Rare", Player, 20, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Scorpion (Rare).
    for _ in range(AnimalDeck["Scorpion"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[2]: np.array([1, AbilityTypes.AbilityTypeList[0]], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[2], AbilityTypes.AbilityTypeList[13]], dtype = object),
            "OnSight": np.array([np.array([AbilityTypes.AbilityTypeList[12], AbilityTypes.AbilityTypeList[12].SubEffects[1]], dtype = object)], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 2
        }

        Animals("Scorpion", "Small", "Predator", "Rare", Player, 8, 1, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Silver Ant (Rare).
    for _ in range(AnimalDeck["Silver Ant"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[0]: np.array([1], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[7], np.array([AbilityTypes.AbilityTypeList[2], AbilityTypes.AbilityTypeList[2].SubEffects[0]], dtype = object), np.array([AbilityTypes.AbilityTypeList[13], AbilityTypes.AbilityTypeList[13].SubEffects[0]], dtype = object), AbilityTypes.AbilityTypeList[10]], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 6
        }

        Animals("Silver Ant", "Tiny", "Prey", "Rare", Player, 5, 2, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Wolf (Rare).
    for _ in range(AnimalDeck["Wolf"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[0]: np.array([2, AbilityTypes.AbilityTypeList[8]], dtype = object),
            AttackTypes.AttackTypeList[3]: np.array([1, AbilityTypes.AbilityTypeList[8]], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[7], AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[13]], dtype = object),
            "OnSight": np.array([np.array([AbilityTypes.AbilityTypeList[12], AbilityTypes.AbilityTypeList[12].SubEffects[0]], dtype = object)], dtype = object),
            "Smell": np.array([np.array([AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[3].SubEffects[0]], dtype = object)], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 3
        }

        Animals("Wolf", "Medium", "Predator", "Rare", Player, 12, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Grizzly Bear (Legendary).
    for _ in range(AnimalDeck["Grizzly Bear"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[0]: np.array([3, AbilityTypes.AbilityTypeList[8]], dtype = object),
            AttackTypes.AttackTypeList[3]: np.array([2, AbilityTypes.AbilityTypeList[8]], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([np.array([AbilityTypes.AbilityTypeList[12], AbilityTypes.AbilityTypeList[12].SubEffects[3]], dtype = object), AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[13]], dtype = object),
            "OnSight": np.array([np.array([AbilityTypes.AbilityTypeList[12], AbilityTypes.AbilityTypeList[12].SubEffects[0]], dtype = object)], dtype = object),
            "Smell": np.array([np.array([AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[3].SubEffects[0]], dtype = object)], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 3
        }

        Animals("Grizzly Bear", "Large", "Predator", "Legendary", Player, 20, 1, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Black Bear (Epic).
    for _ in range(AnimalDeck["Black Bear"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[0]: np.array([2, AbilityTypes.AbilityTypeList[8]], dtype = object),
            AttackTypes.AttackTypeList[3]: np.array([2, AbilityTypes.AbilityTypeList[8]], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[13]], dtype = object),
            "Smell": np.array([np.array([AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[3].SubEffects[0]], dtype = object)], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 3,
            "Climb": 1
        }

        Animals("Black Bear", "Large", "Predator", "Epic", Player, 17, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Deer (Common).
    for _ in range(AnimalDeck["Deer"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[1]: np.array([1, AbilityTypes.AbilityTypeList[5]], dtype = object),
            AttackTypes.AttackTypeList[4]: np.array([2, AbilityTypes.AbilityTypeList[8]], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[13]], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 3,
            "Jump": 2
        }

        Animals("Deer", "Medium", "Prey", "Common", Player, 10, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Rabbit (Common).
    for _ in range(AnimalDeck["Rabbit"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[1]: np.array([1, AbilityTypes.AbilityTypeList[5]], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[13]], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 4,
            "Jump": 2
        }

        Animals("Rabbit", "Small", "Prey", "Common", Player, 6, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Moose (Epic).
    for _ in range(AnimalDeck["Moose"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[1]: np.array([2, AbilityTypes.AbilityTypeList[5]], dtype = object),
            AttackTypes.AttackTypeList[4]: np.array([3, AbilityTypes.AbilityTypeList[8]], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[13]], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 3,
            "Swim": 2
        }

        Animals("Moose", "Large", "Prey", "Epic", Player, 15, 3, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Eagle (Common).
    for _ in range(AnimalDeck["Eagle"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[3]: np.array([2], dtype = object),
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[13]], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 1,
            "Fly": 4
        }

        Animals("Eagle", "Medium", "Predator", "Common", Player, 6, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Hawk (Common).
    for _ in range(AnimalDeck["Hawk"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[3]: np.array([2], dtype = object),
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[13]], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 1,
            "Fly": 3
        }

        Animals("Hawk", "Medium", "Predator", "Common", Player, 7, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Shark (Epic).
    for _ in range(AnimalDeck["Shark"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[0]: np.array([3, AbilityTypes.AbilityTypeList[8]], dtype = object),
            AttackTypes.AttackTypeList[5]: np.array([2, AbilityTypes.AbilityTypeList[5]], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[13]], dtype = object),
            "OnSight": np.array([np.array([AbilityTypes.AbilityTypeList[12], AbilityTypes.AbilityTypeList[12].SubEffects[2]], dtype = object)], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Swim": 3
        }

        Animals("Shark", "Large", "Predator", "Epic", Player, 14, 4, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Dolphin (Epic).
    for _ in range(AnimalDeck["Dolphin"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[5]: np.array([1, AbilityTypes.AbilityTypeList[5]], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[9], AbilityTypes.AbilityTypeList[7], AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[13]], dtype = object),
            "Echo Location": np.array([np.array([AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[3].SubEffects[1]], dtype = object)], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Swim": 4
        }

        Animals("Dolphin", "Medium", "Prey", "Epic", Player, 12, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Orca (Legendary).
    for _ in range(AnimalDeck["Orca"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[0]: np.array([3, AbilityTypes.AbilityTypeList[8]], dtype = object),
            AttackTypes.AttackTypeList[5]: np.array([3, AbilityTypes.AbilityTypeList[5]], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[9], AbilityTypes.AbilityTypeList[7], AbilityTypes.AbilityTypeList[13]], dtype = object),
            "OnSight": np.array([np.array([AbilityTypes.AbilityTypeList[12], AbilityTypes.AbilityTypeList[12].SubEffects[0]], dtype = object)], dtype = object),
            "Echo Location": np.array([AbilityTypes.AbilityTypeList[4], np.array([AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[3].SubEffects[1]], dtype = object)], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Swim": 3
        }

        Animals("Orca", "Large", "Predator", "Legendary", Player, 20, 5, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Plankton (Common).
    for _ in range(AnimalDeck["Plankton"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[7], AbilityTypes.AbilityTypeList[6], AbilityTypes.AbilityTypeList[13]], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Swim": 1
        }

        Animals("Plankton", "Tiny", "Prey", "Common", Player, 2, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Octopus (Rare).
    for _ in range(AnimalDeck["Octopus"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[6]: np.array([1], dtype = object),
            AttackTypes.AttackTypeList[7]: np.array([0, AbilityTypes.AbilityTypeList[1]], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[9], AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[13]], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Swim": 2
        }

        Animals("Octopus", "Small", "Prey", "Rare", Player, 9, 1, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Crab (Rare).
    for _ in range(AnimalDeck["Crab"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[3]: np.array([2], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([np.array([AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[4].SubEffects[0]], dtype = object), AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[13]], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 2,
            "Swim": 1
        }

        Animals("Crab", "Small", "Prey", "Rare", Player, 3, 6, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Lion (Legendary).
    for _ in range(AnimalDeck["Lion"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[0]: np.array([3, AbilityTypes.AbilityTypeList[8]], dtype = object),
            AttackTypes.AttackTypeList[3]: np.array([2, AbilityTypes.AbilityTypeList[8]], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[7], AbilityTypes.AbilityTypeList[13]], dtype = object),
            "OnSight": np.array([np.array([AbilityTypes.AbilityTypeList[12], AbilityTypes.AbilityTypeList[12].SubEffects[0]], dtype = object)], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 3
        }

        Animals("Lion", "Medium", "Predator", "Legendary", Player, 16, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Giraffe (Legendary).
    for _ in range(AnimalDeck["Giraffe"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[1]: np.array([3, AbilityTypes.AbilityTypeList[5]], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[13]], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 2
        }

        Animals("Giraffe", "Giant", "Prey", "Legendary", Player, 25, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Elephant (Legendary).
    for _ in range(AnimalDeck["Elephant"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[8]: np.array([3, AbilityTypes.AbilityTypeList[1]], dtype = object),
            AttackTypes.AttackTypeList[7]: np.array([0, AbilityTypes.AbilityTypeList[1]], dtype = object),
            AttackTypes.AttackTypeList[1]: np.array([2, AbilityTypes.AbilityTypeList[5]], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[13]], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 2
        }

        Animals("Elephant", "Giant", "Prey", "Legendary", Player, 20, 4, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Zebra (Common).
    for _ in range(AnimalDeck["Zebra"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[1]: np.array([1, AbilityTypes.AbilityTypeList[5]], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[7], AbilityTypes.AbilityTypeList[13]], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 3
        }

        Animals("Zebra", "Medium", "Prey", "Common", Player, 12, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Hyena (Rare).
    for _ in range(AnimalDeck["Hyena"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[0]: np.array([2, AbilityTypes.AbilityTypeList[8]], dtype = object),
            AttackTypes.AttackTypeList[3]: np.array([1, AbilityTypes.AbilityTypeList[8]], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[7], AbilityTypes.AbilityTypeList[10], AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[13]], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 3
        }

        Animals("Hyena", "Medium", "Predator", "Rare", Player, 12, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Gazelle (Common).
    for _ in range(AnimalDeck["Gazelle"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[1]: np.array([1, AbilityTypes.AbilityTypeList[5]], dtype = object),
            AttackTypes.AttackTypeList[4]: np.array([2, AbilityTypes.AbilityTypeList[8]], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[7], AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[13]], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 3,
            "Jump": 2
        }

        Animals("Gazelle", "Medium", "Prey", "Common", Player, 10, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Bison (Epic).
    for _ in range(AnimalDeck["Bison"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[1]: np.array([2, AbilityTypes.AbilityTypeList[5]], dtype = object),
            AttackTypes.AttackTypeList[8]: np.array([3, AbilityTypes.AbilityTypeList[5]], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([np.array([AbilityTypes.AbilityTypeList[7], AbilityTypes.AbilityTypeList[7].SubEffects[0]], dtype = object), AbilityTypes.AbilityTypeList[13]], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 3
        }

        Animals("Bison", "Large", "Prey", "Epic", Player, 15, 2, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Vulture (Rare).
    for _ in range(AnimalDeck["Vulture"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[3]: np.array([2], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[10], np.array([AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[4].SubEffects[0]], dtype = object), AbilityTypes.AbilityTypeList[13]], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 1,
            "Fly": 3
        }

        Animals("Vulture", "Medium", "Prey", "Rare", Player, 8, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Monkey (Rare).
    for _ in range(AnimalDeck["Monkey"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[6]: np.array([1], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[9], AbilityTypes.AbilityTypeList[13]], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 2,
            "Climb": 2
        }

        Animals("Monkey", "Medium", "Prey", "Rare", Player, 9, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Ape (Rare).
    for _ in range(AnimalDeck["Ape"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[6]: np.array([2], dtype = object),
            AttackTypes.AttackTypeList[7]: np.array([0, AbilityTypes.AbilityTypeList[1]], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[9], AbilityTypes.AbilityTypeList[13]], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 2
        }

        Animals("Ape", "Large", "Predator", "Rare", Player, 13, 1, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Alligator (Epic).
    for _ in range(AnimalDeck["Alligator"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[0]: np.array([3, AbilityTypes.AbilityTypeList[8]], dtype = object),
            AttackTypes.AttackTypeList[9]: np.array([4, AbilityTypes.AbilityTypeList[8]], dtype = object),
            AttackTypes.AttackTypeList[5]: np.array([2, AbilityTypes.AbilityTypeList[5]], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[13]], dtype = object),
            "OnSight": np.array([np.array([AbilityTypes.AbilityTypeList[12], AbilityTypes.AbilityTypeList[12].SubEffects[0]], dtype = object)], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 2,
            "Swim": 2
        }

        Animals("Alligator", "Medium", "Predator", "Epic", Player, 17, 6, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Crocodile (Epic).
    for _ in range(AnimalDeck["Crocodile"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[0]: np.array([3, AbilityTypes.AbilityTypeList[8]], dtype = object),
            AttackTypes.AttackTypeList[9]: np.array([4, AbilityTypes.AbilityTypeList[8]], dtype = object),
            AttackTypes.AttackTypeList[5]: np.array([2, AbilityTypes.AbilityTypeList[5]], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[13]], dtype = object),
            "OnSight": np.array([np.array([AbilityTypes.AbilityTypeList[12], AbilityTypes.AbilityTypeList[12].SubEffects[0]], dtype = object)], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 2,
            "Swim": 2
        }

        Animals("Crocodile", "Medium", "Predator", "Epic", Player, 21, 2, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Poison Frog (Common).
    for _ in range(AnimalDeck["Poison Frog"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[13]], dtype = object),
            "Hurt": np.array([AbilityTypes.AbilityTypeList[11]], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 1,
            "Jump": 2
        }

        Animals("Poison Frog", "Small", "Prey", "Common", Player, 7, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Polar Bear (Legendary).
    for _ in range(AnimalDeck["Polar Bear"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[0]: np.array([4, AbilityTypes.AbilityTypeList[8]], dtype = object),
            AttackTypes.AttackTypeList[3]: np.array([3, AbilityTypes.AbilityTypeList[8]], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[13]], dtype = object),
            "OnSight": np.array([np.array([AbilityTypes.AbilityTypeList[12], AbilityTypes.AbilityTypeList[12].SubEffects[0]], dtype = object)], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 3,
            "Swim": 3
        }

        Animals("Polar Bear", "Large", "Predator", "Legendary", Player, 20, 5, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Arctic Fox (Rare).
    for _ in range(AnimalDeck["Arctic Fox"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[0]: np.array([2], dtype = object),
            AttackTypes.AttackTypeList[3]: np.array([1], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[13]], dtype = object),
            "Bark": np.array([np.array([AbilityTypes.AbilityTypeList[12], AbilityTypes.AbilityTypeList[12].SubEffects[2]], dtype = object)], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 2
        }

        Animals("Arctic Fox", "Medium", "Predator", "Rare", Player, 8, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Penguin (Common).
    for _ in range(AnimalDeck["Penguin"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[0]: np.array([1], dtype = object)
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[13]], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Walk": 1,
            "Swim": 2
        }

        Animals("Penguin", "Medium", "Prey", "Common", Player, 8, 0, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.


    #Create Seal (Common).
    for _ in range(AnimalDeck["Seal"]):

        AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
            AttackTypes.AttackTypeList[8]: np.array([1, AbilityTypes.AbilityTypeList[1]], dtype = object),
        }

        AnimalAbilities = { #"Activation": (AbilityType Objects)
            "None": np.array([AbilityTypes.AbilityTypeList[4], AbilityTypes.AbilityTypeList[3], AbilityTypes.AbilityTypeList[13]], dtype = object)
        }

        AnimalMovements = { #"MovementType": MovementRadius
            "Swim": 2
        }

        Animals("Seal", "Medium", "Prey", "Common", Player, 12, 1, AnimalAttacks, AnimalMovements, AnimalAbilities) #"AnimalName", "Size", "PredPrey", "Rarity", Player, Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.