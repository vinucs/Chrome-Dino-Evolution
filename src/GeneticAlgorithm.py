import random

class GeneticAlgorithm:

    def __init__(self, num_pop, f, cr, max_value, min_value, num_weights):
        self.num_population = num_pop
        self.mutation_factor = f
        self.crossover_rate = cr
        self.max_value = max_value
        self.min_value = min_value
        self.num_weights = num_weights
        self.population = []
        self.population_fitness = []

    def createPopulation(self):
        random.seed()
        self.population.clear()
        for i in range(self.num_population):
            self.population.append([])
            for j in range(self.num_weights + 1):
                diference = self.max_value - self.min_value
                value_rand = random.uniform(0, 1)
                self.population[i].append(self.min_value + value_rand*diference)

    def printPopulation(self):
        for x in self.population:
            print(x)

    def getPopulation(self):
        return self.population

    def getChildrens(self):
        return self.childrens

    def setFitness(self, pop_fitness):
        self.population_fitness = pop_fitness
    
    def setChildrensFitness(self, chil_fitness):
        self.childrens_fitness = chil_fitness

    def getBestIndividual(self):
        return self.population_fitness.index(max(self.population_fitness))

    def improveIndividuals(self):
        self.childrens = self.binomialCrossover(self.mutationRandToBest())

    def reviseValue(self, value):
        if value < self.min_value:
            value = self.min_value
        elif value > self.max_value:
            value = self.max_value
        return value

    def mutationBest(self):
        random.seed()
        mutants = []
        self.best_individual = self.population[self.getBestIndividual()]
        for i in range(self.num_population):
            mutants.append([])
            rand1 = random.randint(0, self.num_population - 1)
            rand2 = random.randint(0, self.num_population - 1)
            for j in range(self.num_weights + 1):
                value = self.best_individual[j] + (self.mutation_factor *(self.population[rand1][j] - self.population[rand2][j]))
                mutants[i].append(self.reviseValue(value))         
        return mutants

    def mutationRand(self):
        random.seed()
        mutants = []
        for i in range(self.num_population):
            mutants.append([])
            rand1 = random.randint(0, self.num_population - 1)
            rand2 = random.randint(0, self.num_population - 1)
            rand3 = random.randint(0, self.num_population - 1)
            for j in range(self.num_weights + 1):
                value = self.population[rand1][j] + (self.mutation_factor *(self.population[rand2][j] - self.population[rand3][j]))
                mutants[i].append(self.reviseValue(value))         
        return mutants

    def mutationRandToBest(self):
        random.seed()
        mutants = []
        self.best_individual = self.population[self.getBestIndividual()]
        for i in range(self.num_population):
            mutants.append([])
            rand1 = random.randint(0, self.num_population - 1)
            rand2 = random.randint(0, self.num_population - 1)
            for j in range(self.num_weights + 1):
                value = self.population[i][j] + (self.mutation_factor *(self.best_individual[j] - self.population[i][j])) + (self.mutation_factor *(self.population[rand1][j] - self.population[rand2][j]))
                mutants[i].append(self.reviseValue(value))         
        return mutants    

    def binomialCrossover(self, mutants):
        random.seed()
        new_childrens = []
        for i in range(self.num_population):
            j_rand = random.randint(0, self.num_weights + 1)
            new_childrens.append([])
            for j in range(self.num_weights + 1):
                rand_value = random.uniform(0,1)
                if rand_value <= self.crossover_rate or j_rand == j:
                    new_childrens[i].append(mutants[i][j])
                else:
                    new_childrens[i].append(self.population[i][j])
        return new_childrens

    def selection(self):
        new_population = []
        for i in range(self.num_population):
            if self.childrens_fitness[i] >= self.population_fitness[i]:
                new_population.append(self.childrens[i])
            else:
                new_population.append(self.population[i])
        self.population = new_population