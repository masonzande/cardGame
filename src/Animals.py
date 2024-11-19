import random as r #Randomization.
from copy import deepcopy
from InitAnimals import Animals, CreateAnimalsAndAttackTypes
from AnimalGrid import AnimalSight, CreateEnvironmentGrid

'''Update Pre-Battle Effects.'''
def PreBattleEffects():

    #Grouping (Assuming All Animals Start on The Battlefield).
    UniqueAnimals = list(set([Animal2.AnimalName for Animal2 in Animals.AnimalList]))
    for AnimalName in UniqueAnimals:
        AllBattlefieldAnimalsWithThisType = [Animal2 for Animal2 in Animals.AnimalList if Animal2.AnimalName == AnimalName]
        if len(AllBattlefieldAnimalsWithThisType) > 1:
            for SameAnimal in AllBattlefieldAnimalsWithThisType:
                FoundAbility = Animals.FindAbility("Grouping", SameAnimal.AbilityTypes, "None")
                if FoundAbility is not None:
                    FoundAbility[0].AbilityFunction(FoundAbility[0], SameAnimal, FoundAbility[1])

'''Animal Turn Start, Update Effects.'''
def StartTurnEffects(Animal, Weather, Environment, NoMovement, SkipTurn):

    #Cold Blooded
    if Animal.CurrentAbilities["ColdBlooded"]:
        FoundAbility = Animals.FindAbility("ColdBlooded", Animal.AbilityTypes, "None")
        if FoundAbility[1] is not None and Weather in ["Wildfire", "Drought"]:
            #SubEffect == "+1 in Wildfire, Drought"
            FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1])

        elif Weather in ["Wildfire", "Drought", "Blizzard", "Sun"]:
            FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, Weather)

        elif Environment in ["Tundra"]:
            FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, Environment)

    #Intellect
    if Animal.CurrentAbilities["Intellect"] and Environment in ["Forest", "Grasslands", "Tundra"]:
        FoundAbility = Animals.FindAbility("Intellect", Animal.AbilityTypes, "None")
        FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, Environment)

    #Rations
    if Animal.CurrentAbilities["Rations"]:
        FoundAbility = Animals.FindAbility("Rations", Animal.AbilityTypes, "None")
        FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1])

    #Paralysis
    if Animal.CurrentAbilities["Paralysis"][0] or Animal.CurrentAbilities["Exhaustion"][1][0]:
        if r.random() < 0.5:
            NoMovement = True
            for MovementType in Animal.MovementTypes.keys():
                Animal.MovementTypes[MovementType] = 0
            print(f"Due to {Animal.AnimalName}'s Paralysis, {Animal.AnimalName} Cannot Move This Turn.")

        else:
            SkipTurn = True
            print(f"Due to {Animal.AnimalName}'s Paralysis, {Animal.AnimalName}'s Turn Was Skipped.")

    #Flinch
    if Animal.CurrentAbilities["Flinch"]:
        SkipTurn = True
        print(f"Due to {Animal.AnimalName} Being Flinched, {Animal.AnimalName}'s Turn Was Skipped.")

    return NoMovement, SkipTurn

