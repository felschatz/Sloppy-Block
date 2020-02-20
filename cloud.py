import random

class cloud:
	TICKLIMIT = 5
	x = 0
	y = 0
	moveTick = 0
	
	def __init__(self, WIDTH, HEIGHT):
		self.x = WIDTH + 140 + random.randint(0,140)
		self.y = random.randint(0, int(HEIGHT/2))
		
	def moveLeft(self):
		if (self.moveTick > self.TICKLIMIT):
			self.x -= 1
		
		self.moveTick += 1