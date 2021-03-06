#made deviousname with OpenAI Playground using this prompt structure (and some tuned Playground parameters):
"""
1. Create an Ant Farm simulator with Python
2. Create a new Class which generates a Queen Ant with random genetic traits.
    - She can lay eggs and will eventually die and need to be replaced.
    - She has 3 types of children: Worker, Drone, and Soldier
    - Workers help the colony survive by finding food and tending to the eggs.
    - Drones help the species survive by creating new distant colonies (more on these later).
    - Soldiers help the colony survive by protecting it with fighting prowess.
3. Genetic traits will be:
    - Life span (LS) (All)
    - Number of eggs per day (EPD) (Queens)
    - Number of days before first egg (DBE) (Drones)
    - Work Ability (AB) (Workers)
    - Fight Ability (FB) (Soldiers)
    A genetic dictionary looks like this: worker_3 = {"Type":"Worker", "Genetics":f'LS:{LS} EPD:"none" DBE:"none" AB:{AB} FB:{FB}'}
    Which can then become part of the colony dictionary like so: colony = {"Queen":QUEEN, "Drones":{drone_1}, "Workers":{worker_1, worker_2, worker_3}, "Soldiers":{soldier_1, soldier_2}}
4. A 2-D array can be used for the ant farm, and ant locations need to be tracked.
5. The Queen will lay eggs in a random location in the ant farm, and the eggs will hatch after a random number of days.
6. Workers will find food (represented by a '*') and bring it back to the Queen.
7. Soldiers will attack any other ants they encounter, and if they win, they will eat them.
8. Drones will fly to a random location in the ant farm and create a new colony there.
9. Ants cannot move through walls or other ants.
10. Ants can only move one space at a time, but can move in any direction.
11. The simulation ends when the Queen dies or there are no more ants left in the colony.
"""
import random
import time
import os

class Ant:

    def __init__(self, type_of_ant, life_span, num_eggs_per_day, num_days_before_first_egg, work_ability, fight_ability):
        self.type = type_of_ant
        self.life_span = life_span
        self.num_eggs_per_day = num_eggs_per_day
        self.num_days_before_first_egg = num_days_before_first_egg
        self.work_ability = work_ability
        self.fight_ability = fight_ability

    def getType(self):
        return self.type

    def getLifeSpan(self):
        return self.life_span

    def getNumEggsPerDay(self):
        return self.num_eggs_per_day

    def getNumDaysBeforeFirstEgg(self):
        return self.num_days_before_first_egg

    def getWorkAbility(self):
        return self.work_ability

    def getFightAbility(self):
        return self.fight_ability

    def setLifeSpan(self, new_life_span):
        self.life_span = new_life_span

    def setNumEggsPerDay(self, new_num_eggs_per_day):
        self.num_eggs_per_day = new_num_eggs_per_day

    def setNumDaysBeforeFirstEgg(self, new_num_days_before_first_egg):
        self.num_days_before_first_egg = new_num_days_before_first_egg

    def setWorkAbility(self, new_work_ability):
        self.work_ability = new_work_ability

    def setFightAbility(self, new_fight_ability):
        self.fight_ability = new_fight_ability

class Colony:

    def __init__(self, queen, drones, workers, soldiers):
        self.queen = queen
        self.drones = drones
        self.workers = workers
        self.soldiers = soldiers

    def getQueen(self):
        return self.queen

    def getDrones(self):
        return self.drones

    def getWorkers(self):
        return self.workers

    def getSoldiers(self):
        return self.soldiers

    def setQueen(self, newQueen):
        self.queen = newQueen

    def setDrones(self, newDrones):
        self.drones = newDrones

    def setWorkers(self, newWorkers):
        self.workers = newWorkers

    def setSoldiers(self, newSoldiers):
        self.soldiers = newSoldiers

    def addDrone(self, drone):
        self.drones[drone] = drone

    def addWorker(self, worker):
        self.workers[worker] = worker

    def addSoldier(self, soldier):
        self.soldiers[soldier] = soldier

    def removeDrone(self, drone):
        del self.drones[drone]

    def removeWorker(self, worker):
        del self.workers[worker]

    def removeSoldier(self, soldier):
        del self.soldiers[soldier]