'''Perform a Movement Action.'''
def MovementAction(Animal, Environment, DayNight, Grid2D, AttackRadiusAnimals, VisionPlusRadius, ValidMovements, ObstaclesBeside, AnimalsSeen):

    #Choose a Movement
    Movements = ["None"]
    for MovementType in Animal.MovementTypes.keys():
        if MovementType in ["Walk", "Slither", "Climb", "Jump", "Fly"] and Environment not in ["Ocean"]:
            Movements.append(MovementType)

        elif MovementType in ["Swim", "Fly"] and Environment in ["Ocean"]:
            Movements.append(MovementType)

        if MovementType in Movements and MovementType not in ["Climb", "Jump"]:
            Movements.append(f"2x{MovementType}")

    Movement = Movements[r.randint(0, len(Movements) - 1)]

    #Animal Movements Cannot Move Into The Same Grid Location as Another Animal
    if Movement in ["Walk", "2xWalk"] and ValidMovements["Walk"] != []:
        '''Walk.'''

        #Cannot Move Into The Same Grid Location as Obstacles
        print(f"{Animal.AnimalName} {'2x' if Movement.startswith('2x') else ''}Walked From {Animal.CurrentLocation}", end = " ")
        Animal.CurrentLocation = r.choice(ValidMovements["Walk"])
        print(f"to {Animal.CurrentLocation}.")

    elif Movement in ["Slither", "2xSlither"] and ValidMovements["Slither"] != []:
        '''Slither.'''

        #Can Move Into The Same Grid Location as Obstacles
        print(f"{Animal.AnimalName} {'2x' if Movement.startswith('2x') else ''}Slithered From {Animal.CurrentLocation}", end = " ")
        Animal.CurrentLocation = r.choice(ValidMovements["Slither"])
        print(f"to {Animal.CurrentLocation}.")

    elif Movement == "Climb" and ValidMovements["Climb"] != []:
        '''Climb.'''

        #Has to Move Into The Same Grid Location as Obstacles
        print(f"{Animal.AnimalName} {'2x' if Movement.startswith('2x') else ''}Climbed From {Animal.CurrentLocation}", end = " ")
        Animal.CurrentLocation = r.choice(ValidMovements["Climb"])
        print(f"to {Animal.CurrentLocation}.")

    elif Movement == "Jump" and ValidMovements["Jump"] != []:
        '''Jump.'''

        #Has to Move Onto The Other Side of Animal's Grid Location Compared to an Obstacle's (Animal Must be Right Next to The Obstacle)
        print(f"{Animal.AnimalName} {'2x' if Movement.startswith('2x') else ''}Jumped From {Animal.CurrentLocation}", end = " ")
        Animal.CurrentLocation = r.choice(ValidMovements["Jump"])
        print(f"to {Animal.CurrentLocation}.")

    elif Movement in ["Swim", "2xSwim"] and ValidMovements["Swim"] != []:
        '''Swim.'''

        #Cannot Move Into The Same Grid Location as Obstacles
        print(f"{Animal.AnimalName} {'2x' if Movement.startswith('2x') else ''}Swam From {Animal.CurrentLocation}", end = " ")
        Animal.CurrentLocation = r.choice(ValidMovements["Swim"])
        print(f"to {Animal.CurrentLocation}.")

    elif Movement in ["Fly", "2xFly"] and ValidMovements["Fly"] != []:
        '''Fly.'''

        #Can Move Into The Same Grid Location as Obstacles
        print(f"{Animal.AnimalName} {'2x' if Movement.startswith('2x') else ''}Flew From {Animal.CurrentLocation}", end = " ")
        Animal.CurrentLocation = r.choice(ValidMovements["Fly"])
        print(f"to {Animal.CurrentLocation}.")

    #Exhaustion
    if Movement.startswith("2x"):
        FoundAbility = Animals.FindAbility("Exhaustion", Animal.AbilityTypes, "None")
        FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1])

    if Movement != "None":
        '''Determine Who The Animal Can See (Using Camoflauge, Night Vision).'''
        AttackRadiusAnimals, VisionPlusRadius, ValidMovements, ObstaclesBeside, AnimalsSeen = AnimalSight(Animal, Grid2D, DayNight)

    return Movement, AttackRadiusAnimals, VisionPlusRadius, ValidMovements, ObstaclesBeside, AnimalsSeen

