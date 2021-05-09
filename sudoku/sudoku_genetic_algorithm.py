import sys
import random
import numpy

def input_sudoku(filename):
	with open(filename, "r") as f:
		sudoku_board = numpy.loadtxt(f).reshape((9, 9)).astype(int)
	return sudoku_board

def init_population(sudoku_board, num_population):
	return [init_individual(sudoku_board) for _ in range(num_population)]

def init_individual(sudoku_board):
	individual = []
	for i in range(9):
		alleles = [1,2,3,4,5,6,7,8,9]
		individual.append(list(sudoku_board[i]))
		for j in range(9):
			if (sudoku_board[i, j] == 0):
				has_allele = False
				while(has_allele == False):
					picked_allele = random.choice(alleles)
					alleles.remove(picked_allele)
					if(picked_allele not in individual[i]):
						individual[i][j] = picked_allele
						has_allele = True
	return numpy.array(individual)


def select_population(population, fitness_population, num_population):
	sortedPopulation = sorted(zip(population,fitness_population),
							  key = lambda x: x[1], reverse=True)
	return [individual for individual, fitness in
			sortedPopulation[:int(num_population * 0.8)]]

def crossover(population, num_population):
	new_individual=[]
	for i in range(num_population):
		new_individual.append(crossover_individual(random.choice(population),
									  random.choice(population)))
	return new_individual

def crossover_individual(individual_1, individual_2):
	new_individual=numpy.zeros((9,9))
	for i in range(9):
		new_individual[i] = random.choice((individual_1[i], individual_2[i]))
	return new_individual

def mutate_population(population, sudoku_board):
	return [mutate_individual(individual, sudoku_board) for individual in population]

def mutate_individual(individual, sudoku_board):
	for i in range(9):
		if (random.random() < 0.1):
			while True:
				rand1 = random.randint(0,8)
				rand2 = random.randint(0,8)
				if (sudoku_board[i,rand1] == 0 and sudoku_board[i,rand2] == 0):
					individual[i,rand1], individual[i,rand2] = individual[i,rand2], individual[i,rand1]
					break
	return individual


def calc_fitness(population, generation=0):

	fit=[]
	for sudoku_board in population:
		fitness = 0
		for i in range(9):
			different_alleles = set(sudoku_board[:, i])
			fitness += len(different_alleles)
		dim_block = 3
		for i in range(0, 9, dim_block):
			for j in range(0, 9, dim_block):
				block = sudoku_board[i:i + dim_block, j:j + dim_block]
				different_alleles = set(block.flatten())
				fitness += len(different_alleles)
		if (fitness == 162): # for final solution
			print("")
			print("Max current fitness:",fitness)
			print("")
			print("Solution Is: ")
			print(sudoku_board.astype(int))
			print("Gen:", generation )
			sys.exit()
		fit.append(fitness)
	return fit



sudoku_board = input_sudoku("board1")
print("Input Sudoku Board:")
print(sudoku_board.astype(int))
num_population=200
generation = 0
population = init_population(sudoku_board, num_population)
fitness_population = calc_fitness(population)
while True:
	generation += 1
	poplnparents = select_population(population, fitness_population, num_population)
	poplnchild = crossover(poplnparents, num_population)
	population = mutate_population(poplnchild, sudoku_board)
	fitness_population = calc_fitness(population, generation)
	print("Gen:", generation, "& Max fit %.1f" % max(fitness_population))
	if generation > 1000:
		generation = 0
		print("re-initialize population")
		population = init_population(sudoku_board, num_population)
		fitness_population = calc_fitness(population)