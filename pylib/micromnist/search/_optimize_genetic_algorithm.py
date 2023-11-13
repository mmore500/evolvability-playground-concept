import random
import typing

from deap import base as deap_base, creator as deap_creator, tools as deap_tools
import numpy as np
import tensorflow
from tqdm import tqdm

from ..sample import sample_images_value_distribution_unif


# adapted from https://deap.readthedocs.io/en/master/examples/ga_onemax_numpy.html
def _cxTwoPointCopy(ind1, ind2):
    """Execute a two points crossover with copy on the input individuals. The
    copy is required because the slicing in numpy returns a view of the data,
    which leads to a self overwriting in the swap operation. It prevents
    ::

        >>> import numpy
        >>> a = numpy.array((1,2,3,4))
        >>> b = numpy.array((5,6,7,8))
        >>> a[1:3], b[1:3] = b[1:3], a[1:3]
        >>> print(a)
        [1 6 7 4]
        >>> print(b)
        [5 6 7 8]
    """
    size = len(ind1)
    cxpoint1 = random.randint(1, size)
    cxpoint2 = random.randint(1, size - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else:  # Swap the two cx points
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] = (
        ind2[cxpoint1:cxpoint2].copy(),
        ind1[cxpoint1:cxpoint2].copy(),
    )

    return ind1, ind2


def optimize_genetic_algorithm(
    model: tensorflow.keras.Model,
    sample_strategy: typing.Callable = sample_images_value_distribution_unif,
    n_steps: int = 10000,
    population_size: int = 1000,
    crossover_probability: float = 0.7,
    mutation_probability: float = 0.2,
    progress_apply: typing.Callable = tqdm,
    pessimize: bool = False,
) -> typing.Tuple[np.ndarray, int, float]:
    # Define fitness function for batch evaluation
    def evaluate(index_population):
        predictions = model.predict(real_population)
        fitnesses = np.max(predictions, axis=1)
        if pessimize:
            fitnesses *= -1
        return fitnesses[np.array(index_population).ravel()]

    # Crossover operation on real population using indices
    def crossover(ind1, ind2):
        # Perform crossover on the actual individuals in the real population
        return _cxTwoPointCopy(
            real_population[ind1[0]].flat, real_population[ind2[0]].flat
        )

    # Mutation function
    def mutate(index):
        # crossover with a randomly generated individual
        _cxTwoPointCopy(sample_strategy().flat, real_population[index[0]].flat)
        return (index,)

    # DEAP setup
    deap_creator.create("FitnessMax", deap_base.Fitness, weights=(1.0,))
    deap_creator.create("Individual", list, fitness=deap_creator.FitnessMax)

    toolbox = deap_base.Toolbox()
    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", crossover)
    toolbox.register("mutate", mutate)
    toolbox.register("select", deap_tools.selTournament, tournsize=3)

    # Initialize the real population as a NumPy array
    real_population = sample_strategy(n=population_size)

    # Initialize DEAP population (indices)
    deap_population = [
        deap_creator.Individual([i]) for i in range(population_size)
    ]

    # Evolutionary loop
    for _ in progress_apply(
        range((n_steps + population_size - 1) // population_size)
    ):
        # Evaluate the entire population
        fitnesses = evaluate(deap_population)
        for ind, fit in zip(deap_population, fitnesses):
            ind.fitness.values = (fit,)

        # Select and clone the next generation indices
        offspring = toolbox.select(deap_population, len(deap_population))
        real_population = real_population[np.array(offspring).flat].copy()
        deap_population = [
            deap_creator.Individual([i]) for i in range(population_size)
        ]

        # Apply crossover and mutation on the real population
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if np.random.rand() < crossover_probability:
                toolbox.mate(child1, child2)

            if np.random.rand() < mutation_probability:
                toolbox.mutate(child1)
                toolbox.mutate(child2)

    # Select the best individual index
    best_index = deap_tools.selBest(deap_population, 1)[0][0]
    best_image = real_population[best_index]
    best_prediction = model.predict(np.array([best_image]))[0]
    best_confidence = np.max(best_prediction)

    return best_image, best_prediction, best_confidence