'''Perform a Non-Movement, Non-Attack Action.'''
def ExtraAction(Animal, DayNight, Grid2D, AttackRadiusAnimals, VisionPlusRadius, ValidMovements, ObstaclesBeside, AnimalsSeen):

    #Choose an Action
    Actions = []
    for AbilityType in Animal.AbilityTypes.keys():
        if AbilityType not in ["None", "OnSight", "Hurt"]:
            if (AbilityType == "Cut Trees" and ObstaclesBeside != []) or AbilityType != "Cut Trees":
                Actions.append(AbilityType)
    Action = Actions[r.randint(0, len(Actions) - 1)] if Actions != [] else ""
    if Action != "":
        print(f"{Animal.AnimalName} Used {Action}.")

    #Remove Animal From AnimalList to Not Affect Itself.
    Animals.AnimalList.remove(Animal)
    Defenders = []

    if Action == "Rattle":
        '''Rattle.'''

        #Camoflauge
        if Animal.CurrentAbilities["Camoflauge"] != 9999:
            FoundAbility = Animals.FindAbility("Camoflauge", Animal.AbilityTypes, Action)
            if FoundAbility is not None:
                FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1])

        #Fear (Assuming if Animal Sees Other Animals, The Other Animals See Animal).
        FoundAbility = Animals.FindAbility("Fear", Animal.AbilityTypes, Action)
        if FoundAbility is not None:
            for OtherAnimal in AnimalsSeen:
                FoundAbility[0].AbilityFunction(FoundAbility[0], OtherAnimal, FoundAbility[1])

    elif Action == "Smell":
        '''Smell.'''

        #Assume Smell Hits Every Animal Within Vision + 1 Distance Right Now, Not Through Obstacles.
        for Defender in list(VisionPlusRadius):
            Defenders.append(Defender)
            if Defender in Animals.AnimalList:
                Animals.AnimalList.remove(Defender) #Remove Chosen Defenders to Not Choose The Same Defender Twice.

        #Camoflauge
        for Defender in Defenders:
            if Defender.CurrentAbilities["Camoflauge"] != 9999:
                FoundAbility = Animals.FindAbility("Camoflauge", Animal.AbilityTypes, Action)
                if FoundAbility is not None:
                    FoundAbility[0].AbilityFunction(FoundAbility[0], Defender, FoundAbility[1])

        #Night Vision
        if Animal.CurrentAbilities["Night Vision"] != 1:
            FoundAbility = Animals.FindAbility("Night Vision", Animal.AbilityTypes, Action)
            if FoundAbility is not None:
                FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1])
                '''Determine Who The Animal Can See (Using Camoflauge, Night Vision).'''
                AttackRadiusAnimals, VisionPlusRadius, ValidMovements, ObstaclesBeside, AnimalsSeen = AnimalSight(Animal, Grid2D, DayNight)

    elif Action == "Echo Location":
        '''Echo Location.'''

        #Assume Echo Location Hits Every Animal Within Vision + 1 Distance Right Now, Not Through Obstacles.
        for Defender in list(VisionPlusRadius):
            Defenders.append(Defender)
            if Defender in Animals.AnimalList:
                Animals.AnimalList.remove(Defender) #Remove Chosen Defenders to Not Choose The Same Defender Twice.

        #Camoflauge
        for Defender in Defenders:
            if Defender.CurrentAbilities["Camoflauge"] != 9999:
                FoundAbility = Animals.FindAbility("Camoflauge", Animal.AbilityTypes, Action)
                if FoundAbility is not None:
                    FoundAbility[0].AbilityFunction(FoundAbility[0], Defender, FoundAbility[1])

        #Night Vision
        if Animal.CurrentAbilities["Night Vision"] != 1:
            FoundAbility = Animals.FindAbility("Night Vision", Animal.AbilityTypes, Action)
            if FoundAbility is not None:
                FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1])
                '''Determine Who The Animal Can See (Using Camoflauge, Night Vision).'''
                AttackRadiusAnimals, VisionPlusRadius, ValidMovements, ObstaclesBeside, AnimalsSeen = AnimalSight(Animal, Grid2D, DayNight)

    elif Action == "Bark":
        '''Bark.'''

        #Fear (Assuming if Animal Sees Other Animals, The Other Animals See Animal).
        FoundAbility = Animals.FindAbility("Fear", Animal.AbilityTypes, Action)
        if FoundAbility is not None:
            for OtherAnimal in AnimalsSeen:
                FoundAbility[0].AbilityFunction(FoundAbility[0], OtherAnimal, FoundAbility[1])

    elif Action == "Cut Trees":
        '''Cut Trees.'''
        DestroyObstacle = r.choice(ObstaclesBeside)
        Grid2D[DestroyObstacle[0]][DestroyObstacle[1]] = ""

        '''Determine Who The Animal Can See (Using Camoflauge, Night Vision).'''
        AttackRadiusAnimals, VisionPlusRadius, ValidMovements, ObstaclesBeside, AnimalsSeen = AnimalSight(Animal, Grid2D, DayNight)

    return Action, Grid2D, AttackRadiusAnimals, VisionPlusRadius, ValidMovements, ObstaclesBeside, AnimalsSeen, Defenders

'''Perform an Attack Action.'''
def AttackAction(Animal, AttackRadiusAnimals):

    Defenders = []
    if Animal.AttackTypes != {}:
        '''Attack.'''

        #Choose an AttackType.
        ChosenAttackType = r.choice([AttackType for AttackType in Animal.AttackTypes.keys()])

        #Choose Animals to Attack.
        if ChosenAttackType.SplashDamage[0]: #Assume Splash Hits Every Seen Animal in Attack Radius Right Now, Not Through Obstacles.
            for Defender in list(AttackRadiusAnimals[ChosenAttackType]):
                Defenders.append(Defender)
                if Defender in Animals.AnimalList:
                    Animals.AnimalList.remove(Defender) #Remove Chosen Defenders to Not Choose The Same Defender Twice.

        else:
            Defenders = [Animals.AnimalList[r.randint(0, len(Animals.AnimalList) - 1)]]
            Animals.AnimalList.remove(Defenders[0]) #Remove Chosen Defenders to Not Choose The Same Defender Twice (Consistency).

        #Attack Chosen Animals.
        for Defender in Defenders:
            Defenders = Animal.Attack(Defender, Animal.AttackTypes[ChosenAttackType][0], Defenders, ChosenAttackType) #Defender, Damage, AttackType.

    return Defenders

