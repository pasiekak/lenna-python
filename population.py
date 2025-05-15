import numpy as np
from copy import deepcopy
from chromosome import Chromosome
from config import POPULATION_SIZE, MUTATION_RATE, REQUIRE_BETTER_CHILD
from triangle import Triangle

class Population:
    def __init__(self, target_image):
        self.size = POPULATION_SIZE
        self.target_image = np.asarray(target_image, dtype=np.uint8)
        self.chromosomes = [Chromosome() for _ in range(self.size)]
        self.best_chromosome = None

    def evaluate(self):
        for chromosome in self.chromosomes:
            chromosome.fitness(target_img=self.target_image)
        self.best_chromosome = max(self.chromosomes, key=lambda c: c.fitness_score)

    def tournament_selection(self, k=3):
        tournament = np.random.choice(self.chromosomes, k, replace=False)
        return max(tournament, key=lambda c: c.fitness_score)

    def next_generation(self):
        new_chromosomes = []
        for _ in range(self.size):
            parent1 = self.tournament_selection()
            parent2 = self.tournament_selection()
            blendMethod = self.blendCrossover if np.random.rand() < 0.6 else self.pointCrossover
            child = blendMethod(parent1, parent2)
            if np.random.rand() < MUTATION_RATE:
                random_triangle = np.random.choice(child.triangles)
                random_triangle.mutate()
            new_chromosomes.append(child)
        self.chromosomes = new_chromosomes
        self.evaluate()

    def getBest(self):
        return self.best_chromosome, self.best_chromosome.fitness_score

    def blendCrossover(self, parent1, parent2):
        fit1 = parent1.fitness_score
        fit2 = parent2.fitness_score
        total = fit1 + fit2
        x = fit2 / total
        blended_background = (parent1.getImage().astype(np.float32) * (1-x) + parent2.getImage().astype(np.float32) * x).astype(np.uint8)
        better = parent1 if fit1 >= fit2 else parent2
        max_attempts = 10 if REQUIRE_BETTER_CHILD else 1
        for _ in range(max_attempts):
            child = Chromosome()
            child.background = blended_background.copy()
            child.triangles = deepcopy(better.triangles)
            idx = np.random.randint(0, len(child.triangles))
            child.triangles[idx] = Triangle.random()
            child._cached_img = None
            child.fitness_score = child.fitness(target_img=self.target_image)
            if not REQUIRE_BETTER_CHILD or child.fitness_score > better.fitness_score:
                return child
        return deepcopy(better)

    def pointCrossover(self, parent1, parent2):
        fit1 = parent1.fitness_score
        fit2 = parent2.fitness_score
        better = parent1 if fit1 >= fit2 else parent2
        max_attempts = 10 if REQUIRE_BETTER_CHILD else 1
        for _ in range(max_attempts):
            direction = np.random.choice(['horizontal', 'vertical'])
            width, height = parent1.getImage().shape[1], parent1.getImage().shape[0]
            img1 = parent1.getImage()
            img2 = parent2.getImage()
            if direction == 'horizontal':
                cut = np.random.randint(0, height)
                new_img = np.vstack((img1[:cut, :, :], img2[cut:, :, :]))
            else:
                cut = np.random.randint(0, width)
                new_img = np.hstack((img1[:, :cut, :], img2[:, cut:, :]))
            child = Chromosome()
            child.background = new_img.copy()
            child.triangles = deepcopy(better.triangles)
            child._cached_img = None
            child.fitness_score = child.fitness(target_img=self.target_image)
            if not REQUIRE_BETTER_CHILD or child.fitness_score > better.fitness_score:
                return child
        return deepcopy(better)

