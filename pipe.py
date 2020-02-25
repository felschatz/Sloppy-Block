import random

class pipe:
	"""The pipe class. A pipe pair is an obstacle, which will be displayed on the screen"""
	uppery = 0
	lowery = 0
	x = 0
	
	def __init__(self, WIDTH, HEIGHT, distanceToOldPipe):
		"""The constructor of a pipe pair. A pipe pair is the obstacle the bird has to fly through.
		
		INPUT:  WIDTH: The screen width. The new pipe will be initialized to the right of it.
				HEIGHT: The screen height. Defines where the pipe will be initialized.
				distanceToOldPipe: Since pipes are initialized with a random distance, it must keep a minimum distance to an existing pipe on screen or else the pipes can not be flown through
		OUTPUT: None"""
		
		top = random.randint(0,HEIGHT-100)
		self.uppery = random.randint(0,HEIGHT-140) # We wanna show something on the lower end.
		self.lowery = self.uppery + 120
		self.x = distanceToOldPipe/4 + WIDTH + random.randint(0,15) #randomize distance of pipes so the bird can learn better
		
	def moveLeft(self):
		"""When a frame is processed, the pipe moves to the left
		INPUT:  None
		OUTPUT: None"""
		
		self.x -= 4
		