'''Animal Turn End, Update Effects.'''
def EndTurnEffects(Animal, Weather, Environment, Action, Movement, DeathGrid2D):

    #Venom
    if Animal.CurrentAbilities["Venom"] > 0:
        #The Animal Takes Toxic Damage. Ignores Armor.
        FoundAbility = Animals.FindAbility("Venom")
        FoundAbility.AbilityFunction(FoundAbility, Animal, Reverse = True)

    #Paralysis
    if Animal.CurrentAbilities["Paralysis"][0]:
        FoundAbility = Animals.FindAbility("Paralysis")
        FoundAbility.AbilityFunction(FoundAbility, Animal, Reverse = True)

    #Cold Blooded
    if Animal.CurrentAbilities["ColdBlooded"]:
        if Weather in ["Blizzard"]:
            FoundAbility = Animals.FindAbility("ColdBlooded")
            FoundAbility.AbilityFunction(FoundAbility, Animal, Weather, True)

        elif Environment in ["Tundra"]:
            FoundAbility = Animals.FindAbility("ColdBlooded")
            FoundAbility.AbilityFunction(FoundAbility, Animal, Environment, True)

    #Camoflauge
    if Action == "Rattle" and Animal.CurrentAbilities["Camoflauge"] != Animal.OriginalCamoflauge:
        #Undo Animal's Own Camoflauge Reduction
        FoundAbility = Animals.FindAbility("Camoflauge", Animal.AbilityTypes, Action)
        if FoundAbility is not None:
            FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1], True)

    if Animal.CurrentAbilities["Camoflauge"] != Animal.OriginalCamoflauge:
        #Reverse Other Camoflauge Reductions on Animal
        FoundAbility = Animals.FindAbility("Camoflauge")
        FoundAbility.AbilityFunction(FoundAbility, Animal, "Removed" if Animal.CurrentAbilities["Camoflauge"] == 9999 else "Reduced", True) #Assume Camoflauge Reductions Not at 9999

    #Night Vision
    if Animal.CurrentAbilities["Night Vision"] != Animal.OriginalNightVision:
        FoundAbility = Animals.FindAbility("Night Vision")
        FoundAbility[0].AbilityFunction(FoundAbility, Animal, Reverse = True)

    #Exhaustion
    if not(Movement.startswith("2x")):
        FoundAbility = Animals.FindAbility("Exhaustion", Animal.AbilityTypes, "None")
        FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1], True)

    #Flinch
    if Animal.CurrentAbilities["Flinch"]:
        FoundAbility = Animals.FindAbility("Flinch")
        FoundAbility.AbilityFunction(FoundAbility, Animal, Reverse = True)

    #Bleed
    if Animal.CurrentAbilities["Bleed"] > 0:
        FoundAbility = Animals.FindAbility("Bleed")
        if FoundAbility is not None:
            FoundAbility.AbilityFunction(FoundAbility, Animal, Reverse = True)

    #Intellect
    if Animal.CurrentAbilities["Intellect"] and Environment in ["Forest", "Grasslands", "Tundra"]:
        FoundAbility = Animals.FindAbility("Intellect", Animal.AbilityTypes, "None")
        FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, Environment, True)

    #Scavenger
    if Animal.CurrentAbilities["Scavenger"] and DeathGrid2D[Animal.CurrentLocation[0]][Animal.CurrentLocation[1]] > 0:
        DeathGrid2D[Animal.CurrentLocation[0]][Animal.CurrentLocation[1]] -= 1
        FoundAbility = Animals.FindAbility("Scavenger", Animal.AbilityTypes, "None")
        FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1])

    #Poison
    if Animal.CurrentAbilities["Poison"] > 0:
        #The Animal Takes Toxic Damage. Ignores Armor.
        FoundAbility = Animals.FindAbility("Poison")
        FoundAbility.AbilityFunction(FoundAbility, Animal, Reverse = True)

    #Fear
    if Animal.CurrentAbilities["Fear"] > 0:
        FoundAbility = Animals.FindAbility("Fear")
        FoundAbility.AbilityFunction(FoundAbility, Animal, Reverse = True)

    return DeathGrid2D

