from Utils import Rectangle, Color, Button, Text, Point, Window
import random
from Models import NN
import copy
import numpy as np

class Bird:
    x = Window.center[0]/5
    gravity = 0.001
    strength = gravity*1000/3
    sprite = "Images/bird.png"
    architecture = [2,4,1]

    def __init__(self, AI = True):
        self.alive = True
        self.rectangle = Rectangle(Bird.x, Window.center[1], 40, 30)
        self.velocity = 0
        self.brain = NN(Bird.architecture)
        self.score = 0
        self.fit = 0
        self.AI = AI

    def fly(self):
        self.velocity = -Bird.strength

    def die(self, score):
        self.score = score
        self.alive = False

    def update(self, x, y, click: bool):
        if not self.AI:
            if click:
                self.fly()
        else:
            if self.brain.feed([(self.rectangle.x - x)/Window.width, (self.rectangle.y - y)/Window.height]) > 0:
                self.fly()
        y = self.rectangle.y + self.velocity
        self.velocity += Bird.gravity
        self.rectangle.y = y

    def clone(self):
        new = Bird()
        new.brain = copy.copy(self.brain)
        return new

    def mutate(self, rate):
        for i in self.brain.weights:
            for j in i:
                for k in j:
                    if rate < random.random():
                        k += random.random() - 1
        for i in self.brain.baiases:
            for j in i:
                if rate < random.random():
                    k += random.random() - 1
        return self

    import random


class Birds:
    def __init__(self, AI, nbirds=50, mutation_rate=0.4, elite_rate=0.4, fresh_rate=0.2):
        self.nbirds = nbirds
        self.mutation_rate = mutation_rate
        self.fresh_rate = fresh_rate
        self.elite_rate = elite_rate
        self.birds = [Bird(False)]
        self.deads = []
        self.AI = AI
        if self.AI:
            while len(self.birds) < self.nbirds:
                self.birds.append(Bird())

    def kill(self, bird, score):
        self.birds.remove(bird)
        bird.die(score)
        self.deads.append(bird)

    def killall(self, score):
        for bird in self.birds:
            self.kill(bird, score)


    def regenerate(self):
        new_population = []
        new_population.append(Bird(False))
        if not self.AI:
            self.birds = new_population
            return
        scores = np.array([bird.score for bird in self.deads])
        total_score = scores.sum()

        if total_score == 0:
            weights = np.ones(len(self.deads)) / len(self.deads)
        else:
            weights = scores / total_score

        sorted_indices = np.argsort(scores)[::-1]
        sorted_deads = [self.deads[i] for i in sorted_indices]
        sorted_weights = weights[sorted_indices]


        elite_count = max(1, int(self.elite_rate * self.nbirds))
        new_population.extend(bird.clone() for bird in sorted_deads[:elite_count])

        for _ in range(int(self.fresh_rate*self.nbirds)):
            new_population.append(Bird())

        while len(new_population) < self.nbirds:
            parent = np.random.choice(sorted_deads, p=sorted_weights)
            offspring = parent.clone()

            if random.random() < self.mutation_rate:
                offspring.mutate(self.mutation_rate)

            new_population.append(offspring)

        self.birds = new_population

    def __getitem__(self, index):
        return self.birds[index]

    def __setitem__(self, index, value):
        self.birds[index] = value

    def __len__(self):
        return len(self.birds)

    def remove(self, bird):
        self.birds.remove(bird)

    def append(self, bird):
        self.birds.append(bird)

