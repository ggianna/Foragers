from soldiers import *
from towers import *
from economy import Economy
from output import ConsoleOutput, Output
from runGame import Game
import gamemap
import deap
import random

from deap import base
from deap import creator
from deap import tools


def EvaluateMap(chromosome = [0.00, 0.10, 0.10, 0.00] , economy = Economy(50) ):
    # Init economy and map
    economy = Economy(50);
    gameMap = gamemap.GameMap(economy, 30, 30,  *chromosome)
    output = Output()

    armies = [ Game.selectArmy(economy, gameMap, armyColor="white", output=Output(), aUnitPool= ['SoldierClass', 'TechnicianClass', 'MageClass'])
                for _ in range(2)]
    score = sum([Game(economy, gameMap, army, output, 0.0).run() for army in armies])
    print(score)

    return  score,

def printMap(params ):
    economy = Economy(50)
    gameMap = gamemap.GameMap(economy, 30, 30,  *params)
    output = ConsoleOutput()
    output.drawMap(gameMap, [],[] )
    

    print(gameMap)



creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)
toolbox = base.Toolbox()
# Attribute generator
toolbox.register("attr_float", random.uniform, 0.01, 0.2)
# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_float, n=4)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", EvaluateMap)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.5, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=4)









def main():
    random.seed(64)

    # create an initial population of 300 individuals (where
    # each individual is a list of integers)
    pop = toolbox.population(n=5)
    print pop

    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB = 0.5, 0.2

    print("Start of evolution")

    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    print("  Evaluated %i individuals" % len(pop))

    # Extracting all the fitnesses of
    fits = [ind.fitness.values[0] for ind in pop]

    # Variable keeping track of the number of generations
    g = 0

    # Begin the evolution
    while  g < 10:
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)

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
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print("  Evaluated %i individuals" % len(invalid_ind))

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x * x for x in fits)
        std = abs(sum2 / length - mean ** 2) ** 0.5

        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)

    print("-- End of (successful) evolution --")

    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))


if __name__ == "__main__":
    #EvaluateMap()
    #main()
    #printMap([0.8031057995895188, 0.20136711521936546, 0.8194173185392594, 0.6529689056798653])
    printMap([0.10047006982357568, 0.12974162032058817, 0.08675258421800985, 0.18480456240850213])









