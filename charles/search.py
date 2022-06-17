from random import randint, sample


def single_point_co(p1, p2):
    """Implementation of single point crossover.
    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.
    Returns:
        Individuals: Two offsprings, resulting from the crossover.
    """
    co_point = randint(1, len(p1)-2)

    offspring1 = p1[:co_point] + p2[co_point:]
    offspring2 = p2[:co_point] + p1[co_point:]

    return offspring1, offspring2


def multi_point_co(p1, p2):
    """Implementation of single point crossover.
    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.
    Returns:
        Individuals: Two offsprings, resulting from the crossover.
    """

    co_points = sample(range(1, len(p1)-2), 2)
    co_points.sort()

    offspring1 = p1[:co_points[0]] + p2[co_points[0]:co_points[1]] + p1[co_points[1]:]
    offspring2 = p2[:co_points[0]] + p1[co_points[0]:co_points[1]] + p2[co_points[1]:]

    return offspring1, offspring2


def cycle_co(p1, p2):
    """Implementation of cycle crossover.
    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.
    Returns:
        Individuals: Two offsprings, resulting from the crossover.
    """

    # Offspring placeholders - None values make it easy to debug for errors
    offspring1 = [None] * len(p1)
    offspring2 = [None] * len(p2)
    # While there are still None values in offspring, get the first index of
    # None and start a "cycle" according to the cycle crossover method
    while None in offspring1:
        index = offspring1.index(None)

        val1 = p1[index]
        val2 = p2[index]

        while val1 != val2:
            offspring1[index] = p1[index]
            offspring2[index] = p2[index]
            val2 = p2[index]
            index = p1.index(val2)

        for element in offspring1:
            if element is None:
                index = offspring1.index(None)
                if offspring1[index] is None:
                    offspring1[index] = p2[index]
                    offspring2[index] = p1[index]

    return offspring1, offspring2


def uniform_co(p1, p2):
    """Implementation of cycle crossover.
    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.
    Returns:
        Individuals: Two offsprings, resulting from the crossover.
    """

    if len(p1) != len(p2):
        raise Exception("Parents' lengths are not equal.")

    length = len(p1)

    # Offspring placeholders - None values make it easy to debug for errors
    offspring1 = [None] * length
    offspring2 = [None] * length
    # While there are still None values in offspring, get the first index of
    # None and start a "cycle" according to the cycle crossover method
    for index in range(length):
        if randint(0, 1) == 0:
            offspring1[index] = p1[index]
            offspring2[index] = p2[index]
        else:
            offspring1[index] = p2[index]
            offspring2[index] = p1[index]

    return offspring1, offspring2


if __name__ == '__main__':
    p1, p2 = [2, 7, 4, 3, 1, 5, 6, 9, 8], [1, 2, 3, 4, 5, 6, 7, 8, 9]
    o1, o2 = cycle_co(p1, p2)
