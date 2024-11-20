from InitAnimals import OnSightFear, CreateGrid
import random as r

def CheckDirection(Animal, i, Vision, Direction, XY, AnimalsSeen, ValidMovements, VisionPlusRadius, Blocked, Index):

    if Direction[1] not in ["T", "R"] and not(Blocked[Index]):
        if Direction[1] != "":
            #Assume Animal Can Move Through Other Animals
            #Stop Appending to VisionPlusRadius After Vision + 1 Radius
            if i < Vision + 2:
                VisionPlusRadius.append(Direction[1])

            if i <= Direction[1].CurrentAbilities["Camoflauge"]:
                AnimalsSeen.append(Direction[1])

        else:
            #Valid Movements Are WIthin 2xMovement
            if "Walk" in Animal.MovementTypes.keys() and i <= 2 * Animal.MovementTypes["Walk"]:
                ValidMovements["Walk"].append(XY)
            if "Swim" in Animal.MovementTypes.keys() and i <= 2 * Animal.MovementTypes["Swim"]:
                ValidMovements["Swim"].append(XY)
            if "Slither" in Animal.MovementTypes.keys() and i <= 2 * Animal.MovementTypes["Slither"]:
                ValidMovements["Slither"].append(XY)
            if "Fly" in Animal.MovementTypes.keys() and i <= 2 * Animal.MovementTypes["Fly"]:
                ValidMovements["Fly"].append(XY)

    else:
        if not(Blocked[Index]):
            #Valid Movements Are WIthin 2xMovement
            if "Slither" in Animal.MovementTypes.keys() and i <= 2 * Animal.MovementTypes["Slither"]:
                ValidMovements["Slither"].append(XY)
            if "Fly" in Animal.MovementTypes.keys() and i <= 2 * Animal.MovementTypes["Fly"]:
                ValidMovements["Fly"].append(XY)
            Blocked[Index] = True

    return AnimalsSeen, VisionPlusRadius, Blocked, ValidMovements

def AnimalSight(Animal, Grid2D, DayNight):

    '''Determine Who The Animal Can See (Using Camoflauge, Night Vision).'''
    Vision = Animal.CurrentAbilities["Night Vision"] if DayNight == "Night" else 2 + Animal.CurrentAbilities["Night Vision"]

    AnimalsSeen = []
    AttackRadiusAnimals = {Attack: [] for Attack in Animal.AttackTypes}
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
    Blocked = [False, False, False, False]

    MaxMove = max([Move for Move in Animal.MovementTypes.values()])

    for i in range(1, max(2 * Vision + 1, 2 * MaxMove + 1)):
        #Animal in Position Left, Right, up, Down i, Append to Seen if Camoflauge Does Not Impede Vision
        XYs = ((Animal.CurrentLocation[0] - i, Animal.CurrentLocation[1]), (Animal.CurrentLocation[0] + i, Animal.CurrentLocation[1]), (Animal.CurrentLocation[0], Animal.CurrentLocation[1] + i), (Animal.CurrentLocation[0], Animal.CurrentLocation[1] - i))
        for Index in range(len(XYs)):
            XY = XYs[Index]

            #Check That This is a Valid Grid Point
            if XY[0] >= 0 and XY[1] >= 0 and XY[0] < len(Grid2D) and XY[1] < len(Grid2D[0]):
                Direction = Grid2D[XY[0]][XY[1]]
                SaveBlock = Blocked[Index]
                AnimalsSeen, VisionPlusRadius, Blocked, ValidMovements = CheckDirection(Animal, i, Vision, Direction, XY, AnimalsSeen, ValidMovements, VisionPlusRadius, Blocked, Index)

                #Animal Can Only See Animals up to Radius Vision
                if i == Vision:
                    SaveAnimalsSeen = list(AnimalsSeen)

                #First Obstacle in This Direction Just Found
                if SaveBlock != Blocked[Index]:
                    #Check if Animal is Right Next to This Obstacle
                    if i == 1:
                        ObstaclesBeside.append(XY)

                    #Check if Animal Can Climb This Obstacle
                    if "Climb" in Animal.MovementTypes.keys() and i <= Animal.MovementTypes["Climb"]:
                        ValidMovements["Climb"].append(XY)

                    #Check if Animal Can Jump This Obstacle
                    if "Jump" in Animal.MovementTypes.keys() and i < Animal.MovementTypes["Jump"]:
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
            if i == Attack.AttackRadius:
                AttackRadiusAnimals[Attack] = list(AnimalsSeen)

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