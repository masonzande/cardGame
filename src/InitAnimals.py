import random as r
from copy import deepcopy

#Class For Every Animal in The Game.
class Animals():

    AnimalList = [] #List of Every Animal.
    AnimalSizes = ["Tiny", "Small", "Medium", "Large", "Giant"]

    #Define an Animal Object.
    #"AnimalName", "Rarity", Health, Armor, {AttackTypes}, {MovementTypes}, {AbilityTypes}.
    def __init__(Animal, AnimalName, Size, PredPrey, Rarity, Health, Armor, AttackTypes, MovementTypes, AbilityTypes):

        #Animal Name/Rarity/Health/Armor.
        Animal.AnimalName = AnimalName #String Name of The Animal. Unique.
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
            if Animal.CurrentAbilities[Ability[0].AbilityName] == False:
                Animal.CurrentAbilities[Ability[0].AbilityName] = True

            #Update's Animal's Default Camoflauge
            elif Animal.CurrentAbilities[Ability[0].AbilityName] == 9999:

                if Ability[1] == "SelfReduced":
                    Animal.CurrentAbilities[Ability[0].AbilityName] = 2

                else:
                    Animal.CurrentAbilities[Ability[0].AbilityName] = 1

            #Update's Animal's Default Night Vision
            elif Animal.CurrentAbilities[Ability[0].AbilityName] == 1:

                if Ability[1] == "SelfReduced":
                    Animal.CurrentAbilities[Ability[0].AbilityName] = 2

                else:
                    Animal.CurrentAbilities[Ability[0].AbilityName] = 3

        #Save Original Camoflauge
        Animal.OriginalCamoflauge = Animal.CurrentAbilities["Camoflauge"]

    #Find an Ability in a Dictionary of Animal's Abilities.
    def FindAbility(AbilityName, Dictionary = None, Key = None):

        FoundAbility = None
        Ability = 0
        if Dictionary is not None:
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

    #Add Movement to All Movements That an Animal Has
    def AddMovement(Animal, Addition):

        for MovementType, MovementRadius in Animal.MovementTypes:
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
                Animal.AttackTypes[AttackType] = (Animal.AttackTypes[AttackType][0] + Addition, Animal.AttackTypes[AttackType][1:])

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
            FoundAbility = Animals.FindAbility("Venom", Animal.AttackTypes, AttackObject)
            if FoundAbility is not None:
                FoundAbility[0].AbilityFunction(Animal, FoundAbility[1])

        if Animal's Turn Ending:
            if Animal.CurrentAbilities["Venom"] > 0:
                #The Animal Takes Toxic Damage. Ignores Armor.
                FoundAbility = Animals.FindAbility("Venom")
                FoundAbility.AbilityFunction(Animal, Reverse = True)
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
                Animal.CurrentAbilities["Venom"] -= 1 if Animal.CurrentAbilities["Venom"] > 0 else 0

            else:
                Animal.CurrentAbilities["Venom"] += 1 if Animal.CurrentAbilities["Venom"] < 2 else 0

    #Apply Paralysis to Animal. Assume Conditions Met.
    #Paralysis = Immobilization of Smaller Animals. Chance 1-3 Turns of no Movement (50% Chance of Attack Paralysis During That Time).
    def Paralysis(ParalysisObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        if Animal Attacked:
            FoundAbility = Animals.FindAbility("Paralysis", OtherAnimal.AttackTypes, AttackObject)
            if FoundAbility is not None and Animals.AnimalSizes.index(OtherAnimal.Size) > Animals.AnimalSizes.index(Animal.Size):
                FoundAbility[0].AbilityFunction(Animal, FoundAbility[1])

        if Animal's Turn Starting:
            if Animal.CurrentAbilities["Paralysis"][0] or Animal.CurrentAbilities["Exhaustion"][1][0]:
                if r.random() < 0.5:
                    Turn Continues, Cannot Move
                else:
                    Skip Turn

        if Animal's Turn Ending:
            if Animal.CurrentAbilities["Paralysis"][0]:
                FoundAbility = Animals.FindAbility("Paralysis")
                FoundAbility.AbilityFunction(Animal, Reverse = True)

        Can Also Get Paralysis From Exhaustion Level 2
        '''

        #Check if This is a SubEffect
        if SubEffect == ParalysisObject.SubEffects[0]: #SubEffect == "Exhaustion"
            #Set Whether The Animal Has Paralysis Applied to The Animal to True or False. This Cuts Off Movement
            #For The Animal For 1 Turn. During This Time, There is a 50% Chance of Paralysis Each Turn.
            if Reverse:
                NewTime = (Animal.CurrentAbilities["Exhaustion"][1][1] - 1) if Animal.CurrentAbilities["Exhaustion"][1][1] > 0 else 0
                Animal.CurrentAbilities["Exhaustion"][1] = (False if NewTime == 0 else True, NewTime)

            else:
                Animal.CurrentAbilities["Exhaustion"][1] = (True, 1)

        #Not a SubEffect
        else:
            #Set Whether The Animal Has Paralysis Applied to The Animal to True or False. This Cuts Off Movement
            #For The Animal For 1-3 Turns. During This Time, There is a 50% Chance of Paralysis Each Turn.
            if Reverse:
                NewTime = (Animal.CurrentAbilities["Paralysis"][1] - 1) if Animal.CurrentAbilities["Paralysis"][1] > 0 else 0
                Animal.CurrentAbilities["Paralysis"] = (False if NewTime == 0 else True, NewTime)

            else:
                Animal.CurrentAbilities["Paralysis"] = (True, r.randint(1, 3))

    #Apply ColdBlooded to Animal. Assume Conditions Met.
    #ColdBlooded = Gains 1 HP Per Turn in Sun (Not Over Maximum), -1 HP Per Turn in Wildfire, Drought. Half Speed Rounded Down in Blizzard, Tundra.
    def ColdBlooded(ColdBloodedObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        if Animal.CurrentAbilities["ColdBlooded"]:
            if Animal's Turn Starting:
                FoundAbility = Animals.FindAbility("ColdBlooded", Animal.AbilityTypes, "None")

                if Environment == "Sun":
                    FoundAbility[0].AbilityFunction(Animal, "Sun")

                elif Environment in ["Wildfire", "Drought"]:
                    if FoundAbility[1] is not None:
                        #SubEffect == "+1 in Wildfire, Drought"
                        FoundAbility[0].AbilityFunction(Animal, FoundAbility[1])
                    else:
                        FoundAbility[0].AbilityFunction(Animal, SubEffect in ["Wildfire", "Drought"])

                elif Environment in ["Blizzard", "Tundra"]:
                    FoundAbility[0].AbilityFunction(Animal, SubEffect in ["Blizzard", "Tundra"])

            if Animal's Turn Ending:
                if Environment in ["Blizzard", "Tundra"]:
                    FoundAbility = Animals.FindAbility("ColdBlooded")
                    FoundAbility.AbilityFunction(Animal, SubEffect in ["Blizzard", "Tundra"], True)
        '''

        #Check if This is a SubEffect
        if SubEffect == ColdBloodedObject.SubEffects[0]: #SubEffect == "+1 in Wildfire, Drought"
            #The Animal Heals From Being in a Wildfire or Drought
            Animal.Health += 1 if Animal.Health < Animal.MaxHealth else 0

        #Not a SubEffect
        else:

            #The Animal Heals One Health Per Turn in The Sun
            if SubEffect == "Sun":
                Animal.Health += 1 if Animal.Health < Animal.MaxHealth else 0

            #The Animal Loses One Health Per Turn in a Wildfire or Drought
            elif SubEffect in ["Wildfire", "Drought"]:
                    Animal.Health -= 1 if Animal.Health > 0 else 0

            elif SubEffect in ["Blizzard", "Tundra"]:
                if Reverse:
                    Animal.MovementTypes = deepcopy(Animal.OriginalMovementTypes)

                else:
                    for MovementType, MovementRadius in Animal.MovementTypes:
                        Animal.MovementTypes[MovementType] = MovementRadius // 2

    #Apply Camoflauge to Animal. Assume Conditions Met.
    #Camoflauge = Unable to be Seen Easily. Visibility & Attackability of Animal is Within One "Space" Distance. Enemy Player Knows That The Card Exists on The Battlefield.
    def Camoflauge(CamoflaugeObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        if Animal's Turn Starting:
            ReverseCamoflauge = False
            if Action == Rattle and Animal.CurrentAbilities["Camoflauge"] != 9999:
                FoundAbility = Animals.FindAbility("Camoflauge", Animal.AbilityTypes, Action)
                if FoundAbility is not None:
                    FoundAbility[0].AbilityFunction(Animal, FoundAbility[1])
                    ReverseCamoflauge = True

            elif Action in [Smell, Echo Location] and OtherAnimal.CurrentAbilities["Camoflauge"] != 9999:
                FoundAbility = Animals.FindAbility("Camoflauge", Animal.AbilityTypes, Action)
                if FoundAbility is not None:
                    FoundAbility[0].AbilityFunction(OtherAnimal, FoundAbility[1])
                    ReverseCamoflauge = True

        if Animal's Turn Ending:
            if Action == Rattle and ReverseCamoflauge:
                FoundAbility = Animals.FindAbility("Camoflauge", Animal.AbilityTypes, Action)
                FoundAbility[0].AbilityFunction(Animal, FoundAbility[1], True)
                ReverseCamoflauge = False

            elif Action in [Smell, Echo Location] and ReverseCamoflauge:
                FoundAbility = Animals.FindAbility("Camoflauge", Animal.AbilityTypes, Action)
                FoundAbility[0].AbilityFunction(OtherAnimal, FoundAbility[1], True)
                ReverseCamoflauge = False
        '''

        #Check if This is a SubEffect
        if SubEffect == CamoflaugeObject.SubEffects[0] or SubEffect == CamoflaugeObject.SubEffects[2]: #SubEffect == "Reduced" or SubEffect == "SelfReduced"
            #The Animal Reduces Another Animal's Camoflauge or The Animal's Own Camoflauge
            if Reverse:
                Animal.CurrentAbilities["Camoflauge"] -= 2

            else:
                Animal.CurrentAbilities["Camoflauge"] += 2

        elif SubEffect == CamoflaugeObject.SubEffects[1]: #SubEffect == "Removed"
            #Camoflauge is Removed From This Animal
            if Reverse:
                Animal.CurrentAbilities["Camoflauge"] = Animal.OriginalCamoflauge

            else:
                Animal.CurrentAbilities["Camoflauge"] = 9999

        #Not a SubEffect
        else:
            pass #Default Camoflauge Already Applied at Animal Creation

    #Apply Night Vision to Animal. Assume Conditions Met.
    #Night Vision = Decreased Loss of Vision in The Dark.
    def NightVision(NightVisionObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        if Dark:
            if Animal's Turn Starting:
                ReverseNightVision = False
                if Action in [Smell, Echo Location] and Animal.CurrentAbilities["NightVision"] != 1:
                    FoundAbility = Animals.FindAbility("Night Vision", Animal.AbilityTypes, Action)
                    if FoundAbility is not None:
                        FoundAbility[0].AbilityFunction(Animal, FoundAbility[1])
                        ReverseNightVision = True

            if Animal's Turn Ending:
                if Action in [Smell, Echo Location] and ReverseNightVision:
                    FoundAbility = Animals.FindAbility("Night Vision", Animal.AbilityTypes, Action)
                    FoundAbility[0].AbilityFunction(Animal, FoundAbility[1], True)
                    ReverseNightVision = False
        '''

        #Check if This is a SubEffect
        if SubEffect == NightVisionObject.SubEffects[0]: #SubEffect = "SelfReduced"
            #Animal Reduces Animal's Own Night Vision
            if Reverse:
                Animal.CurrentAbilities["Night Vision"] += 1

            else:
                Animal.CurrentAbilities["Night Vision"] -= 1

        #Not a SubEffect
        else:
            pass #Default Night Vision Already Applied at Animal Creation

    #Apply Flinch to Animal. Assume Conditions Met.
    #Flinch = Skip Turn (Affects Lower Size Animals).
    def Flinch(FlinchObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        if Animal Attacked:
            FoundAbility = Animals.FindAbility("Flinch", OtherAnimal.AttackTypes, AttackObject)
            if FoundAbility is not None and Animals.AnimalSizes.index(OtherAnimal.Size) > Animals.AnimalSizes.index(Animal.Size):
                FoundAbility[0].AbilityFunction(Animal, FoundAbility[1])

        if Animal.CurrentAbilities["Flinch"]:
            if Animal's Turn Starting:
                Skip Turn

            if Animal's Turn Ending:
                FoundAbility = Animals.FindAbility("Flinch")
                FoundAbility.AbilityFunction(Animal, Reverse = True)
        '''

        #Check if This is a SubEffect
        if SubEffect is not None:
            pass #SubEffects do Not Exist For Flinch

        #Not a SubEffect
        else:
            if Reverse:
                Animal.CurrentAbilities["Flinch"] = False
            else:
                Animal.CurrentAbilities["Flinch"] = True

    #Apply Rations to Animal. Assume Conditions Met.
    #Rations = +1 HP Per Turn (Not Over Maximum).
    def Rations(RationsObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        if Animal's Turn Starting:
            if Animal.CurrentAbilities["Rations"]:
                FoundAbility = Animals.FindAbility("Rations", Animal.AbilityTypes, "None")
                FoundAbility[0].AbilityFunction(Animal, FoundAbility[1])
        '''

        #Check if This is a SubEffect
        if SubEffect is not None:
            pass #SubEffects do Not Exist For Rations

        #Not a SubEffect
        else:
            Animal.Health += 1 if Animal.Health < Animal.MaxHealth else 0

    #Apply Grouping to Animal. Assume Conditions Met.
    #Grouping = Animal is Stronger in Larger Groups. The More of The Same Animals on The Battlefield For The Start of
    #Animal's Turn, The More Grouping Bonuses For That Turn. +1 HP For Prey, +1 Attack For Predators. Up to 3.
    def Grouping(GroupingObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        if The Same Animal is Added to The Battlefield:
            for Animal in AllBattlefieldAnimalsWithThisType:
                FoundAbility = Animals.FindAbility("Grouping", Animal.AbilityTypes, "None")
                if FoundAbility is not None:
                    FoundAbility[0].AbilityFunction(Animal, FoundAbility[1])

        if The Same Animal is Removed From The Battlefield (Dies):
            for Animal in AllBattlefieldAnimalsWithThisType:
                FoundAbility = Animals.FindAbility("Grouping", Animal.AbilityTypes, "None")
                if FoundAbility is not None:
                    FoundAbility[0].AbilityFunction(Animal, FoundAbility[1], Reverse = True)
        '''

        #Check if This is a SubEffect
        if SubEffect == GroupingObject.SubEffects[0]: #SubEffect == "AttackTypes.AttackTypeList[1] : AbilityTypes.AbilityTypeList[1]"
            if Reverse:
                Animal.AttackTypes[AttackTypes.AttackTypeList[1]] = (Animal.AttackTypes[AttackTypes.AttackTypeList[1]][0], AttackTypes.AttackTypeList[5])

            else:
                Animal.AttackTypes[AttackTypes.AttackTypeList[1]] = (Animal.AttackTypes[AttackTypes.AttackTypeList[1]][0], AttackTypes.AttackTypeList[1])

        #Not a SubEffect
        else:
            if Reverse:
                if Animal.CurrentAbilities["Grouping"] > 0:
                    Animal.CurrentAbilities["Grouping"] -= 1

                    #Reverse +1 Attack For Predators
                    if Animal.PredPrey == "Predator":
                        AttackTypes.AddDamage(Animal, -1)

                    #Reverse +1 HP For Prey
                    else: #Animal.PredPrey == "Prey"
                        Animal.Health -= 1 if Animal.Health > 0 else 0
                        Animal.MaxHealth -= 1

            else:
                if Animal.CurrentAbilities["Grouping"] < 3:
                    Animal.CurrentAbilities["Grouping"] += 1

                    #+1 Attack For Predators
                    if Animal.PredPrey == "Predator":
                        AttackTypes.AddDamage(Animal, 1)

                    #+1 HP For Prey
                    else: #Animal.PredPrey == "Prey"
                        Animal.Health += 1
                        Animal.MaxHealth += 1

    #Apply Bleed to Animal. Assume Conditions Met.
    #Bleed = Lose 1 Health Ignoring Armor Per Level of Bleed Per Turn. Max 3.
    def Bleed(BleedObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        if Animal Attacked:
            FoundAbility = Animals.FindAbility("Bleed", OtherAnimal.AttackTypes, AttackObject)
            if FoundAbility is not None:
                FoundAbility[0].AbilityFunction(Animal, FoundAbility[1])

        if Animal's Turn Ending:
            if Animal.CurrentAbilities["Bleed"] > 0:
                FoundAbility = Animals.FindAbility("Bleed")
                if FoundAbility is not None:
                    FoundAbility.AbilityFunction(Animal, Reverse = True)
        '''

        #Check if This is a SubEffect
        if SubEffect is not None:
            pass #SubEffects do Not Exist For Bleed

        #Not a SubEffect
        else:
            if Reverse:
                Animal.Health -= Animal.CurrentAbilities["Bleed"] if Animal.Health - Animal.CurrentAbilities["Bleed"] > 0 else 0
                Animal.CurrentAbilities["Bleed"] -= 1 if Animal.CurrentAbilities["Bleed"] > 0 else 0

            else:
                Animal.CurrentAbilities["Bleed"] += 1 if Animal.CurrentAbilities["Bleed"] < 3 else 0

    #Apply Intellect to Animal. Assume Conditions Met.
    #Intellect = Able to Use Tools. (Axe For +1 Attack & Able to Cut Trees in Forest, Sword + Shield For +1 Attack & +1 Armor in Grasslands,
    #Boots For +1 to All Speeds in Tundra).
    def Intellect(IntellectObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        if Animal.CurrentAbilities["Intellect"] and Environment in [Forest, Grasslands, Tundra]:
            FoundAbility = Animals.FindAbility("Intellect", Animal.AbilityTypes, "None")
            FoundAbility[0].AbilityFunction(Animal, SubEffect in [Forest, Grasslands, Tundra])

        if Battle Ends:
            if Animal.CurrentAbilities["Intellect"] and Environment in [Forest, Grasslands, Tundra]:
                FoundAbility = Animals.FindAbility("Intellect", Animal.AbilityTypes, "None")
                FoundAbility[0].AbilityFunction(Animal, SubEffect in [Forest, Grasslands, Tundra], True)
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

                    #Reverse Can Cut Trees
                    del Animal.AbilityTypes["Cut Trees"]

                else:
                    #+1 Attack
                    AttackTypes.AddDamage(Animal, 1)

                    #Can Cut Trees
                    Animal.AbilityTypes["Cut Trees"] = tuple([])

            elif SubEffect == "Grasslands":
                #Sword + Shield
                if Reverse:
                    #Reverse +1 Attack
                    AttackTypes.AddDamage(Animal, -1)

                    #Reverse +1 Armor
                    Animal.Armor -= 1 if Animal.Armor > 0 else 0
                    Animal.MaxArmor -= 1

                else:
                    #+1 Attack
                    AttackTypes.AddDamage(Animal, 1)

                    #+1 Armor
                    Animal.Armor += 1
                    Animal.MaxArmor += 1

            elif SubEffect == "Tundra":
                #Boots For +1 Speed in Tundra
                if Reverse:
                    Animals.AddMovement(Animal, -1)

                else:
                    Animals.AddMovement(Animal, 1)

    #Apply Scavenger to Animal. Assume Conditions Met.
    #Scavenger = +1 HP (Not Over Maximum) When Ending Turn on a Square Where an Animal Has Died (One Turn Use Per Death on Square).
    def Scavenger(ScavengerObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        Each Square Needs a Count of Deaths on That Square.

        if Animal's Turn Ending:
            if Animal.CurrentAbilities["Scavenger"] and Square.DeathCount > 0:
                Square.DeathCount -= 1
                FoundAbility = Animals.FindAbility("Scavenger", Animal.AbilityTypes, "None")
                FoundAbility[0].AbilityFunction(Animal, FoundAbility[1])
        '''

        #Check if This is a SubEffect
        if SubEffect is not None:
            pass #SubEffects do Not Exist For Scavenger

        #Not a SubEffect
        else:
            Animal.Health += 1 if Animal.Health < Animal.MaxHealth else 0

    #Apply Poison to Animal. Assume Conditions Met.
    #Poison = Touching The Animal Causes Toxic Damage. Max 2.
    def Poison(PoisonObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        if Animal Attacked:
            FoundAbility = Animals.FindAbility("Poison", Animal.AbilityTypes, "Hurt")
            if FoundAbility is not None:
                FoundAbility[0].AbilityFunction(OtherAnimal, FoundAbility[1])

        if Animal's Turn Ending:
            if Animal.CurrentAbilities["Poison"] > 0:
                #The Animal Takes Toxic Damage. Ignores Armor.
                FoundAbility = Animals.FindAbility("Poison")
                FoundAbility.AbilityFunction(Animal, Reverse = True)
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
                Animal.CurrentAbilities["Poison"] -= 1 if Animal.CurrentAbilities["Poison"] > 0 else 0

            else:
                Animal.CurrentAbilities["Poison"] += 1 if Animal.CurrentAbilities["Poison"] < 2 else 0

    #Apply Fear to Animal. Assume Conditions Met.
    #Fear = Subtracts Attack From Opposing Animal (1 Per Size Difference).
    def Fear(FearObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        if Animal Played Onto Battlefield:
            FoundAbility = Animals.FindAbility("Fear", Animal.AbilityTypes, "OnSight")
            if FoundAbility is not None:
                for OtherAnimal in CanSeeAnimal:
                    FoundAbility[0].AbilityFunction(OtherAnimal, FoundAbility[1])

        if Action in [Rattle, Bark]:
            FoundAbility = Animals.FindAbility("Fear", Animal.AbilityTypes, Action)
            if FoundAbility is not None:
                for OtherAnimal in CanSeeAnimal:
                    FoundAbility[0].AbilityFunction(OtherAnimal, FoundAbility[1])

        if Animal's Turn Ending:
            if Animal.CurrentAbilities["Fear"] > 0:
                FoundAbility = Animals.FindAbility("Fear")
                FoundAbility.AbilityFunction(Animal, Reverse = True)
        '''

        if Reverse:
            #Remove All Fear
            Animal.CurrentAbilities["Fear"] = 0

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
                Animal.CurrentAbilities["Fear"] = abs(FearLevel)
                AttackTypes.AddDamage(Animal, min(0, FearLevel))

    #Apply Exhaustion to Animal. Assume Conditions Met.
    #Exhaustion = Level 1: Lose Half Speed, Rounded Down. Level 2: Paralysis, Cannot Move. Max 2.
    def Exhaustion(ExhaustionObject, Animal, SubEffect = None, Reverse = False):

        '''
        Use Cases:
        if Animal's Turn Ending + Animal Moved 2x Movement This Turn:
            FoundAbility = Animals.FindAbility("Exhaustion", Animal.AbilityTypes, "None")
            FoundAbility[0].AbilityFunction(Animal, FoundAbility[1])

        elif Animal's Turn Ending + Animal Did Not Move 2x Movement This Turn:
            FoundAbility = Animals.FindAbility("Exhaustion", Animal.AbilityTypes, "None")
            FoundAbility[0].AbilityFunction(Animal, FoundAbility[1], True)
        '''

        if not(Reverse):
            Animal.CurrentAbilities["Exhaustion"] += 1 if Animal.CurrentAbilities["Exhaustion"] < 2 else 0

        #Level 1 Exhaustion, Speed Drop.
        if Animal.CurrentAbilities["Exhaustion"] == 1:
            if Reverse:
                Animal.CurrentAbilities["Exhaustion"] -= 1
                Animal.MovementTypes = deepcopy(Animal.OriginalMovementTypes)

            else:
                #Check if This is a SubEffect
                if SubEffect == ExhaustionObject.SubEffects[0]:
                    #Speed Drops by Half, Halved
                    for MovementType, MovementRadius in Animal.MovementTypes:
                        Animal.MovementTypes[MovementType] = MovementRadius * 3 // 4

                #Not a SubEffect
                else:
                    #Speed Drops by Half
                    for MovementType, MovementRadius in Animal.MovementTypes:
                        Animal.MovementTypes[MovementType] = MovementRadius // 2

        #Level 2 Exhaustion, Paralysis.
        elif Animal.CurrentAbilities["Exhaustion"] == 2:
            if Reverse:
                Animal.CurrentAbilities["Exhaustion"] -= 1
                #Remove Exhaustion Paralysis
                FoundAbility = Animals.FindAbility("Paralysis")
                while Animal.CurrentAbilities["Exhaustion"][1][0]:
                    FoundAbility.AbilityFunction(Animal, "Exhaustion", Reverse = True)

            else:
                FoundAbility = Animals.FindAbility("Paralysis")
                FoundAbility.AbilityFunction(Animal, "Exhaustion")

#Create The Animals + Attack Types.
def CreateAnimalsAndAttackTypes():

    #Create AbilityTypes: "AbilityName", ["SubEffects"]
    AbilityTypes("Venom", AbilityTypes.Venom)
    AbilityTypes("Paralysis", AbilityTypes.Paralysis, ["Exhaustion"])
    AbilityTypes("ColdBlooded", AbilityTypes.ColdBlooded, ["+1 in Wildfire, Drought"])
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


    #Create Bison (Epic).
    AnimalAttacks = { #AttackType Object: (Damage, AbilityType Objects)
        AttackTypes.AttackTypeList[1]: (2, AbilityTypes.AbilityTypeList[5]),
        AttackTypes.AttackTypeList[8]: (3, AbilityTypes.AbilityTypeList[5])
    }

    AnimalAbilities = { #"Activation": (AbilityType Objects)
        "None": (AbilityTypes.AbilityTypeList[7], AbilityTypes.AbilityTypeList[13]),
        "Grouping": tuple(["AttackTypes.AttackTypeList[1] : AbilityTypes.AbilityTypeList[1]"])
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