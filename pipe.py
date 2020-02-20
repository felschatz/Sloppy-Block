import random

class pipe:
	uppery = 0
	lowery = 0
	x = 0
	
	def __init__(self, WIDTH, HEIGHT):
		top = random.randint(0,HEIGHT-100)
		self.uppery = random.randint(0,HEIGHT-140) # We wanna show something on the lower end.
		self.lowery = self.uppery + 120
		self.x = WIDTH+random.randint(0,15) #randomize distance of pipes so the bird can learn better