class Farm:

    def __init__(self, farm_size, queen, drones, workers, soldiers):
        self.farm_size = farm_size
        self.colony = Colony(queen, drones, workers, soldiers)
        self.farm = [['.' for i in range(farm_size)] for j in range(farm_size)]
        self.food = [['*' for i in range(farm_size)] for j in range(farm_size)]
        self.ant_locations = {}

    def getFarmSize(self):
        return self.farm_size

    def getColony(self):
        return self.colony

    def getFarm(self):
        return self.farm

    def getFood(self):
        return self.food

    def getAntLocations(self):
        return self.ant_locations

    def setFarmSize(self, newFarmSize):
        self.farm_size = newFarmSize

    def setColony(self, newColony):
        self.colony = newColony

    def setFarm(self, newFarm):
        self.farm = newFarm

    def setFood(self, newFood):
        self.food = newFood

    def setAntLocations(self, newAntLocations):
        self.ant_locations = newAntLocations

    def addAntLocation(self, ant, location):
        self.ant_locations[ant] = location

    def removeAntLocation(self, ant):
        del self.ant_locations[ant]

    def moveAnt(self, ant, newLocation):
        oldLocation = self.ant_locations[ant]
        self.farm[oldLocation[0]][oldLocation[1]] = '.'
        self.farm[newLocation[0]][newLocation[1]] = ant.getType()[0]
        self.ant_locations[ant] = newLocation

    def placeAnt(self, ant, location):
        self.farm[location[0]][location[1]] = ant.getType()[0]
        self.ant_locations[ant] = location

    def placeFood(self, location):
        self.food[location[0]][location[1]] = '*'

    def removeFood(self, location):
        self.food[location[0]][location[1]] = '.'

    def printFarm(self):
        for i in range(self.farm_size):
            for j in range(self.farm_size):
                print(self.farm[i][j], end=' ')
            print()

    def printFood(self):
        for i in range(self.farm_size):
            for j in range(self.farm_size):
                print(self.food[i][j], end=' ')
            print()

    def runSimulation(self):
        queen = self.colony.getQueen()
        drones = self.colony.getDrones()
        workers = self.colony.getWorkers()
        soldiers = self.colony.getSoldiers()

        # Place the Queen in the center of the farm and add her to the ant locations dictionary
        queen_location = [int(self.farm_size/2), int(self.farm_size/2)]
        self.placeAnt(queen, queen_location)

        # Place the Drones in random locations around the Queen and add them to the ant locations dictionary
        for drone in drones:
            drone_location = [random.randint(0, self.farm_size-1), random.randint(0, self.farm_size-1)]
            while drone_location == queen_location:
                drone_location = [random.randint(0, self.farm_size-1), random.randint(0, self.farm_size-1)]
            self.placeAnt(drone, drone_location)

        # Place the Workers in random locations around the Queen and add them to the ant locations dictionary
        for worker in workers:
            worker_location = [random.randint(0, self.farm_size-1), random.randint(0, self.farm_size-1)]
            while worker_location == queen_location:
                worker_location = [random.randint(0, self.farm_size-1), random.randint(0, self.farm_size-1)]
            self.placeAnt(worker, worker_location)

        # Place the Soldiers in random locations around the Queen and add them to the ant locations dictionary
        for soldier in soldiers:
            soldier_location = [random.randint(0, self.farm_size-1), random.randint(0, self.farm_size-1)]
            while soldier_location == queen_location:
                soldier_location = [random.randint(0, self.farm_size-1), random.randint(0, self.farm_size-1)]
            self.placeAnt(soldier, soldier_location)

        # Place food in random locations around the farm
        for i in range(self.farm_size):
            for j in range(self.farm_size):
                if self.farm[i][j] == '.':
                    self.placeFood([i, j])

        # Run the simulation until the Queen dies or there are no more ants left in the colony
        while queen.getLifeSpan() > 0 and len(list(drones)) > 0 and len(list(workers)) > 0 and len(list(soldiers)) > 0:

            # Queen lays eggs
            for i in range(queen.getNumEggsPerDay()):
                egg_location = [random.randint(0, self.farm_size-1), random.randint(0, self.farm_size-1)]
                while egg_location == queen_location:
                    egg_location = [random.randint(0, self.farm_size-1), random.randint(0, self.farm_size-1)]
                egg = Ant('Egg', random.randint(1, 10), 0, 0, 0, 0)
                self.placeAnt(egg, egg_location)

            # Drones fly to a random location in the ant farm and create a new colony there
            for drone in drones:
                drone_location = self.ant_locations[drone]
                new_drone_location = [random.randint(0, self.farm_size-1), random.randint(0, self.farm_size-1)]
                while new_drone_location == drone_location:
                    new_drone_location = [random.randint(0, self.farm_size-1), random.randint(0, self.farm_size-1)]
                if drone.getNumDaysBeforeFirstEgg() == 0:
                    drone.setNumDaysBeforeFirstEgg(random.randint(1, 10))
                else:
                    drone.setNumDaysBeforeFirstEgg(drone.getNumDaysBeforeFirstEgg() - 1)
                self.moveAnt(drone, new_drone_location)

            # Workers find food and bring it back to the Queen
            for worker in workers:
                worker_location = self.ant_locations[worker]
                if self.food[worker_location[0]][worker_location[1]] == '*':
                    self.removeFood(worker_location)
                    self.moveAnt(worker, queen_location)

            # Soldiers attack any other ants they encounter, and if they win, they will eat them
            for soldier in soldiers:
                soldier_location = self.ant_locations[soldier]
                for ant in self.ant_locations:
                    ant_location = self.ant_locations[ant]
                    if soldier_location == ant_location and ant != soldier:
                        if soldier.getFightAbility() > ant.getFightAbility():
                            if ant == queen:
                                queen.setLifeSpan(0)
                            elif ant in drones:
                                drones[ant].setLifeSpan(0)
                            elif ant in workers:
                                workers[ant].setLifeSpan(0)
                            elif ant in soldiers:
                                soldiers[ant].setLifeSpan(0)

            # Decrement the life span of all ants by 1 day and remove dead ants from the farm and colony dictionaries
            queen.setLifeSpan(queen.getLifeSpan() - 1)
            for drone in list(drones):
                drone.setLifeSpan(drone.getLifeSpan() - 1)
                if drone.getLifeSpan() == 0:
                    drone_location = self.ant_locations[drone]
                    self.farm[drone_location[0]][drone_location[1]] = '.'
                    self.removeAntLocation(drone)
                    self.colony.removeDrone(drone)
            for worker in list(workers):
                worker.setLifeSpan(worker.getLifeSpan() - 1)
                if worker.getLifeSpan() == 0:
                    worker_location = self.ant_locations[worker]
                    self.farm[worker_location[0]][worker_location[1]] = '.'
                    self.removeAntLocation(worker)
                    self.colony.removeWorker(worker)
            for soldier in list(soldiers):
                soldier.setLifeSpan(soldier.getLifeSpan() - 1)
                if soldier.getLifeSpan() == 0:
                    soldier_location = self.ant_locations[soldier]
                    self.farm[soldier_location[0]][soldier_location[1]] = '.'
                    self.removeAntLocation(soldier)
                    self.colony.removeSoldier(soldier)

            # Print the farm and food arrays to the console and wait 1 second before the next day begins
            os.system('cls')
            print('Day', queen.getLifeSpan())
            print('Ant Farm')
            self.printFarm()
            print('Food')
            self.printFood()
            time.sleep(1)

        # Print the final results of the simulation to the console and wait 5 seconds before exiting the program
        os.system('cls')
        if queen.getLifeSpan() == 0:
            print('The Queen has died!')
        elif len(drones) == 0:
            print('There are no more Drones left in the colony!')
        elif len(workers) == 0:
            print('There are no more Workers left in the colony!')
        elif len(soldiers) == 0:
            print('There are no more Soldiers left in the colony!')
        time.sleep(5)

