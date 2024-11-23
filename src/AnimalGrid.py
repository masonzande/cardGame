from InitAnimals import OnSightFear, CreateGrid
import random as r

def CheckDirection(Animal, i, Vision, Direction, XY, AnimalsSeen, ValidMovements, VisionPlusRadius, ObstacleBlocked, AnimalBlocked, Index):

    if Direction[1] not in ["T", "R"] and not(ObstacleBlocked[Index]):
        #Check if This Square is an Animal
        if Direction[1] != "":
            #Square is an Animal

            #Stop Appending Opposing Animals to VisionPlusRadius After Vision + 1 Radius
            if i < Vision + 2 and Animal.Player != Direction[1].Player:
                VisionPlusRadius.append(Direction[1])

            #Effects Only Occur to Seen Opposing Animals
            if not(AnimalBlocked[Index]):
                #Empty Path to This Square. This Square is an Animal
                if i <= Direction[1].CurrentAbilities["Camoflauge"] and Animal.Player != Direction[1].Player:
                    AnimalsSeen.append(Direction[1])

                #Animals Are Blocks
                AnimalBlocked[Index] = True

        else:
            #Square is Empty
            #Valid Movements Are Within 2xMovement
            if "Walk" in Animal.MovementTypes.keys() and i <= 2 * Animal.MovementTypes["Walk"] and not(AnimalBlocked[Index]):
                #Empty Path to This Square, Including Square
                ValidMovements["Walk"].append(XY)
            if "Swim" in Animal.MovementTypes.keys() and i <= 2 * Animal.MovementTypes["Swim"] and not(AnimalBlocked[Index]):
                #Empty Path to This Square, Including Square
                ValidMovements["Swim"].append(XY)
            if "Slither" in Animal.MovementTypes.keys() and i <= 2 * Animal.MovementTypes["Slither"] and not(AnimalBlocked[Index]):
                #Empty Path to This Square, Including Square
                ValidMovements["Slither"].append(XY)
            if "Fly" in Animal.MovementTypes.keys() and i <= 2 * Animal.MovementTypes["Fly"]:
                #Maybe Empty Path to This Square (Can Fly Over Animals), Empty Square
                ValidMovements["Fly"].append(XY)

    else:
        if not(ObstacleBlocked[Index]) and not(AnimalBlocked[Index]):
            #Empty Path to This Square. This Square is an Obstacle

            #Check if There is an Animal on This Obstacle
            if Direction[1] not in ["T", "R", ""]:
                #Empty Path to This Square. This Square Also Has an Animal
                AnimalBlocked[Index] = True

            else:
                #Empty Path to This Square. This Square is Just an Obstacle
                #Valid Movements Are Within 2xMovement
                if "Slither" in Animal.MovementTypes.keys() and i <= 2 * Animal.MovementTypes["Slither"]:
                    ValidMovements["Slither"].append(XY)
                if "Fly" in Animal.MovementTypes.keys() and i <= 2 * Animal.MovementTypes["Fly"]:
                    ValidMovements["Fly"].append(XY)

            ObstacleBlocked[Index] = True

    return AnimalsSeen, VisionPlusRadius, ObstacleBlocked, AnimalBlocked, ValidMovements

