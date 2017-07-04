import random
import sys
import math
import os
import time

DIRECTIONS = {"LEFT": [-1, 0], "UP_LEFT": [-1, 1], "UP": [0, 1],
              "UP_RIGHT": [1, 1], "RIGHT": [1, 0], "DOWN_RIGHT": [1, -1],
              "DOWN": [0, -1], "DOWN_LEFT": [-1, -1]}
BOARD_SIZE = [20, 20]

class Agent:

    def __init__(self, dna_length, position=[0, 0], genes=[]):
        self.__fitness = sys.maxint
        self.__position = position
        if len(genes) == 0:
            self.__dna = DNA(dna_length, randomize=True)
        else:
            self.__dna = DNA(dna_length, genes=genes)

    def get_fitness(self):
        return self.__fitness

    def get_dna(self):
        return self.__dna

    def get_position(self):
        return self.__position

    def set_position(self, position):
        self.__position = position

    def walk(self, key):
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

    def mutate(self, idx):
        self.__genes[idx] = random.choice(DIRECTIONS.keys())


class Population:

    def __init__(self, dna_length, size, initial_position, target_position):

        self.__agents = [Agent(dna_length, position=initial_position)
                         for _ in range(size)]
        self.__target_position = target_position
        self.__size = size
        self.__dna_length = dna_length
        self.__initial_position = initial_position

    def get_agents(self):
        return self.__agents

    def walk(self, board, generation):
        for i in range(self.__dna_length):
            board.run(self.__agents, self.__target_position, generation)
            for agent in self.__agents:
                agent.walk(agent.get_dna().get_genes()[i])
            #print agent.get_dna().get_genes()
            #print agent.get_position()
            board.run(self.__agents, self.__target_position, generation)

    def calculate_fitness(self):
        for agent in self.__agents:
            agent.calculate_fitness(self.__target_position)
            #print agent.get_fitness()

    def select(self, selection_rate):
        self.__agents = sorted(self.__agents,
                               key=lambda agent: agent.get_fitness())
        self.__agents = self.__agents[:int(selection_rate * self.__size)]

    def reproduce(self, mutation_rate):
        self._crossover()
        self._mutation(mutation_rate)

    def reposition(self):
        for agent in self.__agents:
            agent.set_position(self.__initial_position)

    def _crossover(self):
        offspring = []

        for _ in range(self.__size - len(self.__agents)):
            parent1 = random.choice(self.__agents)
            parent2 = random.choice(self.__agents)
            parent1_genes = parent1.get_dna().get_genes()
            parent2_genes = parent2.get_dna().get_genes()

            split = random.randint(0, self.__dna_length)

            child_genes = parent1_genes[0:split] + parent2_genes[split:self.__dna_length]

            agent = Agent(self.__dna_length, self.__initial_position,
                          genes=child_genes)
            offspring.append(agent)

        self.__agents.extend(offspring)

    def _mutation(self, mutation_rate):
        for agent in self.__agents:
            for idx, gene in enumerate(agent.get_dna().get_genes()):
                if random.uniform(0.0, 1.0) <= mutation_rate:
                    agent.get_dna().mutate(idx)


class GeneticAlgorithm:

    def __init__(self, dna_length, population_size, mutation_rate,
                 initial_position, target_position, selection_rate,
                 sleep_time, n_generations=sys.maxint):

        self.__population = Population(dna_length, population_size,
                                       initial_position, target_position)
        self.__n_generations = n_generations
        self.__board = Board(BOARD_SIZE)
        self.__sleep_time = sleep_time

    def run(self):
        for x in range(self.__n_generations):
            self.__population.walk(self.__board, x)
            self.__population.calculate_fitness()
            self.__population.select(selection_rate)
            self.__population.reproduce(mutation_rate)
            self.__population.reposition()

class Board:

    def __init__(self, size):
        self.__size = size
        self.__matrix = None

    def insert_objects(self, agents, target_position):
        self.__matrix[target_position[0]][target_position[1]] = 'X'

        for agent in agents:
            self.__matrix[agent.get_position()[0]][agent.get_position()[1]] = 'O'


    def show(self, generation):
        for row in self.__matrix:
            print "\n"
            for col in row:
                print col,
        print "Generation %d" % (generation)

    def clear(self):
        self.__matrix = [["|" for _ in range(self.__size[0])] for _ in range(self.__size[1])]

    def run(self, agents, target_position, generation):
        time.sleep(0.1)
        os.system('cls' if os.name == 'nt' else 'clear')
        self.clear()
        self.insert_objects(agents, target_position)
        self.show(generation)


if __name__ == "__main__":

    dna_length = 30
    n_generations = 50
    population_size = 20
    mutation_rate = 0.05
    selection_rate = 0.2
    initial_position = [10, 10]
    target_position = [19, 0]
    sleep_time = 1

    ga = GeneticAlgorithm(dna_length, population_size, mutation_rate,
                          initial_position, target_position, selection_rate,
                          sleep_time, n_generations)
    ga.run()