def EndTurn(Animal, SkipTurn, NoMovement, Defenders, Defenders2, DeathGrid2D):

    if not(SkipTurn):
        #Append Animals Back to AnimalList.
        AllAnimals = list(set(Defenders + Defenders2)) + [Animal]
        for Animal2 in AllAnimals:
            if Animal2.Health > 0:
                Animals.AnimalList.append(Animal2)

            else:
                print(f"{Animal2.AnimalName} is Dead.")
                DeathGrid2D[Animal2.CurrentLocation[0]][Animal2.CurrentLocation[1]] += 1

                #Grouping (Assuming All Animals Start on The Battlefield).
                AllBattlefieldAnimalsWithThisType = [Animal3 for Animal3 in AllAnimals if Animal3.AnimalName == Animal2.AnimalName]
                if len(AllBattlefieldAnimalsWithThisType) > 1:
                    for SameAnimal in AllBattlefieldAnimalsWithThisType:
                        FoundAbility = Animals.FindAbility("Grouping", SameAnimal.AbilityTypes, "None")
                        if FoundAbility is not None:
                            FoundAbility[0].AbilityFunction(FoundAbility[0], SameAnimal, FoundAbility[1], Reverse = True)

    else:
        if NoMovement:
            Animal.MovementTypes = deepcopy(Animal.OriginalMovementTypes)

        if Animal.Health <= 0:
            AllBattlefieldAnimalsWithThisType = [Animal2 for Animal2 in Animals.AnimalList if Animal2.AnimalName == Animal.AnimalName]
            Animals.AnimalList.remove(Animal)
            print(f"{Animal.AnimalName} is Dead.")
            DeathGrid2D[Animal.CurrentLocation[0]][Animal.CurrentLocation[1]] += 1

            #Grouping (Assuming All Animals Start on The Battlefield).
            if len(AllBattlefieldAnimalsWithThisType) > 1:
                for SameAnimal in AllBattlefieldAnimalsWithThisType:
                    FoundAbility = Animals.FindAbility("Grouping", SameAnimal.AbilityTypes, "None")
                    if FoundAbility is not None:
                        FoundAbility[0].AbilityFunction(FoundAbility[0], SameAnimal, FoundAbility[1], Reverse = True)

    return DeathGrid2D

#Test File
def main():

    #Create The Animals + AttackTypes.
    CreateAnimalsAndAttackTypes()

    #Choose Environment, Weather / Natural Disaster, Time of Day.
    Environment, Weather, DayNight, Grid2D, DeathGrid2D = CreateEnvironmentGrid()

    '''Update Pre-Battle Effects.'''
    PreBattleEffects()

    #Print The Stats of All Animals Before Any Attacks.
    Animals.PrintAllAnimals()

    #All Animals Attack a Random Other Animal (All if Splash)
    for Animal in list(Animals.AnimalList):
        SkipTurn = False
        NoMovement = False

        if Animal.Health > 0:

            '''Animal Turn Start, Update Effects.'''
            NoMovement, SkipTurn = StartTurnEffects(Animal, Weather, Environment, NoMovement, SkipTurn)

            '''Turn.'''
            if not(SkipTurn):

                '''Determine Who The Animal Can See (Using Camoflauge, Night Vision).'''
                AttackRadiusAnimals, VisionPlusRadius, ValidMovements, ObstaclesBeside, AnimalsSeen = AnimalSight(Animal, Grid2D, DayNight)

                '''Perform a Movement Action.'''
                Movement, AttackRadiusAnimals, VisionPlusRadius, ValidMovements, ObstaclesBeside, AnimalsSeen = MovementAction(Animal, Environment, DayNight, Grid2D, AttackRadiusAnimals, VisionPlusRadius, ValidMovements, ObstaclesBeside, AnimalsSeen)

                '''Perform a Non-Movement, Non-Attack Action.'''
                Action, Grid2D, AttackRadiusAnimals, VisionPlusRadius, ValidMovements, ObstaclesBeside, AnimalsSeen, Defenders = ExtraAction(Animal, DayNight, Grid2D, AttackRadiusAnimals, VisionPlusRadius, ValidMovements, ObstaclesBeside, AnimalsSeen)

                '''Perform an Attack Action.'''
                Defenders2 = AttackAction(Animal, AttackRadiusAnimals)

            '''Animal Turn End, Update Effects.'''
            DeathGrid2D = EndTurnEffects(Animal, Weather, Environment, Action, Movement, DeathGrid2D)

            #End of Turn
            DeathGrid2D = EndTurn(Animal, SkipTurn, NoMovement, Defenders, Defenders2, DeathGrid2D)

    #Print The Stats of All Animals After The Battle.
    Animals.PrintAllAnimals()

main()