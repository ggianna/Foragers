from soldiers import *
from towers import *
from economy import Economy
from output import ConsoleOutput, Output
from runGame import Game
import gamemap
import deap
import random, copy

from deap import base
from deap import creator
from deap import tools


def updateArmyWithCurrentMap(fodderArmy, newMap):
    for unit in fodderArmy:
        unit.setMap(newMap)
    return fodderArmy


def EvaluateUnit(chromosome=[0.00, 0.10, 0.10, 0.00], currentUnit = None ,currenArmy = None, gameMap = None, economy = None, unitIdx = None ):
        # Create an instance of our army, based on the original army, which we will use in a given game
        fodderArmy = copy.deepcopy(currenArmy)
        # Create a (changeable) map, based on the original map
        changeableMap = copy.deepcopy(gameMap)

        currentUnit.strategy.curiosity = chromosome[0]
        currentUnit.strategy.groupSpirit = chromosome[1]
        currentUnit.strategy.riskiness = {"SoldierClass": chromosome[2], "TrapClass": chromosome[3],
                  "TowerClass": chromosome[4]};  # Base probability to get closer to interact
        currentUnit.strategy.fasting = chromosome[5];  # Base probability to return if hungry
        currentUnit.strategy.greed = chromosome[6];  # Base probability to reach for loot, when not enough has been collected  # Update the fodder army with the altered unit
        fodderArmy[unitIdx] = currentUnit
        updateArmyWithCurrentMap(fodderArmy, changeableMap);

        # We create a new game, with the changeable map
        output = Output()
        g = Game(economy, changeableMap, fodderArmy, output, 0.0);


        score = g.run()
        return  score,




creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox = base.Toolbox()
# Attribute generator
toolbox.register("attr_float", random.random)
# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_float, n=7)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", EvaluateUnit)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.2, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=4)


def main(popsize, generations, currentUnit = None ,currenArmy = None, gameMap = None, economy = None, unitIdx = None ):
    random.seed(64)

    # create an initial population of 300 individuals (where
    # each individual is a list of integers)
    pop = toolbox.population(n=popsize)
    #print pop

    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB = 0.6, 0.5

    print("Start of evolution")

    # Evaluate the entire population
    #fitnesses = list(map(toolbox.evaluate, pop))

    fitnesses = [toolbox.evaluate(x,  currentUnit, currenArmy, gameMap, economy, unitIdx) for x in pop]
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    #print("  Evaluated %i individuals" % len(pop))

    # Extracting all the fitnesses of
    fits = [ind.fitness.values[0] for ind in pop]

    # Variable keeping track of the number of generations
    g = 0

    # Begin the evolution
    while g < generations:
        # A new generation
        g = g + 1
        # print("-- Generation %i --" % g)

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                toolbox.mate(child1, child2)

                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:

            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = [toolbox.evaluate(x,  currentUnit, currenArmy, gameMap, economy, unitIdx) for x in invalid_ind]
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        #print("  Evaluated %i individuals" % len(invalid_ind))

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x * x for x in fits)
        std = abs(sum2 / length - mean ** 2) ** 0.5

        #print("  Min %s" % min(fits))
        #print("  Max %s" % max(fits))
        #print("  Avg %s" % mean)
        #print("  Std %s" % std)

    print("-- End of (successful) evolution --")

    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
    return best_ind,best_ind.fitness.values[0]


if __name__ == "__main__":

    economy = Economy()
    output = Output()
    curmap = gamemap.GameMap(economy)

    army = Game.selectArmy(economy, curmap, armyColor="white", output=Output(),
                    aUnitPool=['SoldierClass', 'TechnicianClass', 'MageClass'])
    scores = []
    for index, unit in enumerate(army):
        print "Treasures:",len(curmap.treasures),

        evolvedParams, best = main(popsize=100, generations=20,  currentUnit = army[index] ,currenArmy = army, gameMap = curmap, economy = economy, unitIdx = index)
        scores.append(( best, evolvedParams))
        army[index].strategy.curiosity = evolvedParams[0]
        army[index].strategy.groupSpirit = evolvedParams[1]
        army[index].strategy.riskiness = {"SoldierClass": evolvedParams[2], "TrapClass": evolvedParams[3],
                                          "TowerClass": evolvedParams[4]};  # Base probability to get closer to interact
        army[index].strategy.fasting = evolvedParams[5];  # Base probability to return if hungry
        army[index].strategy.greed = evolvedParams[6]
        for u in army[:5]:
            print u.strategy.curiosity

    scores.sort(reverse=True)
    for score in scores[:5]:
        print(score)

    


