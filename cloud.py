import random

class cloud:
	"""The cloud class is just for the looks
	It passes in the background - every five ticks, one pixel"""
	
	def __init__(self, WIDTH, HEIGHT):
		"""Constructor for a cloud, which will be moving from the right to the left
		
		INPUT:  WIDTH - The value where the cloud will be initialized. Will be randomized
				HEIGHT - The value where the cloud will be initialized. Will be randomized
		
		OUTPUT: None"""
				
		self.x = WIDTH + 140 + random.randint(0,140)
		self.y = random.randint(0, int(HEIGHT/2))
		self.TICKLIMIT = 5
		self.moveTick = 0
		
	def moveLeft(self):
		"""Move the cloud every five frames from right to left
		
		INPUT: None
		OUTPUT: None"""
		if (self.moveTick > self.TICKLIMIT):
			self.x -= 1
		
		self.moveTick += 1