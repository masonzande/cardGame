import random as r #Randomization.

#Class For Every Animal in The Game.
class Animals:

    AnimalList = [] #List of Every Animal.

    #Define an Animal Object.
    def __init__(Animal, AnimalName, Health, Armor, AttackTypes, MovementRadius, MovementTypes, Abilities, Conditions):

        #Animal Name/Health/Armor.
        Animal.AnimalName = AnimalName #String Name of The Animal. Unique.
        Animal.Health = Health #Integer. The Health of an Animal. Reaching 0 Means The Card is Removed From The Battlefield.
        Animal.Armor = Armor #Integer. Damage Done Affects Armor First. Health Cannot be Damaged When Armor Has Not Broken.
        Animals.AnimalList.append(Animal) #The Animals Class Contains a List of Every Animal

        #Animal Movement.
        Animal.MovementRadius = MovementRadius #Integer. Number of Squares That The Animal Can Move Without Being Hindered.
        Animal.MovementTypes = MovementTypes #List of String Movement Types For This Animal.

        #Animal Attacks/Abilities.
        Animal.AttackTypes = AttackTypes #{AttackType: Damage, AttackType: Damage}. {ClassObject: Damage}.
        Animal.Abilities = Abilities #List of Ability Function Pointers.
        Animal.Conditions = Conditions #List That Holds The Conditions to Activate Abilities.

    #Animal Attacks a Defender. Object Method.
    def Attack(Animal, Defender, Damage, AttackType):

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
                Animals.AnimalList.remove(Defender)

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
    def __init__(AttackType, AttackName, AttackRadius, SplashDamageBoolean):

        AttackType.AttackName = AttackName  #String Name of The Attack. Unique.
        AttackType.AttackRadius = AttackRadius #Integer. Number of Squares That The Attack Can Reach Without Being Hindered.
        AttackType.SplashDamageBoolean = SplashDamageBoolean #Boolean. Whether or Not The Attack Has Splash Damage (Not The Damage Itself).
        AttackTypes.AttackTypeList.append(AttackType) #The AttackTypes Class Contains a List of Every AttackType

#Create The Animals + Attack Types.
def CreateAnimalsAndAttackTypes():

    #Create AttackTypes.
    AttackTypes("Bite", 1, False)
    AttackTypes("Claw", 1, False)
    AttackTypes("BiteSpin", 1, False)
    AttackTypes("TailSpin", 2, True)
    AttackTypes("Punch", 1, False)

    #Create Deer.
    AnimalAttacks = {
        AttackTypes.AttackTypeList[0]: 1 #Bite, 1 Damage.
    }

    Animals("Deer", 10, 0, AnimalAttacks, 3, ["Walk"], [], []) #AnimalName, Health, Armor, AttackTypes, MovementRadius, MovementTypes, Abilities, Conditions.

    #Create Wolf.
    AnimalAttacks = {
        AttackTypes.AttackTypeList[0]: 3, #Bite, 3 Damage.
        AttackTypes.AttackTypeList[1]: 2 #Claw, 2 Damage.
    }

    Animals("Wolf", 5, 0, AnimalAttacks, 2, ["Walk"], [], []) #AnimalName, Health, Armor, AttackTypes, MovementRadius, MovementTypes, Abilities, Conditions.

#Test File
def main():

    #Create The Animals + AttackTypes.
    CreateAnimalsAndAttackTypes()

    #Print The Stats of All Animals Before Any Attacks.
    Animals.PrintAllAnimals()

    #Deer Attacks Wolf. Wolf Attacks Deer.
    for Animal in list(Animals.AnimalList):

        if Animal.Health > 0:

            #Remove Animal From AnimalList to Not Attack Itself.
            Animals.AnimalList.remove(Animal)

            #Choose an AttackType.
            ChosenAttackType = r.choice([AttackType for AttackType in Animal.AttackTypes.keys()])

            #Choose Animals to Attack.
            if ChosenAttackType.SplashDamageBoolean: #Assume Splash Hits Every Animal Right Now.
                Defenders = []
                for Defender in list(Animals.AnimalList):
                    Defenders.append(Defender)
                    Animals.AnimalList.remove(Defender) #Remove Chosen Defenders to Not Choose The Same Defender Twice.

            else:
                Defenders = [r.choice(Animals.AnimalList)]
                Animals.AnimalList.remove(Defenders[0]) #Remove Chosen Defenders to Not Choose The Same Defender Twice (Consistency).

            #Attack Chosen Animals.
            for Defender in Defenders:
                Animal.Attack(Defender, Animal.AttackTypes[ChosenAttackType], ChosenAttackType) #Defender, Damage, AttackType.

            #Append Animals Back to AnimalList.
            [Animals.AnimalList.append(Defender) for Defender in Defenders]
            Animals.AnimalList.append(Animal)

            #Print The Stats of All Animals After The Attack.
            Animals.PrintAllAnimals()

main()