from copy import deepcopy
from InitAnimals import Animals, CreateAttackAbilityTypes, CreateAnimalDeck, CreateEachAnimal
from AnimalGrid import AnimalSight, CreateEnvironmentGrid, AddAnimalToGrid
import numpy as np

'''Update Join-Battle Effects.'''
def JoinBattleEffects():

    #Grouping.
    print("\nJoin-Battle Effects Applied.")
    UniqueAnimals = np.unique(np.array([Animal2.AnimalName for Animal2 in Animals.InBattle], dtype = object))
    for AnimalName in UniqueAnimals:
        AllBattlefieldAnimalsWithThisType = np.array([OtherAnimal for OtherAnimal in Animals.InBattle if OtherAnimal.AnimalName == AnimalName], dtype = object)
        if AllBattlefieldAnimalsWithThisType.shape[0] > 1:
            #Assume Each of The Same Animal Has Grouping or Not
            FoundAbility = Animals.FindAbility("Grouping", AllBattlefieldAnimalsWithThisType[0].AbilityTypes, "None")

            if FoundAbility is not None:
                for SameAnimal in AllBattlefieldAnimalsWithThisType:
                    FoundAbility[0].AbilityFunction(FoundAbility[0], SameAnimal, FoundAbility[1])

'''Animal Turn Start, Update Effects.'''
def StartTurnEffects(Animal, Weather, Environment, NoMovement, SkipTurn):

    #Cold Blooded
    if Animal.CurrentAbilities["ColdBlooded"]:
        FoundAbility = Animals.FindAbility("ColdBlooded", Animal.AbilityTypes, "None")
        if FoundAbility[1] is not None and Weather in ("Wildfire", "Drought"):
            #SubEffect == "+1 in Wildfire, Drought"
            FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1])

        elif Weather in ("Wildfire", "Drought", "Blizzard", "Sun"):
            FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, Weather)

        elif Environment == "Tundra":
            FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, Environment)

    #Intellect
    if Animal.CurrentAbilities["Intellect"] and Environment in ("Forest", "Grasslands", "Tundra"):
        FoundAbility = Animals.FindAbility("Intellect", Animal.AbilityTypes, "None")
        FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, Environment)

    #Rations
    if Animal.CurrentAbilities["Rations"]:
        FoundAbility = Animals.FindAbility("Rations", Animal.AbilityTypes, "None")
        FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1])

    #Paralysis
    if Animal.CurrentAbilities["Paralysis"][0] or Animal.CurrentAbilities["Exhaustion"][1][0]:
        if np.random.random() < 0.5:
            NoMovement = True
            for MovementType in Animal.MovementTypes.keys():
                Animal.MovementTypes[MovementType] = 0
            print(f"Due to {Animal}'s Paralysis, {Animal} Cannot Move This Turn.")

        else:
            SkipTurn = True
            print(f"Due to {Animal}'s Paralysis, {Animal}'s Turn Was Skipped.")

    #Flinch
    if Animal.CurrentAbilities["Flinch"]:
        SkipTurn = True
        print(f"Due to {Animal} Being Flinched, {Animal}'s Turn Was Skipped.")

    return NoMovement, SkipTurn

