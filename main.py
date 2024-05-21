import random

# Inisialisasi parameter algoritma
numChromosomes = 10
numIterations = 100
numServices = 5
numEs = 2

# Inisialisasi kromosom secara acak
def initializePopulation(numChromosomes, numServices, numEs):
    population = []
    for _ in range(numChromosomes):
        chromosome = []
        for _ in range(numEs):
            gene = ''.join(random.choice('01') for _ in range(numServices))
            chromosome.append(gene)
        population.append(chromosome)
    return population

# Fungsi evaluasi untuk menghitung nilai fitness
def calculateFitness(chromosome):
    # Contoh perhitungan fitness (harus disesuaikan dengan fungsi objektif spesifik)
    finishedTasks = sum(int(gene, 2) for gene in chromosome)
    resourceUtilization = sum(gene.count('1') for gene in chromosome)
    return finishedTasks + resourceUtilization

# Operator crossover
def crossover(parent1, parent2):
    crossoverPoint = random.randint(0, numServices - 1)
    child1 = parent1[:crossoverPoint] + parent2[crossoverPoint:]
    child2 = parent2[:crossoverPoint] + parent1[crossoverPoint:]
    return child1, child2

# Operator mutasi
def mutate(chromosome):
    # mutationPoint = random.randint(0, numServices - 1)
    # mutatedGene = list(chromosome)
    # mutatedGene[mutationPoint] = '1' if chromosome[mutationPoint] == '0' else '0'
    # return ''.join(mutatedGene)
    print(chromosome)
    return chromosome

# Operator seleksi turnamen
def tournamentSelection(population, fitnesses, tournamentSize=3):
    selected = random.sample(range(len(population)), tournamentSize)
    bestIndividual = max(selected, key=lambda i: fitnesses[i])
    return population[bestIndividual]

# Algoritma Genetika dengan Pencarian Heuristik Dua Tahap
def geneticAlgorithm(numIterations, numChromosomes, numServices, numEs):
    population = initializePopulation(numChromosomes, numServices, numEs)
    bestChromosome = None
    bestFitness = -1

    for _ in range(numIterations):
        fitnesses = [calculateFitness(chromosome) for chromosome in population]

        for i in range(numChromosomes):
            if fitnesses[i] > bestFitness:
                bestFitness = fitnesses[i]
                bestChromosome = population[i]

        newPopulation = []
        for _ in range(numChromosomes // 2):
            parent1 = tournamentSelection(population, fitnesses)
            parent2 = tournamentSelection(population, fitnesses)
            child1, child2 = crossover(parent1, parent2)
            newPopulation.append(mutate(child1))
            newPopulation.append(mutate(child2))

        population = newPopulation

    return bestChromosome, bestFitness

# Menjalankan algoritma genetika
bestChromosome, bestFitness = geneticAlgorithm(numIterations, numChromosomes, numServices, numEs)
print(f'Best Chromosome: {bestChromosome}, Best Fitness: {bestFitness}')
