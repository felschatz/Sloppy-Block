import numpy as np
import random

class Boord:
	"""The Bird class. Contains information about the bird and also it's brain,
		breeding behaviour and decision making"""

	def __init__(self, height, male = None, female = None):
		"""The constructor. Either a bird, which is initialized by breeding,
			a mutated bird, or a standalone bird.
		INPUT:  height: The screen height.
						The bird will be initialized in the middle of it
				male: 	Defaulted to None.
						If set:
						  The brain (weights for NN) are taken over and mutated
				female: Defaulted to None
				 		If set with male:
						Averages the brains (weights for NN)
						  of male and female and mutate

		OUTPUT: None"""
		self.bestReported = False
		self.y = height/2
		self.velocity = 0
		self.distanceBot = 0
		self.distanceTop = 0
		self.distanceX = 0
		self.distanceGround = 0
		self.distanceCeil = 0
		self.fitness = 0
		self.alive = True
		if (male == None): #New Bird, no parents
			#easy network
			self.inputWeights = np.random.normal(0, scale=0.1, size=(5, 3))
			self.hiddenWeights = np.random.normal(0, scale=0.1, size=(3, 1))
		elif (female == None): #Only one Parent (self mutate)
			self.inputWeights = male.inputWeights
			self.hiddenWeights = male.hiddenWeights
			self.mutate()
		else: # Two parents - Breed.
			self.inputWeights = np.random.normal(0, scale=0.1, size=(5, 3))
			self.hiddenWeights = np.random.normal(0, scale=0.1, size=(3, 1))
			self.breed(male, female)

	def processBrain(self, pipeUpperY, pipeLowerY, pipeDistance):
		"""Updates what the bird sees.

		INPUT:  pipeUpperY - The y coordinate of the upper pipe
				pipeLowerY - The y coordinate of the lower pipe
				pipeDistance - The x distance to the pipe pair
		OUTPUT: None"""

		self.distanceTop = pipeUpperY - self.y
		self.distanceBot = pipeLowerY - self.y
		self.distanceX = pipeDistance
		self.fitness += 0.01

	def handleCollision(self, HEIGHT, BLOCKSIZE, pipe):
		"""Checks if the bird hits the upper bounds, lower bounds or a pipe

		INPUT:  HEIGHT - The global height of the screen
				BLOCKSIZE - The global bird size
				pipe - The pipe to handle the collision with
		OUTPUT: None"""
		#Check if player collided with upper or lower pipe
		if ( ((pipe.x >= 20) and (pipe.x <= 20+BLOCKSIZE)) or ((pipe.x+20 >= 20)
		 			and (pipe.x+20 <= 20+BLOCKSIZE)) ): #pipe in X reach
			if ( (self.alive) and ((self.y <= pipe.uppery)
			 		or (self.y+BLOCKSIZE >= pipe.lowery)) ): # also in y?
				#alive player hits a pipe
				self.alive = False
				self.fitness -= 1

		#upper/lower bounds handling (did the bird hit the ground/ceil)
		if (self.y + self.velocity > HEIGHT-BLOCKSIZE): #LowerBounds
			self.y = HEIGHT-BLOCKSIZE
			self.alive = False
			self.fitness -= 1
		elif (self.y + self.velocity < 1): #UpperBounds
			self.y = 0
			self.velocity = 0
			self.alive = False
			self.fitness -= 1


	def thinkIfJump(self):
		"""Forward pass through neural network,
		  	 giving the decision if the bird should jump.
		The neural network consists out of the y position of the bird,
			y distance to the bottom pipe, the y distance to the top pipe,
			the x distance to the pipe pair and the own velocity.

		INPUT:  None
		OUTPUT: boolean, which determines,
		 			if the bird should jump (True) or not (False)"""
		BIAS = -0.5
		X = [self.y, self.distanceBot, self.distanceTop, self.distanceX,
			self.velocity]

		hidden_layer_in = np.dot(X, self.inputWeights)
		hidden_layer_out = self.sigmoid(hidden_layer_in)
		output_layer_in = np.dot(hidden_layer_out, self.hiddenWeights)
		prediction = self.sigmoid(output_layer_in)

		if (prediction+BIAS > 0):
			return True
		else:
			return False

	def relu(self, x):
		"""The relu actication function for the neural network

		INPUT: x - The value to apply the ReLu function on
		OUTPUT: The applied ReLus function value"""

		return np.maximum(x, 0)

	def sigmoid(self, x):
		"""The sigmoid activation function for the neural net

		INPUT: x - The value to calculate
		OUTPUT: The calculated result"""

		return 1 / (1 + np.exp(-x))

	def setWeights(self, inputWeights, hiddenWeights):
		"""Overwrites the current weights of the birds brain (neural network).

		INPUT:  inputWeights: The weights for the neural network (input layer)
				hiddenWeights: The weights for the neural network (hidden layer)
		OUTPUT:	None"""
		self.inputWeights = inputWeights
		self.hiddenWeights = hiddenWeights

	def breed(self, male, female):
		"""Generate a new brain (neural network) from two parent birds
		 	by averaging their brains and mutating them afterwards

		INPUT:  male - The male bird object (of class bird)
				female - The female bird object (of class bird)
		OUTPUT:	None"""
		for i in range(len(self.inputWeights)):
			self.inputWeights[i] = (male.inputWeights[i] +
									female.inputWeights[i]) / 2

		for i in range(len(self.hiddenWeights)):
			self.hiddenWeights[i] = (male.hiddenWeights[i] +
									female.hiddenWeights[i]) / 2

		self.mutate()

	def mutate(self):
		"""mutate (randomly apply the learning rate) the birds brain
			(neural network) randomly changing the individual weights

		INPUT:  None
		OUTPUT:	None"""
		for i in range(len(self.inputWeights)):
			for j in range(len(self.inputWeights[i])):
				self.inputWeights[i][j] = self.getMutatedGene(self.inputWeights[i][j])
		for i in range(len(self.hiddenWeights)):
			for j in range(len(self.hiddenWeights[i])):
				self.hiddenWeights[i][j] = self.getMutatedGene(self.hiddenWeights[i][j])

	def getMutatedGene(self, weight):
		"""mutate the input by -0.125 to 0.125 or not at all

		INPUT: weight - The weight to mutate
		OUTPUT: mutatedWeight - The mutated weight"""

		multiplier = 0
		learning_rate = random.randint(0, 25) * 0.005
		randBool = bool(random.getrandbits(1)) #adapt upwards or downwards?
		randBool2 = bool(random.getrandbits(1)) #or not at all?
		if (randBool and randBool2):
			multiplier = 1
		elif (not randBool and randBool2):
			multiplier = -1

		mutatedWeight = weight + learning_rate*multiplier

		return mutatedWeight
