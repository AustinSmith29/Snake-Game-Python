import pygame, sys
import random

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def copy(self):
		"""Return a point that copies this points values"""
		return Point(self.x, self.y)

	def __repr__(self):
		return "Point({0}, {1})".format(self.x, self.y)

class Node:
	"""One segment of the snake"""
	def __init__(self, point):
		self.head = None
		self.tail = None
		self.coord = point
		self.prevCoord = point

	def __str__(self):
		return "Node <{0}, {1}>".format(self.coord.x, self.coord.y)
	
class Snake:
	"""The Snake is a linked list of Nodes"""
	def __init__(self, startingPoint):
		self.snake = [Node(startingPoint)]
		self.head = self.snake[0]
		self.direction = 0 #0: UP; 1: RIGHT; 2: DOWN; 3: LEFT

	def increaseSize(self):
		#get last location of last segment of snake
		lastNode = self.snake[len(self.snake) - 1]
		loc = lastNode.prevCoord

		#create new node and set its head
		new = Node(loc)
		new.head = lastNode
		new.tail = None

		#set the tail of the previously last node to new node
		lastNode.tail = new
				
		self.snake.append(new)

	def updateSnake(self, head):
		node = head
		while node.tail:
			node = node.tail
			node.prevCoord = node.coord
			node.coord = node.head.prevCoord

	#The reason I check if the user is not trying to go in 
	#the opposite direction is to avoid the snake instantly
	#eating itself
	def moveUp(self):
		if self.direction != 2:
			self.direction = 0

	def moveRight(self):
		if self.direction != 3:
			self.direction = 1

	def moveDown(self):
		if self.direction != 0:
			self.direction = 2

	def moveLeft(self):
		if self.direction != 1:
			self.direction = 3
	
	def update(self):
		self.head.prevCoord = self.head.coord.copy()

		#update position every frame based on direction
		if self.direction == 0:
			self.head.coord.y -= 1

		elif self.direction == 1:
			self.head.coord.x += 1

		elif self.direction == 2:
			self.head.coord.y += 1

		else:
			self.head.coord.x -= 1

		self.updateSnake(self.head)
		
	def __repr__(self):
		node = self.snake[0]
		while node.tail:
			print node,
			print "-->",
			node = node.tail
		print self.snake[len(self.snake)-1]
		return ""

class Food:
	def __init__(self, point):
		self.point = point
		self.eaten = False

class Environment:
	def __init__(self):
		self.width = 40
		self.height = 30
		self.grid = [[0 for x in range(self.width)] 
					for y in range(self.height)]
		self.objects = []
		self.foodPoint = None
		self.score = 0
		self.snake = Snake(Point(20,15))
		self.snake.increaseSize()
		self.snake.increaseSize()
		self.placeFood()

	def update(self):
		self.clear()
		for node in self.snake.snake:
			self.grid[node.coord.y][node.coord.x] = 1

		self.grid[self.foodPoint.y][self.foodPoint.x] = 2
		self.snake.update()
		
		
		#"Wrap" the screen for the snake		
		if self.snake.head.coord.y < 0:
			self.snake.head.coord.y = self.height - 1
		if self.snake.head.coord.y >= self.height:
			self.snake.head.coord.y = 0
		if self.snake.head.coord.x < 0:
			self.snake.head.coord.x = self.width - 1
		if self.snake.head.coord.x >= self.width:
			self.snake.head.coord.x = 0

		#check collision for snake eating self
		if self.grid[self.snake.head.coord.y][self.snake.head.coord.x] == 1:
					print "YOU LOSE. FINAL SCORE: %d" % self.score
					pygame.quit()
					sys.exit() #temp for now

		#check collision for food
		if self.grid[self.snake.head.coord.y][self.snake.head.coord.x] == 2:
			self.grid[self.snake.head.coord.y][self.snake.head.coord.x] == 0
			self.snake.increaseSize()
			self.score += 10
			self.placeFood()

	def clear(self):
		self.grid[:][:] = []
		self.grid = [[0 for x in range(self.width)] 
					for y in range(self.height)]

	def placeFood(self):
		validSpot = False
		while not validSpot:
			x = random.randint(0, self.width-1)
			y = random.randint(0, self.height-1)
			if self.grid[y][x] == 0:
				self.foodPoint = Point(x,y)
				validSpot = True

def renderEnvironment(env, surface):
	for ey, y in enumerate(env.grid):
		for ex, x in enumerate(y):
			if x == 1:
				pygame.draw.rect(surface, (255,0,0),
						(ex * 16, ey * 16, 16, 16))
			if x == 2:	
				pygame.draw.rect(surface, (0,255,0),
						(ex * 16, ey * 16, 16, 16))

if __name__ == "__main__":
	pygame.init()
	screen = pygame.display.set_mode((640, 480))
	env = Environment()
	clock = pygame.time.Clock()
	paused = False
	while True:
		clock.tick(20)
		pygame.display.set_caption("Snake!       Score: %d" % env.score)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					env.snake.moveUp()
				if event.key == pygame.K_RIGHT:
					env.snake.moveRight()
				if event.key == pygame.K_DOWN:
					env.snake.moveDown()
				if event.key == pygame.K_LEFT:
					env.snake.moveLeft()
				if event.key == pygame.K_p:
					if paused:
						paused = False
					else:
						paused = True

		if not paused:
			env.update()
		screen.fill((0,0,0))
		renderEnvironment(env, screen)
		pygame.display.flip()
	#	pygame.time.wait(50)
