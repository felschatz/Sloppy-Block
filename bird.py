import numpy as np
import random

class Boord:
	"""The Bird class. Contains information about the bird and also it's brain, breeding behaviour and decision making"""
	y = 0
	velocity = 0
	distanceBot = 0
	distanceTop = 0
	distanceX = 0
	distanceCeil = 0
	distanceGround = 0
	fitness = 0
	alive = True
	weights = [] 
	jump = False
	bestReported = False
	
	def __init__(self, height, male = None, female = None):
		"""The constructor. Either a bird, which is initialized by breeding, a mutated bird, or a standalone bird.
		INPUT:  height: The screen height. The bird will be initialized in the middle of it
				male: Defaulted to None. If set: The brain (weights for NN) are taken over and mutated
				female: Defaulted to None. If set with male: Averages the brains (weights for NN) of male and female and mutate
				
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
			#complex network
			#self.weights = np.random.normal(scale=1 / 4**.5, size=6)
			#easy network
			self.weights = np.random.normal(scale=1 / 4**.5, size=5)
		elif (female == None): #Only one Parent (self mutate)
			self.weights = male.weights
			self.mutate()
		else: # Two parents - Breed.
			#complex network
			#self.weights = np.random.normal(scale=1 / 4**.5, size=6)	
			#easy network
			self.weights = np.random.normal(scale=1 / 4**.5, size=5)
			self.breed(male, female)
		
	def thinkIfJump(self):
		"""Forward pass through neural network, giving the decision if the bird should jump.
		The neural network consists out of the y position of the bird, y distance to the bottom pipe, the y distance to the top pipe, the x distance to the pipe pair and the own velocity
		
		INPUT:  None
		OUTPUT: boolean, which determines if the bird should jump (True) or not (False)"""
		BIAS = 0.5
		#complex network
		#prediction = self.sigmoid(np.dot([self.y, self.distanceBot, self.distanceTop, self.distanceX, self.distanceCeil, self.distanceGround], self.weights))
		#easy network
		prediction = self.sigmoid(np.dot([self.y, self.distanceBot, self.distanceTop, self.distanceX, self.velocity], self.weights))
		if (prediction+BIAS > 0.5):
			return True
		else:
			return False
		
	def sigmoid(self, x):
		"""The sigmoid activation function for the neural net
		
		INPUT: x - The value to calculate
		OUTPUT: The calculated result"""
		return 1 / (1 + np.exp(-x))

	def setWeights(self, weights):
		"""Overwrites the current weights of the birds brain (neural network).
		
		INPUT:  weights: The weights for the neural network
		OUTPUT:	None"""
		self.weights = weights
	
	def breed(self, male, female):
		"""Generate a new brain (neural network) from two parent birds by averaging their brains and mutating them afterwards
		
		INPUT:  male - The male bird object (of class bird)
				female - The female bird object (of class bird)
		OUTPUT:	None"""
		for i in range(len(self.weights)):
			self.weights[i] = (male.weights[i] + female.weights[i]) / 2
		self.mutate()
		
	def mutate(self):
		"""mutate (randomly apply the learning rate) the brain (neural network) of the birds brain by randomly changing the individual weights from 0 to +-0,125
		
		INPUT:  None
		OUTPUT:	None"""
		for i in range(len(self.weights)):
			multiplier = 0
			learning_rate = random.randint(0, 25) * 0.005
			randBool = bool(random.getrandbits(1)) #adapt upwards or downwards?
			randBool2 = bool(random.getrandbits(1)) #adapt upwards or downwards or not at all?
			if (randBool and randBool2):
				multiplier = 1
			elif (not randBool and randBool2):
				multiplier = -1
			
			self.weights[i] = self.weights[i] + learning_rate*multiplier
			

		