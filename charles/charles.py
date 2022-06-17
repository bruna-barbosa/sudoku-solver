from typing import List
from random import shuffle, choice, sample, random
from operator import attrgetter
from copy import deepcopy
import sys


class Individual:
    def __init__(
        self,
        representation=None,
        valid_set=None,
        init_repr=None,
        mutable_indexes=None,
    ):
        if representation is None:
            self.representation = init_repr
            for i in mutable_indexes:
                self.representation[i] = choice(valid_set)
        else:
            self.representation = representation
        self.fitness = self.get_fitness()

    def get_fitness(self):
        raise Exception("You need to monkey patch the fitness path.")

    def get_neighbours(self, func, **kwargs):
        raise Exception("You need to monkey patch the neighbourhood function.")

    def index(self, value):
        return self.representation.index(value)

    def __len__(self):
        return len(self.representation)

    def __getitem__(self, position):
        return self.representation[position]

    def __setitem__(self, position, value):
        self.representation[position] = value

    def __repr__(self):
        return f"Individual(size={len(self.representation)}); Fitness: {self.fitness}"


class Population:
    def __init__(self, size, optim, **kwargs):
        self.individuals = []
        self.size = size
        self.optim = optim
        self.init_repr = kwargs["init_repr"]
        self.valid_set = kwargs["valid_set"]
        self.mutable_indexes = []
        for i, v in enumerate(self.init_repr):
            if v == 0:
                self.mutable_indexes.append(i)

        for _ in range(size):
            self.individuals.append(
                Individual(
                    valid_set=list(self.valid_set),
                    init_repr=self.init_repr,
                    mutable_indexes=self.mutable_indexes,
                )
            )

    def evolve(self, gens, select, crossover, mutate, co_p, mu_p, elitism):
        best_individuals = []
        for gen in range(gens):
            new_pop = []

            if elitism:
                if self.optim == "max":
                    elite = deepcopy(max(self.individuals, key=attrgetter("fitness")))
                elif self.optim == "min":
                    elite = deepcopy(min(self.individuals, key=attrgetter("fitness")))

            while len(new_pop) < self.size:
                parent1, parent2 = select(self), select(self)
                # Crossover
                if random() < co_p:
                    offspring1, offspring2 = crossover(parent1, parent2)
                else:
                    offspring1, offspring2 = parent1, parent2
                # Mutation
                if random() < mu_p:
                    offspring1 = mutate(offspring1, self.mutable_indexes, self.valid_set)
                if random() < mu_p:
                    offspring2 = mutate(offspring2, self.mutable_indexes, self.valid_set)

                new_pop.append(Individual(representation=offspring1))
                if len(new_pop) < self.size:
                    new_pop.append(Individual(representation=offspring2))

            if elitism:
                if self.optim == "max":
                    least = min(new_pop, key=attrgetter("fitness"))
                elif self.optim == "min":
                    least = max(new_pop, key=attrgetter("fitness"))
                new_pop.pop(new_pop.index(least))
                new_pop.append(elite)

            self.individuals = new_pop

            if self.optim == "max":
                best_individuals.append(max(self, key=attrgetter("fitness")))

            elif self.optim == "min":
                best_individuals.append(min(self, key=attrgetter("fitness")).fitness)
                if best_individuals[-1] == 0:
                    return best_individuals

        return best_individuals

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]

    def __repr__(self):
        return f"Population(size={len(self.individuals)}, individual_size={len(self.individuals[0])})"
