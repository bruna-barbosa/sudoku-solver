from random import shuffle, choice, sample, random
from operator import attrgetter
from copy import deepcopy
from init_board import valid_init_boards

class Individual:

    def __init__(self, representation=None, valid_set=None, init_repr = None, mutable_indexes=None):
        if representation is None:
            if init_repr is None:
                ini_board = choice(valid_init_boards)
                self.representation = ini_board[0]
                self.mutable_indexes = ini_board[1]
            else:
                self.representation = init_repr
                self.mutable_indexes = mutable_indexes

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

        board = ''

        for index, item in enumerate(self.representation):
            if index % 9 == 8:
                board += str(item) + '\n'
                if (index % 8 == 2) | (index % 8 == 5):
                    board += str('---------------------') + '\n'
            elif index % 3 == 2:
                board += str(item) + ' | '
            else:
                board += str(item) + ' '

        return board + f"" \
                       f"Individual(size={len(self.representation)}); Fitness: {self.fitness}\n"

    def check_row(self, row):
        lista = [self.__getitem__(i) for i in range(row * 9, (row + 1) * 9)]

        valid_list = [j for j in lista if j != 0]

        for ind, val in enumerate(valid_list):
            if val == 0:
                pass
            else:
                for ind_, val_ in enumerate(valid_list):
                    if ind == ind_:
                        pass
                    else:
                        if val == val_:
                            return False
        return True

    def get_row_fit(self, row):

        result = 0
        for index, value in enumerate(row):
            for index_, value_ in enumerate(row):
                if index == index_:
                    pass
                else:
                    if (value == 0) | (value == value_):
                        result += 1

        return result


    def check_col(self, col):
        lista = [self.__getitem__(i) for i in range(col, 73 + col, 9)]
        valid_list = [j for j in lista if j != 0]

        for ind, val in enumerate(valid_list):
            if val == 0:
                pass
            else:
                for ind_, val_ in enumerate(valid_list):
                    if ind == ind_:
                        pass
                    else:
                        if val == val_:
                            return False
        return True

    def get_col_fit(self, col):

        result = 0
        for index, value in enumerate(col):
            for index_, value_ in enumerate(col):
                if index == index_:
                    pass
                else:
                    if (value == 0) | (value == value_):
                        result += 1

        return result


    def check_box(self, box):

        if box % 3 == 0:
            inicio = 9 * box
        else:
            if box < 3:
                inicio = 3 * box
            else:
                inicio = (3 * box - (2 * (box % 3))) * 3

        if box % 3 == 0:
            lista = [self.__getitem__(i) for i in range(inicio, 21 + inicio) if (i % 9 < 3)]

        elif box % 3 == 1:
            lista = [self.__getitem__(i) for i in range(inicio, 21 + inicio) if (i % 9 > 2) & (i % 9 < 6)]

        else:
            lista = [self.__getitem__(i) for i in range(inicio, 21 + inicio) if (i % 9 > 5)]

        valid_list = [j for j in lista if j != 0]

        for ind, val in enumerate(valid_list):
            if val == 0:
                pass
            else:
                for ind_, val_ in enumerate(valid_list):
                    if ind == ind_:
                        pass
                    else:
                        if val == val_:
                            return False
        return True


    def get_row(self, row):
        return [self.__getitem__(i) for i in range(row * 9, (row + 1) * 9)]

    def get_col(self, col):
        return [self.__getitem__(i) for i in range(col, 73 + col, 9)]

    def get_box(self, box):
        if box % 3 == 0:
            inicio = 9 * box
        else:
            if box < 3:
                inicio = 3 * box
            else:
                inicio = (3 * box - (2 * (box % 3))) * 3

        if box % 3 == 0:
            return [self.__getitem__(i) for i in range(inicio, 21 + inicio) if (i % 9 < 3)]

        elif box % 3 == 1:
            return [self.__getitem__(i) for i in range(inicio, 21 + inicio) if (i % 9 > 2) & (i % 9 < 6)]

        else:
            return [self.__getitem__(i) for i in range(inicio, 21 + inicio) if (i % 9 > 5)]


class Population:
    def __init__(self, size, optim, **kwargs):
        self.individuals = []
        self.size = size
        self.optim = optim
        self.init_repr = kwargs["init_repr"]
        self.valid_set = kwargs["valid_set"]
        self.mutable_indexes = kwargs['mutable_indexes']


        for _ in range(size):
            self.individuals.append(
                Individual(
                    valid_set=list(self.valid_set),
                    init_repr=self.init_repr,
                    mutable_indexes=self.mutable_indexes,
                )
            )

    def evolve(self, gens, select, crossover, mutate, co_p, mu_p, elitism):
        best_individual = None
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
                best_individual = max(self, key=attrgetter("fitness"))

            elif self.optim == "min":
                best_individual = min(self, key=attrgetter("fitness"))

            print(f'Best Individual gen {gen}:\n{best_individual}')

        print(best_individual.representation)
        return best_individual

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]

    def __repr__(self):
        return f"Population(size={len(self.individuals)}, individual_size={len(self.individuals[0])})"