'''Perform a Movement Action.'''
def MovementAction(Animal, Environment, DayNight, Grid2D, AttackRadiusAnimals, VisionPlusRadius, ValidMovements, ObstaclesBeside, AnimalsSeen):

    #Choose a Movement
    Movements = ["None"]
    for MovementType in Animal.MovementTypes.keys():
        if MovementType in ("Walk", "Slither", "Climb", "Jump", "Fly") and ValidMovements[MovementType].shape[0] != 0 and Environment != "Ocean":
            Movements.append(MovementType)

        elif Environment == "Ocean" and MovementType in ("Swim", "Fly") and ValidMovements[MovementType].shape[0] != 0:
            Movements.append(MovementType)

    Movements = np.array(Movements, dtype = np.str_)
    Movement = ""
    while Movement not in Movements and Movement.upper() != "N":
        Movement = input(f"Which Valid Movement Type Should {Animal} Choose to Use From {Movements} (N For None)? ")
    SaveLocation = Animal.CurrentLocation

    #Animal Movements Cannot Move Into The Same Grid Location as Another Animal
    if Movement == "Walk" and ValidMovements["Walk"].shape[0] != 0:
        '''Walk.'''

        #Cannot Move Into The Same Grid Location as Obstacles or Animals
        Moved = "Walked"

    elif Movement == "Slither" and ValidMovements["Slither"].shape[0] != 0:
        '''Slither.'''

        #Can Move Into The Same Grid Location as Obstacles, Without Animals
        Moved = "Slithered"

    elif Movement == "Climb" and ValidMovements["Climb"].shape[0] != 0:
        '''Climb.'''

        #Has to Move Into The Same Grid Location as Obstacles, Without Animals
        Moved = "Climbed"

    elif Movement == "Jump" and ValidMovements["Jump"].shape[0] != 0:
        '''Jump.'''

        #Has to Move Onto The Other Side of Animal's Grid Location Compared to an Obstacle's
        #(Animal Must be Right Next to The Obstacle, Without Animals).
        Moved = "Jumped"

    elif Movement == "Swim" and ValidMovements["Swim"].shape[0] != 0:
        '''Swim.'''

        #Cannot Move Into The Same Grid Location as Obstacles or Animals
        Moved = "Swam"

    elif Movement == "Fly" and ValidMovements["Fly"].shape[0] != 0:
        '''Fly.'''

        #Can Move Into The Same Grid Location as Obstacles, Without Animals
        Moved = "Flew"

    if Movement != "None":
        #Move Animal
        print(f"Valid Movements For {Movement}: {ValidMovements[Movement]}")
        print(f"This Includes Movements up to Twice The Value of {Animal}'s Movement Speed For Movement {Movement}.")
        GridLocation = Animal.CurrentLocation
        while not(any(np.array_equal(GridLocation, ValidMove) for ValidMove in ValidMovements[Movement])):
            GridLocation = input(f"Which Location Should {Animal} go to? ")
            GridLocation = GridLocation.replace(",", " ")
            GridLocation = [XY.strip() for XY in GridLocation.split(" ") if XY.strip() != ""]
            GridLocation = np.array([int(GridLocation[0]), int(GridLocation[1])], dtype = np.int32)
        Animal.CurrentLocation = GridLocation

        #Check if Movement Was 2x
        if np.abs(Animal.CurrentLocation[0] - SaveLocation[0]) > Animal.MovementTypes[Movement] or np.abs(Animal.CurrentLocation[1] - SaveLocation[1]) > Animal.MovementTypes[Movement]:
            Movement = f"2x{Movement}"

        #Print Movement
        print(f"{Animal} {'2x' if Movement.startswith('2x') else ''}{Moved} From {SaveLocation} to {Animal.CurrentLocation}.")

    #Exhaustion
    if Movement.startswith("2x"):
        FoundAbility = Animals.FindAbility("Exhaustion", Animal.AbilityTypes, "None")
        FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1])

    if Movement != "None":
        #Update The Grid
        Grid2D[SaveLocation[0]][SaveLocation[1]][1] = Grid2D[SaveLocation[0]][SaveLocation[1]][0] #Old Location
        Grid2D[Animal.CurrentLocation[0]][Animal.CurrentLocation[1]][1] = Animal #New Location

        '''Determine Who The Animal Can See (Using Camoflauge, Night Vision).'''
        AttackRadiusAnimals, VisionPlusRadius, ValidMovements, ObstaclesBeside, AnimalsSeen = AnimalSight(Animal, Grid2D, DayNight)

    else:
        print("Movement Not Chosen.")

    return Movement, AttackRadiusAnimals, VisionPlusRadius, ValidMovements, ObstaclesBeside, AnimalsSeen

