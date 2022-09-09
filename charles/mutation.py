from random import choice, sample, shuffle


def random_resetting(individual, mutable_indexes, valid_set):
    """Replace mutation for a GA individual

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    # Get a mutation point
    mut_point = choice(mutable_indexes)
    # Mutate it
    individual[mut_point] = choice(valid_set)
    return individual


def swap(individual, mutable_indexes, valid_set):
    """Swap mutation for a GA individual

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    # Get two mutation points
    mut_points = sample(mutable_indexes, 2)
    # Swap them
    individual[mut_points[0]], individual[mut_points[1]] = individual[mut_points[1]], individual[mut_points[0]]

    return individual


def scramble(individual, mutable_indexes, valid_set):
    """Scramble mutation for a GA individual

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    # Get a few mutation points
    mut_points = sample(mutable_indexes, int(len(mutable_indexes)/2))
    mut_points.sort()
    values = [individual[point] for point in mut_points]
    shuffle(values)
    # Assign shuffled values
    for idx, point in enumerate(mut_points):
        individual[point] = values[idx]

    return individual


def inversion(individual, mutable_indexes, valid_set):
    """Inversion mutation for a GA individual

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    # Get a few mutation points
    mut_points = sample(mutable_indexes, int(len(mutable_indexes)/2))
    mut_points.sort()
    values = [individual[point] for point in mut_points]
    values.reverse()
    # Reverse values of mutation points
    for idx, point in enumerate(mut_points):
        individual[point] = values[idx]

    return individual
