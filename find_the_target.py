import random
import sys
import math

DIRECTIONS = {"LEFT": [-1, 0], "UP_LEFT": [-1, 1], "UP": [0, 1],
              "UP_RIGHT": [1, 1], "RIGHT": [1, 0], "DOWN_RIGHT": [1, -1],
              "DOWN": [0, -1], "DOWN_LEFT": [-1, -1]}
BOARD_SIZE = [40, 40]

class Agent:

    def __init__(self, dna_length, position=[0, 0]):
        self.__fitness = sys.maxint
        self.__position = position
        self.__dna = DNA(dna_length, randomize=True)

    def get_fitness(self):
        return self.__fitness

    def get_dna(self):
        return self.__dna.get_genes()

    def get_position(self):
        return self.__position

    def walk(self):
        for key in self.__dna.get_genes():
            new_position = [self.__position[0] + DIRECTIONS[key][0],
                            self.__position[1] + DIRECTIONS[key][1]]

            if (new_position[0] < BOARD_SIZE[0] and
                new_position[1] < BOARD_SIZE[1] and
                new_position[0] >= 0 and
                new_position[1] >= 0):
                self.__position = new_position

    def calculate_fitness(self, target_position):
        self.__fitness = math.hypot(target_position[0] - self.__position[0],
                                    target_position[1] - self.__position[1])

class DNA:

    def __init__(self, length, randomize=False, genes=[]):
        if randomize:
            self.__genes = [random.choice(DIRECTIONS.keys())
                            for x in range(length)]
        else:
            self.__genes = genes

        self.__length = length

    def get_genes(self):
        return self.__genes


class Population:

    def __init__(self, dna_length, size, mutation_rate,
                 initial_position, target_position, selection_rate):

        self.__agents = [Agent(dna_length, position=initial_position)
                         for _ in range(size)]
        self.__target_position = target_position

    def get_agents(self):
        return self.__agents

    def walk(self):
        for agent in self.__agents:
            agent.walk()
            print agent.get_dna()
            print agent.get_position()

    def calculate_fitness(self):
        for agent in self.__agents:
            agent.calculate_fitness(self.__target_position)
            print agent.get_fitness()

    def select_reproduce(self):
        self.__agents = sorted(self.__agents,
                               key=lambda agent: agent.get_fitness())
        print [x.get_fitness() for x in self.__agents]



class GeneticAlgorithm:

    def __init__(self, dna_length, population_size, mutation_rate,
                 initial_position, target_position, selection_rate,
                 n_generations=sys.maxint):

        self.__population = Population(dna_length, population_size,
                                       mutation_rate, initial_position,
                                       target_position, selection_rate)
        self.__n_generations = n_generations

    def run(self):
        for x in range(1):
            self.__population.walk()
            self.__population.calculate_fitness()
            self.__population.select_reproduce()


if __name__ == "__main__":

    dna_length = 5
    n_generations = 10
    population_size = 10
    mutation_rate = 0.01
    selection_rate = 0.2
    initial_position = [0, 0]
    target_position = [2, 0]

    ga = GeneticAlgorithm(dna_length, population_size, mutation_rate,
                          initial_position, target_position, selection_rate,
                          n_generations)
    ga.run()
