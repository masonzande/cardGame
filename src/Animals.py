import random as r #Randomization.
import InitAnimals

#Test File
def main():

    #Create The Animals + AttackTypes.
    InitAnimals.CreateAnimalsAndAttackTypes()

    #Print The Stats of All Animals Before Any Attacks.
    InitAnimals.Animals.PrintAllAnimals()

    #All Animals Attack a Random Other Animal (All if Splash)
    for Animal in list(InitAnimals.Animals.AnimalList):

        if Animal.Health > 0:

            #Remove Animal From AnimalList to Not Attack Itself.
            InitAnimals.Animals.AnimalList.remove(Animal)

            #Choose an AttackType.
            ChosenAttackType = r.choice([AttackType for AttackType in Animal.AttackTypes.keys()])

            #Choose Animals to Attack.
            if ChosenAttackType.SplashDamage[0]: #Assume Splash Hits Every Animal Right Now.
                Defenders = []
                for Defender in list(InitAnimals.Animals.AnimalList):
                    Defenders.append(Defender)
                    InitAnimals.Animals.AnimalList.remove(Defender) #Remove Chosen Defenders to Not Choose The Same Defender Twice.

            else:
                Defenders = [r.choice(InitAnimals.Animals.AnimalList)]
                InitAnimals.Animals.AnimalList.remove(Defenders[0]) #Remove Chosen Defenders to Not Choose The Same Defender Twice (Consistency).

            #Attack Chosen Animals.
            for Defender in Defenders:
                Defenders = Animal.Attack(Defender, Animal.AttackTypes[ChosenAttackType][0], Defenders, ChosenAttackType) #Defender, Damage, AttackType.

            #Append Animals Back to AnimalList.
            [InitAnimals.Animals.AnimalList.append(Defender) for Defender in Defenders]
            InitAnimals.Animals.AnimalList.append(Animal)

            #Print The Stats of All Animals After The Attack.
            InitAnimals.Animals.PrintAllAnimals()

main()