'''Perform a Non-Movement, Non-Attack Action.'''
def ExtraAction(Animal, DayNight, Grid2D, AttackRadiusAnimals, VisionPlusRadius, ValidMovements, ObstaclesBeside, AnimalsSeen):

    #Choose an Action
    Actions = []
    for AbilityType in Animal.AbilityTypes.keys():
        if AbilityType not in ("None", "OnSight", "Hurt"):
            if (AbilityType == "Cut Trees" and ObstaclesBeside.shape[0] != 0) or AbilityType != "Cut Trees":
                Actions.append(AbilityType)
    Actions = np.array(Actions, dtype = np.str_)

    Action = ""
    if Actions.shape[0] != 0:
        while Action not in Actions and Action.upper() != "N":
            Action = input(f"Which Valid Action Should {Animal} Choose to Use From {Actions} (N For None)? ")
        print(f"{Animal} Used {Action}.")

    #Remove Animal From InBattle to Not Affect Itself.
    Animals.InBattle = np.delete(Animals.InBattle, np.where(Animals.InBattle == Animal)[0][0])
    Defenders = np.array([], dtype = object)

    if Action == "Rattle":
        '''Rattle.'''

        #Camoflauge
        if Animal.CurrentAbilities["Camoflauge"] != 9999:
            FoundAbility = Animals.FindAbility("Camoflauge", Animal.AbilityTypes, Action)
            if FoundAbility is not None:
                FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1])

        #Fear (Assuming if Animal Sees Opposing Animals, The Opposing Animals See Animal).
        FoundAbility = Animals.FindAbility("Fear", Animal.AbilityTypes, Action)
        if FoundAbility is not None:
            print(f"Surrounding Animals Heard & Feared {Animal}'s Rattle: {np.array([OtherAnimal.AnimalName for OtherAnimal in AnimalsSeen], dtype = object)}")
            for OtherAnimal in AnimalsSeen:
                FoundAbility[0].AbilityFunction(FoundAbility[0], OtherAnimal, FoundAbility[1])

    elif Action == "Smell":
        '''Smell.'''

        #Assume Smell Hits Every Opposing Animal Within Vision + 1 Distance Right Now, Not Through Obstacles (Can be Through Animals).
        print(f"{Animal} Smelled The Surrounding Animals: {np.array([OtherAnimal.AnimalName for OtherAnimal in VisionPlusRadius], dtype = object)}")
        Defenders = np.append(Defenders, VisionPlusRadius)
        for Defender in VisionPlusRadius:
            if Defender in Animals.InBattle:
                Animals.InBattle = np.delete(Animals.InBattle, np.where(Animals.InBattle == Defender)[0][0]) #Remove Chosen Defenders to Not Choose The Same Defender Twice.

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

        #Assume Echo Location Hits Every Opposing Animal Within Vision + 1 Distance Right Now, Not Through Obstacles (Can be Through Animals).
        print(f"{Animal} Echo Located The Surrounding Animals: {np.array([OtherAnimal.AnimalName for OtherAnimal in VisionPlusRadius], dtype = object)}")
        Defenders = np.append(Defenders, VisionPlusRadius)
        for Defender in VisionPlusRadius:
            if Defender in Animals.InBattle:
                Animals.InBattle = np.delete(Animals.InBattle, np.where(Animals.InBattle == Defender)[0][0]) #Remove Chosen Defenders to Not Choose The Same Defender Twice.

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

        #Fear (Assuming if Animal Sees Opposing Animals, The Opposing Animals See Animal).
        FoundAbility = Animals.FindAbility("Fear", Animal.AbilityTypes, Action)
        if FoundAbility is not None:
            print(f"Surrounding Animals Heard & Feared {Animal}'s Bark: {np.array([OtherAnimal.AnimalName for OtherAnimal in AnimalsSeen], dtype = object)}")
            for OtherAnimal in AnimalsSeen:
                FoundAbility[0].AbilityFunction(FoundAbility[0], OtherAnimal, FoundAbility[1])

    elif Action == "Cut Trees":
        '''Cut Trees.'''
        print(f"Trees That {Animal} Could Cut: {ObstaclesBeside}")
        DestroyObstacle = np.array([-1, -1], dtype = np.int32)
        #Does Not Care if an Animal is on The Obstacle
        while not(any(np.array_equal(DestroyObstacle, ValidObstacle) for ValidObstacle in ObstaclesBeside)):
            DestroyObstacle = input(f"Which Tree Should {Animal} Choose to Cut From {ObstaclesBeside}? ")
        Grid2D[DestroyObstacle[0]][DestroyObstacle[1]][0] = ""
        print(f"{Animal} Cut a Tree at {DestroyObstacle}.")

        #Should Always be in ["T", "", AnimalObject]
        if Grid2D[DestroyObstacle[0]][DestroyObstacle[1]][1] == "T":
            Grid2D[DestroyObstacle[0]][DestroyObstacle[1]][1] = ""

        '''Determine Who The Animal Can See (Using Camoflauge, Night Vision).'''
        AttackRadiusAnimals, VisionPlusRadius, ValidMovements, ObstaclesBeside, AnimalsSeen = AnimalSight(Animal, Grid2D, DayNight)

    return Action, Grid2D, AttackRadiusAnimals, VisionPlusRadius, ValidMovements, ObstaclesBeside, AnimalsSeen, Defenders