def AnimalSight(Animal, Grid2D, DayNight):

    '''Determine Who The Animal Can See (Using Camoflauge, Night Vision).'''
    Vision = Animal.CurrentAbilities["Night Vision"] if DayNight == "Night" else 2 + Animal.CurrentAbilities["Night Vision"]

    AnimalsSeen = []
    AttackRadiusAnimals = {Attack: ["None"] for Attack in Animal.AttackTypes}
    VisionPlusRadius = []
    ObstaclesBeside = []
    ValidMovements = {
        "Walk": [],
        "Slither": [],
        "Climb": [],
        "Jump": [],
        "Swim": [],
        "Fly": []
    }
    ObstacleBlocked = [False, False, False, False]
    AnimalBlocked = [False, False, False, False]

    MaxMove = max([Move for Move in Animal.MovementTypes.values()])

    for i in range(1, max(2 * Vision + 1, 2 * MaxMove + 1)):
        #Animal in Position Left, Right, up, Down i, Append to Seen if Camoflauge Does Not Impede Vision
        XYs = ((Animal.CurrentLocation[0] - i, Animal.CurrentLocation[1]), (Animal.CurrentLocation[0] + i, Animal.CurrentLocation[1]), (Animal.CurrentLocation[0], Animal.CurrentLocation[1] + i), (Animal.CurrentLocation[0], Animal.CurrentLocation[1] - i))
        for Index in range(len(XYs)):
            XY = XYs[Index]

            #Check That This is a Valid Grid Point
            if XY[0] >= 0 and XY[1] >= 0 and XY[0] < len(Grid2D) and XY[1] < len(Grid2D[0]):
                Direction = Grid2D[XY[0]][XY[1]]
                SaveObsBlock = ObstacleBlocked[Index]
                SaveAnBlock = AnimalBlocked[Index]
                AnimalsSeen, VisionPlusRadius, ObstacleBlocked, AnimalBlocked, ValidMovements = CheckDirection(Animal, i, Vision, Direction, XY, AnimalsSeen, ValidMovements, VisionPlusRadius, ObstacleBlocked, AnimalBlocked, Index)

                #Animal Can Only See Animals up to Radius Vision
                if i == Vision:
                    SaveAnimalsSeen = list(AnimalsSeen)

                #First Obstacle in This Direction Just Found
                if SaveObsBlock != ObstacleBlocked[Index]:
                    #Check if Animal is Right Next to This Obstacle
                    if i == 1:
                        ObstaclesBeside.append(XY)

                    #Check if Animal Can Climb This Obstacle
                    if "Climb" in Animal.MovementTypes.keys() and i <= Animal.MovementTypes["Climb"] and SaveAnBlock != AnimalBlocked[Index]:
                        ValidMovements["Climb"].append(XY)

                    #Check if Animal Can Jump This Obstacle
                    if "Jump" in Animal.MovementTypes.keys() and i < Animal.MovementTypes["Jump"] and SaveAnBlock != AnimalBlocked[Index]:
                        #Determine The Other Side of This Obstacle
                        if Index == 0:
                            OtherSide = (Animal.CurrentLocation[0] - i - 1, Animal.CurrentLocation[1])

                        elif Index == 1:
                            OtherSide = (Animal.CurrentLocation[0] + i + 1, Animal.CurrentLocation[1])

                        elif Index == 2:
                            OtherSide = (Animal.CurrentLocation[0], Animal.CurrentLocation[1] + i + 1)

                        elif Index == 3:
                            OtherSide = (Animal.CurrentLocation[0], Animal.CurrentLocation[1] - i - 1)

                        #Check if OtherSide is Valid
                        if OtherSide[0] >= 0 and OtherSide[1] >= 0 and OtherSide[0] < len(Grid2D) and OtherSide[1] < len(Grid2D[0]):
                            #Check if The Other Side of This Obstacle is Free
                            if Grid2D[OtherSide[0]][OtherSide[1]][1] == "":
                                ValidMovements["Jump"].append(OtherSide)

        #When Radius Reached For AttackRadius, Collect AnimalsSeen Into AttackRadiusAnimals
        for Attack in AttackRadiusAnimals.keys(): #Assume Attack Radius is at Most 2 * Vision Radius
            #Animals on Obstacles Have to be Attacked From 1 Closer Distance Than Normal
            if i + 1 == Attack.AttackRadius:
                AttackRadiusAnimals[Attack].extend([Animal2 for Animal2 in AnimalsSeen if Grid2D[Animal2.CurrentLocation[0]][Animal2.CurrentLocation[1]][0] in ["T", "R"]])

            #Animals Not on Obstacles Can be Attacked From Normal Distance
            elif i == Attack.AttackRadius:
                AttackRadiusAnimals[Attack].extend([Animal2 for Animal2 in AnimalsSeen if Grid2D[Animal2.CurrentLocation[0]][Animal2.CurrentLocation[1]][0] not in ["T", "R"]])


    '''Animal's Sight Changed, Update Effects.'''
    OnSightFear(Animal, SaveAnimalsSeen)

    return AttackRadiusAnimals, VisionPlusRadius, ValidMovements, ObstaclesBeside, SaveAnimalsSeen

def CreateEnvironmentGrid():

    #Map Environments to Weathers / Natural Disasters
    Environments = {
        "Tundra": ["Sun", "Clouds", "Snow", "Blizzard", "Hail", "Meteor", "Earthquake"],
        "Rainforest": ["Rain", "Sun", "Clouds", "Thunderstorm", "Earthquake", "Meteor", "Wildfire"],
        "Grasslands": ["Rain", "Sun", "Clouds", "Snow", "Thunderstorm", "Tsunami", "Drought", "Tornado", "Earthquake", "Meteor", "Wildfire"],
        "Ocean": ["Rain", "Sun", "Clouds", "Thunderstorm", "Tsunami", "Meteor"],
        "Forest": ["Rain", "Sun", "Clouds", "Snow", "Thunderstorm", "Drought", "Earthquake", "Meteor", "Wildfire"],
        "Desert": ["Sun", "Drought", "Earthquake", "Meteor"]
    }

    #Choose Environment, Weather / Natural Disaster, Time of Day.
    Environment = r.choice(list(Environments.keys()))
    Weather = r.choice(Environments[Environment])
    DayNight = r.choice(["Day", "Night"])
    print(f"Environment = {Environment}, Weather = {Weather}, DayNight = {DayNight}.")

    Grid2D, DeathGrid2D = CreateGrid(Environment)

    return Environment, Weather, DayNight, Grid2D, DeathGrid2D