def main():

    # Create a Queen Ant with random genetic traits
    queen = Ant('Queen', random.randint(1, 10), random.randint(1, 10), 0, 0, 0)

    # Create Drones with random genetic traits
    drone_1 = Ant('Drone', random.randint(1, 10), 0, random.randint(1, 10), 0, 0)
    drone_2 = Ant('Drone', random.randint(1, 10), 0, random.randint(1, 10), 0, 0)
    drone_3 = Ant('Drone', random.randint(1, 10), 0, random.randint(1, 10), 0, 0)

    # Create Workers with random genetic traits
    worker_1 = Ant('Worker', random.randint(1, 10), 0, 0, random.randint(1, 10), 0)
    worker_2 = Ant('Worker', random.randint(1, 10), 0, 0, random.randint(1, 10), 0)
    worker_3 = Ant('Worker', random.randint(1, 10), 0, 0, random.randint(1, 10), 0)

    # Create Soldiers with random genetic traits
    soldier_1 = Ant('Soldier', random.randint(1, 10), 0, 0, 0, random.randint(1, 10))
    soldier_2 = Ant('Soldier', random.randint(1, 10), 0, 0, 0, random.randint(1, 10))

    # Create a Colony with the Queen and her children
    drones = {drone_1:drone_1}
    workers = {worker_1:worker_1, worker_2:worker_2, worker_3:worker_3}
    soldiers = {soldier_1:soldier_1, soldier_2:soldier_2}
    colony = Colony(queen, drones, workers, soldiers)

    # Create a Farm with the Colony and run the simulation
    farm = Farm(32, queen, drones, workers, soldiers)
    farm.runSimulation()

if __name__ == '__main__':
    main()
