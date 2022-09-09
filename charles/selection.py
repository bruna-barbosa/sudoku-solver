from random import choice, uniform
from operator import attrgetter

import numpy
from numpy import random


def fps(population):
    """Fitness proportionate selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """
    # Sum total fitness
    total_fitness = sum([i.fitness for i in population])
    # Get a 'position' on the wheel
    spin = uniform(0, total_fitness)

    if population.optim == "max":
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += individual.fitness
            if position > spin:
                return individual

    elif population.optim == "min":
        position = total_fitness
        # Find individual in the position of the spin
        for individual in population:
            position -= individual.fitness
            if position < spin:
                return individual

    else:
        raise Exception("No optimization specified (min or max).")


def ranking(population):
    """Ranking selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """

    if population.optim == "max":
        pop_sorted = sorted(population, key=attrgetter("fitness"))
    elif population.optim == "min":
        pop_sorted = sorted(population, key=attrgetter("fitness"), reverse=True)
    else:
        raise Exception("No optimization specified (min or max).")

    probs = [(rank + 1) / sum(range(len(pop_sorted) + 1)) for rank, _ in enumerate(pop_sorted)]
    index = random.choice(len(pop_sorted), p=probs)
    return pop_sorted[index]


def tournament(population, size=10):
    """Tournament selection implementation.

    Args:
        population (Population): The population we want to select from.
        size (int): Size of the tournament.

    Returns:
        Individual: Best individual in the tournament.
    """

    # Select individuals based on tournament size
    tournament = [choice(population.individuals) for i in range(size)]
    # Check if the problem is max or min
    if population.optim == 'max':
        return max(tournament, key=attrgetter("fitness"))
    elif population.optim == 'min':
        return min(tournament, key=attrgetter("fitness"))
    else:
        raise Exception("No optimization specified (min or max).")

