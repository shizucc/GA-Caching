import random
import numpy as np


populationSize = 10
generations = 50
crossoverRate = 1
mutationRate = 0.05


def fitness(chromosome, taskRequirements, edgeResources, cloudResources):
    edgeUsage = np.zeros(len(edgeResources))
    cloudUsage = 0
    satisfiedTasks = 0
    totalEdgeUsage = 0
    totalCloudUsage = 0

    for task, node in enumerate(chromosome):
        if node < len(edgeResources):  # Offload ke server edge
   
            if edgeUsage[node] + taskRequirements[task] <= edgeResources[node]:
                edgeUsage[node] += taskRequirements[task]
                totalEdgeUsage += taskRequirements[task]
                satisfiedTasks += 1
        else:  # Offload ke cloud
     
            if cloudUsage + taskRequirements[task] <= cloudResources:
                cloudUsage += taskRequirements[task]
                totalCloudUsage += taskRequirements[task]
                satisfiedTasks += 1


    edgeEfficiency = totalEdgeUsage / sum(edgeResources) if sum(edgeResources) > 0 else 0
    cloudEfficiency = totalCloudUsage / cloudResources if cloudResources > 0 else 0


    baseFitness = satisfiedTasks

   
    penalty = (cloudEfficiency * 0.5 + edgeEfficiency * 0.5) * (1 + cloudEfficiency + edgeEfficiency)

 
    preferenceBonus = totalEdgeUsage * 0.1


    totalFitness = baseFitness + preferenceBonus - penalty

    return totalFitness



def initializePopulation():
    population = []
    for _ in range(populationSize):
        # Penjelasan 
        # [x1,x2,x3,x4,x5] : 0,1,2 (edge), 3 (cloud)
        chromosome = np.random.randint(0, len(edgeResources) + 1, len(taskRequirements))
        population.append(chromosome)
    return population

def selectParents(population):
    #Penjelasan
    # Hitung total fitness dari seluruh populasi
    totalFitness = sum(fitness(c, taskRequirements, edgeResources, cloudResources) for c in population)

    # Hitung probabilitas kumulatif untuk setiap kromosom
    selectionProbabilities = []
    cumulativeFitness = 0
    for chrom in population:
        chromFitness = fitness(chrom, taskRequirements, edgeResources, cloudResources)
        cumulativeFitness += chromFitness
        selectionProbabilities.append(cumulativeFitness / totalFitness)
    
    # memilih satu kromosom berdasarkan RWS
    def selectOne():
        rand = random.random()
        for i, prob in enumerate(selectionProbabilities):
            if rand <= prob:
                return population[i]
    
    # Pilih dua orang tua
    parent1 = selectOne()
    parent2 = selectOne()
    return parent1, parent2


def crossover(parent1, parent2):
    if random.random() < crossoverRate:
        crossoverPoint = random.randint(1, len(parent1) - 1)
        child1 = np.concatenate((parent1[:crossoverPoint], parent2[crossoverPoint:]))
        child2 = np.concatenate((parent2[:crossoverPoint], parent1[crossoverPoint:]))
        
        return child1, child2
    return parent1, parent2


def mutate(chromosome):
    if random.random() < mutationRate:

        point1 = random.randint(0, len(chromosome) - 1)
        point2 = random.randint(0, len(chromosome) - 1)
        

        while point1 == point2:
            point2 = random.randint(0, len(chromosome) - 1)
        
        chromosome[point1], chromosome[point2] = chromosome[point2], chromosome[point1]
    
    return chromosome

def evolvePopulation(population):
    newPopulation = []
    for _ in range(populationSize // 2):
        parent1, parent2 = selectParents(population)
        offspring1, offspring2 = crossover(parent1, parent2)
        newPopulation.extend([mutate(offspring1), mutate(offspring2)])
    return newPopulation

# Inisialisasi sumber daya dan tugas
edgeResources = [100, 100, 100]  
cloudResources = 500  
taskRequirements = [30, 90, 60, 70, 50] 

# Inisialisasi populasi
population = initializePopulation()

# Generasi

for generation in range(generations):
    population = evolvePopulation(population)
    bestChromosome = max(population, key=lambda c: fitness(c, taskRequirements, edgeResources, cloudResources))
    print(f"Generasi {generation}: Fitness Terbaik = {fitness(bestChromosome, taskRequirements, edgeResources, cloudResources)}")

# Hasil terbaik

bestChromosome = max(population, key=lambda c: fitness(c, taskRequirements, edgeResources, cloudResources))
print("Kromosom Terbaik:", bestChromosome)
print("Fitness Terbaik:", fitness(bestChromosome, taskRequirements, edgeResources, cloudResources))
