import numpy as np
import random

class Boord:
	y = 0
	velocity = 0
	distanceBot = 0
	distanceTop = 0
	distanceX = 0
	fitness = 0
	alive = True
	weights = [] 
	jump = False
	bestReported = False
	
	#TODO Birds have brains and brains need to mutate. Also brains need to decide
	#Mutation of brain: adapt weights a little bit up and down for each node of the net. potentially also the bias?!
	def __init__(self, height, male = None, female = None):
		self.bestReported = False
		self.y = height/2
		self.velocity = 0
		self.distanceBot = 0
		self.distanceTop = 0
		self.distanceX = 0
		self.fitness = 0
		self.alive = True
		if (male == None): #New Bird, no parents
			self.weights = np.random.normal(scale=1 / 4**.5, size=4)
		elif (female == None): #Only one Parent (self mutate)
			self.weights = male.weights
			self.mutate()
		else: # Two parents - Breed.
			self.weights = np.random.normal(scale=1 / 4**.5, size=4)	
			self.breed(male, female)
		
	def thinkIfJump(self):
		BIAS = 0.5
		prediction = self.sigmoid(np.dot([self.y, self.distanceBot, self.distanceTop, self.distanceX], self.weights))
		if (prediction+BIAS > 0.5):
			return True
		else:
			return False
		
	# Activation (sigmoid) function
	def sigmoid(self, x):
		return 1 / (1 + np.exp(-x))

	def setWeights(self, weights):
		self.weights = weights
	
	def breed(self, male, female):
		for i in range(len(self.weights)):
			self.weights[i] = (male.weights[i] + female.weights[i]) / 2
		self.mutate()
		
	def mutate(self):
		"""'mutate' (randomly apply the learning rate) the 'genes' (weights) of the birds small brain"""
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
			

		