'''Perform an Attack Action.'''
def AttackAction(Animal, AttackRadiusAnimals):

    Defenders = np.array([], dtype = object)
    if Animal.AttackTypes != {}:
        '''Attack.'''

        #Choose an AttackType.
        PossibleAttacks = np.array([AttackType for AttackType in Animal.AttackTypes.keys() if AttackRadiusAnimals[AttackType].shape[0] != 1], dtype = object)

        PossibleAttackNames = np.array([Attack.AttackName for Attack in PossibleAttacks], dtype = np.str_)
        print(f"{Animal}'s Possible Attacks: {PossibleAttackNames}")
        if PossibleAttacks.shape[0] != 0:
            #Choose a Valid Attack Type
            ChosenAttackType = ""
            while ChosenAttackType not in PossibleAttackNames and ChosenAttackType.upper() != "N":
                ChosenAttackType = input(f"Which Valid Attack Should {Animal} Choose to Use (N For None)? ")

            if ChosenAttackType.upper() != "N":
                ChosenAttackType = PossibleAttacks[np.where(PossibleAttackNames == ChosenAttackType)[0][0]]
                ValidDefenders = AttackRadiusAnimals[ChosenAttackType][1:]
                ValidDefenderNames = np.array(["None"] + [Defender.AnimalName for Defender in ValidDefenders], dtype = object)
                print(f"With Chosen Attack {ChosenAttackType.AttackName}, {Animal} Could Attack: {ValidDefenderNames}")

                if ValidDefenders.shape[0] != 0:
                    #Choose Animals to Attack.
                    ChosenDefender = ""
                    while ChosenDefender not in ValidDefenderNames:
                        ChosenDefender = input(f"Which Valid Defender Should {Animal} Choose to Attack? ")
                    Defenders = np.array([AttackRadiusAnimals[ChosenAttackType][np.where(ValidDefenderNames == ChosenDefender)[0][0]]], dtype = object)

                    if ChosenAttackType.SplashDamage[0] and np.where(Defenders == "None")[0].shape[0] == 0: #Assume Splash Hits Every Seen Opposing Animal in Attack Radius Right Now, Not Through Obstacles or Animals.
                        print(f"{Animal} Splash Attacks All.")
                        Defenders = np.append(Defenders, ValidDefenders)
                        for Defender in ValidDefenders:
                            if Defender in Animals.InBattle:
                                Animals.InBattle = np.delete(Animals.InBattle, np.where(Animals.InBattle == Defender)[0][0]) #Remove Chosen Defenders to Not Choose The Same Defender Twice.

                    else:
                        print(f"{Animal} Attacks {Defenders[0]}.")
                        #Check if Animal Chooses to Attack at All
                        if Defenders[0] in Animals.InBattle:
                            Animals.InBattle = np.delete(Animals.InBattle, np.where(Animals.InBattle == Defenders[0])[0][0]) #Remove Chosen Defenders to Not Choose The Same Defender Twice (Consistency).

                            #Attack Chosen Animals.
                            for Defender in np.array(Defenders, dtype = object):
                                Defenders = Animal.Attack(Defender, Animal.AttackTypes[ChosenAttackType][0], Defenders, ChosenAttackType) #Defender, Damage, AttackType.

                        else:
                            Defenders = np.array([], dtype = object)

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
        if Weather == "Blizzard":
            FoundAbility = Animals.FindAbility("ColdBlooded")
            FoundAbility.AbilityFunction(FoundAbility, Animal, Weather, True)

        elif Environment == "Tundra":
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
    if Animal.CurrentAbilities["Intellect"] and Environment in ("Forest", "Grasslands", "Tundra"):
        FoundAbility = Animals.FindAbility("Intellect", Animal.AbilityTypes, "None")
        FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, Environment, True)

    #Scavenger
    if Animal.CurrentAbilities["Scavenger"] and DeathGrid2D[Animal.CurrentLocation[0]][Animal.CurrentLocation[1]] > 0:
        DeathGrid2D[Animal.CurrentLocation[0]][Animal.CurrentLocation[1]] -= 1
        FoundAbility = Animals.FindAbility("Scavenger", Animal.AbilityTypes, "None")
        FoundAbility[0].AbilityFunction(FoundAbility[0], Animal, FoundAbility[1])

    #Poison (The Animal Takes Toxic Damage. Ignores Armor), Fear
    for Ability in ("Poison", "Fear"):
        if Animal.CurrentAbilities[Ability] > 0:
            FoundAbility = Animals.FindAbility(Ability)
            FoundAbility.AbilityFunction(FoundAbility, Animal, Reverse = True)

    return DeathGrid2D

