# -*- coding:UTF-8 -*-
import random
import time
from matplotlib import pyplot as plt


class Individual(object):
    __slots__ = ("gene", "value")

    def __init__(self, gene=None):
        if gene is None:
            self.gene = []
            for i in range(16):
                self.gene.append(random.randint(0, 1))
        else:
            self.gene = gene
        self.value = calc_fitness(self)

    @classmethod
    def crossover(cls, a, b):
        start = random.randint(0, len(a.gene) - 2)
        end = random.randint(start + 1, len(b.gene) - 1)
        a.gene[start: end], b.gene[start: end] = b.gene[start: end], a.gene[start: end]

    def mutate(self):
        index = random.randrange(0, len(self.gene))
        if self.gene[index] == 1:
            self.gene[index] = 0
        else:
            self.gene[index] = 1


def calc_fitness(individual):
    return sum(individual.gene)


def choose_stronger(individuals):
    """

    :param individuals:
    :rtype: list
    choose individuals according to fitness
    """
    individual_fitness = list(map(calc_fitness, individuals))  # return a list contain the fitness of each individual
    total_fitness = sum(individual_fitness)
    inherit_prob = [ind/total_fitness for ind in individual_fitness]

    copy_of_inherit_prob = inherit_prob[:]
    for _index in range(len(inherit_prob)):
        inherit_prob[_index] = sum(copy_of_inherit_prob[:_index + 1])
    del copy_of_inherit_prob

    chosen_individuals = []
    for i in range(len(individuals)):
        p = random.random()
        inherit_prob.append(p)
        inherit_prob.sort()
        _index = inherit_prob.index(p)
        inherit_prob.remove(p)
        chosen_individuals.append(Individual(individuals[_index].gene))

    return chosen_individuals


def create_group(size):
    """
    :param size:
    :return: list
    create first population
    """
    individuals = []
    random.seed(time.time())
    for i in range(size):
        individuals.append(Individual())

    return individuals


def generate_new_group(individuals):
    individuals = choose_stronger(individuals)
    new_group = []
    while individuals:
        length = len(individuals)
        # choose parents randomly
        i1, i2 = random.randrange(0, length), random.randrange(0, length)
        if i1 != i2:
            if i1 < i2:
                i1, i2 = i2, i1

            _a, _b = individuals.pop(i1), individuals.pop(i2)
            Individual.crossover(_a, _b)  # exchange the gene between a and b

            if random.random() <= 0.001:
                _a.mutate()
            if random.random() <= 0.001:
                _b.mutate()
            new_group.append(_a)
            new_group.append(_b)

    return new_group


def plot_graph(x, maximum, minimum, average):
    plt.ylabel('value')
    plt.xlabel('generation')
    plt.title("my first GA")
    plt.xlim(0, 101)
    plt.ylim(0, 20)
    plt.plot(x, maximum, "r--", label="maximum")
    plt.plot(x, minimum, "b--", label="minimum")
    plt.plot(x, average, "g-", label="average")
    plt.plot(x, maximum, "ro", x, minimum, "bo", x, average, "go")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    n = 100
    N = n
    s = []
    _maximum = []
    _minimum = []
    _average = []
    _individuals = create_group(64)
    for _i in _individuals:
        s += [calc_fitness(_i)]
    _maximum.append(max(s))
    _minimum.append(min(s))
    _average.append(sum(s)/64)

    while n != 0:
        s = []
        random.seed(time.time())

        new_individuals = generate_new_group(_individuals)
        for _i in new_individuals:
            s += [calc_fitness(_i)]
        _maximum.append(max(s))
        _minimum.append(min(s))
        _average.append(sum(s)/64)

        _individuals = new_individuals
        print("generation %s" % (101-n))
        n -= 1

    _x = [i for i in range(N+1)]
    plot_graph(_x, _maximum, _minimum, _average)
