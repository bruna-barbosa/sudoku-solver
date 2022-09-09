import plotly.graph_objects as go
from charles.charles import Population, Individual
from copy import deepcopy
from data.sudoku_data import evil, hard, simple
from charles.selection import fps, tournament, ranking
from charles.mutation import random_resetting, swap, scramble, inversion
from charles.crossover import single_point_co, multi_point_co, cycle_co, uniform_co
from numpy import std


def get_fitness(self):
    """A fitness function for the Sudoku Problem.
    Calculates the fitness of rows, columns and blocks in terms of repetition and sum

    Returns:
        int: the closer to 0 the better
    """

    rows = 0
    columns = 0
    blocks = 0

    for i in range(9):
        sum = 0
        for j in range(9):
            sum = sum + self.representation[i * 9 + j]
        rows = rows + abs(sum - 45)

    for i in range(9):
        sum = 0
        for j in range(9):
            sum = sum + self.representation[i + j * 9]
        columns = columns + abs(sum - 45)

    for box_num in range(9):
        row = 3 * int(box_num / 3)
        col = 3 * (box_num % 3)
        sum = 0
        for i in range(row, row + 3):
            for j in range(col, col + 3):
                sum = sum + self.representation[i * 9 + j]
        blocks = blocks + abs(sum - 45)

    return rows + columns + blocks


def get_neighbours(self):
    """A neighbourhood function for the Sudoku Problem.

    Returns:
        list: a list of individuals
    """
    n = [deepcopy(self.representation) for i in range(len(self.representation))]

    for count, i in enumerate(n):
        if i[count] == 1:
            i[count] = 0
        elif i[count] == 0:
            i[count] = 1

    n = [Individual(i) for i in n]
    return n


# Monkey Patching
Individual.get_fitness = get_fitness
Individual.get_neighbours = get_neighbours

def check_setting(
        size,
        gens,
        select,
        crossover,
        mutate,
        co_p,
        mu_p,
        elitism
):
    total_runs = 10
    pop = Population(
        size=size, optim="min", init_repr=deepcopy(hard), valid_set=[1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    fitness = []
    for _ in range(total_runs):
        fitness.append(
            pop.evolve(
                gens=gens,
                select=select,
                crossover=crossover,
                mutate=mutate,
                co_p=co_p,
                mu_p=mu_p,
                elitism=elitism
            )
        )


def total_check(values, folder):
    comp_figure = go.Figure()

    crossovers = [single_point_co, multi_point_co, uniform_co]
    mutations = [swap, random_resetting]

    for c, m in [
        (c, m)
        for c in crossovers
        for m in mutations
    ]:
        figure = go.Figure()
        fitness = []
        for i in range(10):
            pop = Population(
            size=500, optim="min", init_repr=deepcopy(values), valid_set=[1, 2, 3, 4, 5, 6, 7, 8, 9]
        )
            result = pop.evolve(
                gens=500,
                select=ranking,
                crossover=c,
                mutate=m,
                co_p=0.8,
                mu_p=1.0,
                elitism=True
            )
            fitness.append(result)

        results = [item[-1] for item in fitness]

        best = min(results)
        best_index = results.index(best)
        average = sum(results) / len(results)
        st_dev = std(results)

        for i, item in enumerate(fitness):
            figure.add_scatter(
                y=item,
                mode='lines',
                name=f'Test {i}'
            )

        figure.update_layout(
            title=f"{c.__name__}/{m.__name__} fitness. Best: {best}, average: {average}, std: {st_dev:.2f}",
            xaxis_title="Number of generations",
            yaxis_title="Fitness",
        )

        figure.write_image(f"{folder}/{c.__name__}_{m.__name__}.png")

        comp_figure.add_scatter(
            y=fitness[best_index],
            mode='lines',
            name=f'{c.__name__}/{m.__name__}',
        )

    comp_figure.update_layout(
        title="Fitness function comparison (best runs)",
        xaxis_title="Number of generations",
        yaxis_title="Fitness",
    )

    comp_figure.write_image(f"{folder}/comparison.png")


total_check(simple, "simple")
total_check(hard, "hard")
total_check(evil, "evil")
