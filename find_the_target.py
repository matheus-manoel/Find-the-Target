import random


class Agent:

    def __init__(self, position=[0, 0]):
        self.fitness = -1
        self.position = position
        self.DNA = DNA()


class DNA:

    def __init__(self):
        self.genes = []
