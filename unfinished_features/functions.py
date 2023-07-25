from easygui import *
import random
from Fitness import Fitness
import operator
# generate a window to get information necessary for algorithm


def detail_info():
    try:
        good = True
        fieldValues = multenterbox("Insert starting conditions", "Genetic algorithm",
                                   ["Chromosomes in generation", "Heritage fragment size (x > 0 and x < 1)",
                                    "Mutation value (x>0 and x<1)", "What type of box do you want to pick (dang, radi, norm, frag, flam)",
                                    "How many generations"])
        if fieldValues[0] is None:
            return 0
        if not (fieldValues[0].isnumeric() and (fieldValues[0] != "")):
            good = False
            msgbox("Value is not a number", "Error")

        if isinstance(float(fieldValues[1]), float) and (fieldValues[1] != ""):
            if (float(fieldValues[1]) <= 0) and good and (float(fieldValues[1]) >= 1):
                msgbox("Wrong fragment number")
                good = False
        elif good:
            msgbox("Value is not a number", "Error")
            good = False

        if isinstance(float(fieldValues[2]), float) and (fieldValues[2] != ""):
            if (float(fieldValues[1]) <= 0) and good and (float(fieldValues[1]) >= 1):
                msgbox("Wrong mutation value")
                good = False
        elif good:
            msgbox("Value is not a number", "Error")
            good = False

        if fieldValues[3] not in ['dang', 'radi', 'norm', 'frag', 'flam']:
            msgbox("Value is not a number", "Error")
            good = False

        if good:
            return [fieldValues[0], fieldValues[1], fieldValues[2], fieldValues[3], fieldValues[4]]

        if not (fieldValues[4].isnumeric() and (fieldValues[4] != "")):
            msgbox("Value is not a number", "Error")
            good = False

        if good:
            return [fieldValues[0], fieldValues[1], fieldValues[2], fieldValues[3], fieldValues[4]]
    except:
        return 0


def createRoute(allBoxes, allShelves):
    boxes = []
    shelves = []
    routes = []
    for box in allBoxes:
        boxes.append(box)
    for shelf in allShelves:
        shelves.append(shelf)
    randBoxes = random.sample(boxes, len(boxes))
    randShelves = random.sample(shelves, len(shelves))
    for num, shelf in enumerate(randShelves):
        if shelf.type == randBoxes[num].type:
            routes.append((shelf, randBoxes[num]))
    return routes


def initialPopulation(popSize, allBoxes, allShelves):
    population = []
    for i in range(0, popSize):
        population.append(createRoute(allBoxes, allShelves))
    return population


def rankRoutes(population):
    fitnessResults = {}
    for i in range(0, len(population)):
        fitnessResults[i] = Fitness(population[i]).routeFitness()
    return sorted(fitnessResults.items(), key=operator.itemgetter(1), reverse=True)