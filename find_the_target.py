import random
import sys

DIRECTIONS = ("LEFT", "UP_LEFT", "UP", "UP_RIGHT",
              "RIGHT", "DOWN_RIGHT", "DOWN", "DOWN_LEFT")


class Agent:

    def __init__(self, dna_length, position=[0, 0]):
        self.__fitness = sys.maxint
        self.__position = position
        self.__dna = DNA(dna_length, randomize=True)

    def print_dna(self):
        print self.__dna.get_genes()


class DNA:

    def __init__(self, length, randomize=False, genes=[]):
        if randomize:
            self.__genes = [random.choice(DIRECTIONS) for x in range(length)]
        else:
            self.__genes = genes

        self.__length = length

    def get_genes(self):
        return self.__genes


class Population:

    def __init__(self, dna_length, size,
                 mutation_rate, initial_position, target_position):

        self.__population = [Agent(dna_length, position=initial_position)
                             for _ in range(size)]

class GeneticAlgorithm:

    def __init__(self, dna_length, population_size, n_generations=sys.maxint):

        self.__population = Population(dna_length, population_size,
                                       mutation_rate, initial_position,
                                       target_position)

        self.__dna_length = dna_length
        self.__population_size = population_size
        self.__n_generations = n_generations

    def run:

        for x in range(n_generations):

if __name__ == "__main__":

    dna_length = 50
    n_generations = 100
    population_size = 50
    mutation_rate = 0.01
    board_size = [40, 40]
    initial_position = [0, 0]
    target_position = [24, 25]