def EndTurn(Animal, SkipTurn, NoMovement, Defenders, Defenders2, DeathGrid2D):

    if not(SkipTurn):
        #Append Animals Back to InBattle.
        AllAnimals = np.array(list(set(np.append(Defenders, Defenders2))), dtype = object)
        AllAnimals = np.append(AllAnimals, Animal)
        for Animal2 in AllAnimals:
            if Animal2.Health > 0:
                Animals.InBattle = np.append(Animals.InBattle, Animal2)

            else:
                print(f"{Animal2} is Dead.")
                DeathGrid2D[Animal2.CurrentLocation[0]][Animal2.CurrentLocation[1]] += 1

                #Grouping.
                AllBattlefieldAnimalsWithThisType = np.array([OtherAnimal for OtherAnimal in AllAnimals if OtherAnimal.AnimalName == Animal2.AnimalName], dtype = object)
                if AllBattlefieldAnimalsWithThisType.shape[0] > 1:
                    for SameAnimal in AllBattlefieldAnimalsWithThisType:
                        FoundAbility = Animals.FindAbility("Grouping", SameAnimal.AbilityTypes, "None")
                        if FoundAbility is not None:
                            FoundAbility[0].AbilityFunction(FoundAbility[0], SameAnimal, FoundAbility[1], Reverse = True)

    else:
        if NoMovement:
            Animal.MovementTypes = deepcopy(Animal.OriginalMovementTypes)

        if Animal.Health <= 0:
            AllBattlefieldAnimalsWithThisType = np.array([OtherAnimal for OtherAnimal in Animals.InBattle if OtherAnimal.AnimalName == Animal.AnimalName], dtype = object)
            Animals.InBattle = np.delete(Animals.InBattle, np.where(Animals.InBattle == Animal)[0][0])
            print(f"{Animal} is Dead.")
            DeathGrid2D[Animal.CurrentLocation[0]][Animal.CurrentLocation[1]] += 1

            #Grouping.
            if AllBattlefieldAnimalsWithThisType.shape[0] > 1:
                for SameAnimal in AllBattlefieldAnimalsWithThisType:
                    FoundAbility = Animals.FindAbility("Grouping", SameAnimal.AbilityTypes, "None")
                    if FoundAbility is not None:
                        FoundAbility[0].AbilityFunction(FoundAbility[0], SameAnimal, FoundAbility[1], Reverse = True)

    return DeathGrid2D

def main():

    #Create Attack Types + Ability Types
    CreateAttackAbilityTypes()

    #Create 1 of Every Animal For Later Copies
    CreateEachAnimal()

    #Create Players + Player Decks
    Player1, Player2 = input("Player 1 Name: "), input("Player 2 Name: ")
    MaxDeckSize1, MaxDeckSize2 = 12, 12 #Change Deck Sizes Here
    CreateAnimalDeck(Player1, MaxDeckSize1)
    CreateAnimalDeck(Player2, MaxDeckSize2)

    #Choose Environment, Weather / Natural Disaster, Time of Day.
    Environment, Weather, DayNight, Grid2D, DeathGrid2D = CreateEnvironmentGrid()

    Turn = 1
    GameOver = False
    LastTurnPlus = 21
    while not(GameOver) and Turn < LastTurnPlus: #Change Turn Count Here

        #Check if Game Over (Game Ends When at Least One Player Has no Animals on The Battlefield)
        Player1Animals = [Animal for Animal in Animals.InBattle if Animal.Player == Player1]
        Player2Animals = [Animal for Animal in Animals.InBattle if Animal.Player == Player2]
        if Turn == 1 or (Player1Animals != [] and Player2Animals != []):
            print(f"\nTurn {Turn}:")

            #Print The Stats of All Animals Starting The Turn.
            Animals.PrintAllAnimalsInBattle()

            #Players Can Place an Animal This Turn or Not
            AddAnimalToGrid(Player1, MaxDeckSize1, Grid2D)
            AddAnimalToGrid(Player2, MaxDeckSize2, Grid2D)

            '''Update Join-Battle Effects.'''
            JoinBattleEffects()

            #All Animals Attack a Random Opposing Animal
            for Animal in np.array(Animals.InBattle, dtype = object):
                SkipTurn = False
                NoMovement = False

                if Animal.Health > 0:

                    '''Animal Turn Start, Update Effects.'''
                    print(f"\nPlayer {Animal.Player}'s {Animal}'s Turn.")
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

            Turn += 1

        else:
            GameOver = True

            #Print The Winner
            if Player1Animals == [] and Player2Animals == []:
                print("The Game is a Tie!")
            elif Player1Animals == []:
                print(f"Player {Player2} Wins!")
            elif Player2Animals == []:
                print(f"Player {Player1} Wins!")

    #Print That The Time Ran Out
    if Turn == LastTurnPlus:
        print("Game Ran Out of Time! The Game is a Tie!")

main()