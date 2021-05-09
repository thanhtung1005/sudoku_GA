import random
import numpy
import pygame
DIM = 9
MUTA_RATE = 0.1
""" Solve Sudoku"""
# def input_sudoku(filename):
# 	with open(filename, "r") as f:
# 		sudoku_board = numpy.loadtxt(f).reshape((9, 9)).astype(int)
# 	return sudoku_board

def init_population(sudoku_board, num_population):
	return [init_individual(sudoku_board) for _ in range(num_population)]

def init_individual(sudoku_board):
	individual = []
	for i in range(DIM):
		alleles = list(range(1,DIM + 1))
		individual.append(list(sudoku_board[i]))
		for j in range(DIM):
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
	new_individual=numpy.zeros((DIM,DIM))
	for i in range(DIM):
		new_individual[i] = random.choice((individual_1[i], individual_2[i]))
	return new_individual

def mutate_population(population, sudoku_board):
	return [mutate_individual(individual, sudoku_board) for individual in population]

def mutate_individual(individual, sudoku_board):
	for i in range(DIM):
		if (random.random() < MUTA_RATE):
			while True:
				rand1 = random.randint(0, DIM - 1)
				rand2 = random.randint(0, DIM - 1)
				if (sudoku_board[i,rand1] == 0 and sudoku_board[i,rand2] == 0):
					individual[i,rand1], individual[i,rand2] = individual[i,rand2], individual[i,rand1]
					break
	return individual


def calc_fitness(population, generation=0):

	fit=[]
	for sudoku_board in population:
		fitness = 0
		for i in range(DIM):
			different_alleles = set(sudoku_board[:, i])
			fitness += len(different_alleles)
		dim_block = 3
		for i in range(0, DIM, dim_block):
			for j in range(0, DIM, dim_block):
				block = sudoku_board[i:i + dim_block, j:j + dim_block]
				different_alleles = set(block.flatten())
				fitness += len(different_alleles)
		fit.append(fitness)
	return fit

# sudoku_board = input_sudoku("board1")
# print("Input Sudoku Board:")
# print(sudoku_board.astype(int))
num_population=200
generation = 0
# population = init_population(sudoku_board, num_population)
# fitness_population = calc_fitness(population)
# while True:
# 	generation += 1
# 	poplnparents = select_population(population, fitness_population, num_population)
# 	poplnchild = crossover(poplnparents, num_population)
# 	population = mutate_population(poplnchild, sudoku_board)
# 	fitness_population = calc_fitness(population, generation)
# 	# print("Gen:", generation, "& Max fit %.1f" % max(fitness_population))
# 	num_re_init = 0
# 	if generation > 1000:
# 		generation = 0
# 		num_re_init += 1
# 		# print("re-initialize population")
# 		population = init_population(sudoku_board, num_population)
# 		fitness_population = calc_fitness(population)
# 	best_fitness = max(fitness_population)
# 	best_individual = population[fitness_population.index(best_fitness)].astype(int)
# 	if best_fitness == 162:
# 		# print(best_individual)
# 		break
# 	if num_re_init >= 10:
# 		# print("can't solve'")
# 		break

pygame.init()
pygame.display.set_caption("Sudoku")
screen = pygame.display.set_mode((405, 405))
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)
height=40
width=40

class InputBox:
	def __init__(self, x, y, w, h, text = "0"):
		self.rect = pygame.Rect(x, y, w, h)
		self.color = COLOR_INACTIVE
		self.text = text
		self.txt_surface = FONT.render(text, True, self.color)
		self.txt_rect = self.txt_surface.get_rect()
		self.txt_rect.center = self.rect.center
		self.active = False
	def update_text(self, text):
		self.text = text
		self.txt_surface = FONT.render(text, True, self.color)
		self.txt_rect = self.txt_surface.get_rect()
		self.txt_rect.center = self.rect.center
	def draw(self, screen):
		screen.blit(self.txt_surface, self.txt_rect)
		pygame.draw.rect(screen, self.color, self.rect, 2)

input_board = []
for i in range(DIM):
	col = []
	for j in range(DIM):
		col.append(InputBox(i*(width+5),j*(height+5),height,width))
	input_board.append(col)
solve = False
run = True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if not solve:
				for i in range(DIM):
					for j in range(DIM):
						if input_board[i][j].rect.collidepoint(event.pos):
							input_board[i][j].active = not input_board[i][j].active
						else:
							input_board[i][j].active = False
						input_board[i][j].color = COLOR_ACTIVE if input_board[i][j].active else COLOR_INACTIVE
		if event.type == pygame.KEYDOWN:
			for i in range(DIM):
				for j in range(DIM):
					if event.unicode in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
						if input_board[i][j].active:
							input_board[i][j].update_text(event.unicode)
			if event.key == pygame.K_RETURN:
				solve = not solve
				sudoku_board = numpy.zeros((9,9))
				for i in range(DIM):
					for j in range(DIM):
						sudoku_board[i, j] = int(input_board[i][j].text)
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
						population = init_population(sudoku_board, num_population)
						fitness_population = calc_fitness(population)
					best_fitness = max(fitness_population)
					best_individual = population[fitness_population.index(best_fitness)].astype(int)
					for i in range(DIM):
						for j in range(DIM):
							input_board[i][j].update_text(str(best_individual[i, j]))
					if best_fitness == 162:
						print(best_individual)
						break
					screen.fill((0, 0, 0))
					for i in range(DIM):
						for j in range(DIM):
							input_board[i][j].draw(screen)
					pygame.display.flip()
	screen.fill((0, 0, 0))
	for i in range(DIM):
		for j in range(DIM):
			input_board[i][j].draw(screen)
	pygame.display.flip()
pygame.quit()