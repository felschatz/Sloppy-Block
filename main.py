import sys
import copy
import pygame
import bird
import pipe
import cloud

"""TODO: 
Comment
In blog, talk about pygame
		Genetic algorithms https://towardsdatascience.com/artificial-neural-networks-optimization-using-genetic-algorithm-with-python-1fe8ed17733e
		https://blog.coast.ai/lets-evolve-a-neural-network-with-a-genetic-algorithm-code-included-8809bece164
		
		https://homepages.inf.ed.ac.uk/pkoehn/publications/gann94.pdf
		
		Dino NN
		https://heartbeat.fritz.ai/automating-chrome-dinosaur-game-part-1-290578f13907
		https://github.com/aayusharora/GeneticAlgorithms/blob/master/part1/src/nn.js
		
		floppy: https://github.com/Code-Bullet/Flappy-Bird-AI/blob/master/flappyBird/Population.js 
		
		Noteworthy that it does not jump to time the pipe (so it will pass the pipe in the middle). this might eb solved with a deeper neural network
"""

#Initialize constants
WIDTH = 640 #screensize
HEIGHT = 480 #screensize
BLOCKSIZE = 20 #Blocks Fatness for bounding box
BIRDS = 90 #No of Blocks to spawn
Gen788BestOfBest = [ 1.39379687, -0.77627931, -0.59737657, -0.04154869] #Pretty good bird - not the best, but pretty good
# Good genes after changes [ 1.20232449 -0.69404621 -0.49657121  0.01391649] (Generation 12 - beaten at prev score of 33 - currently at score 187)
FPSSES = 60 #Increase by pressing +/-

ReplayBest = False #Set to true, if you want to use trained network
AI = True # Set to false, if you want to play yourself
birdView = True # Set to false, if you don't want to see what the birds see

#pygame initialization
pygame.init()
fps = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32) 
pygame.display.set_caption('Sloppy Block')

#GlobalVariable Setup
bestWeights = [0,0,0,0]
player = None
multiPlayer = []
pipes = []
clouds = []
score = 0
running = True
font = pygame.font.SysFont("comicsansms", 72)
littlefont = pygame.font.SysFont("comicsansms", 16)
generation = 1
birdsToBreed = []
highscore = -1
highgen = 0
allTimeBestBird = None
maxscore = -1
blockPic = pygame.image.load("./img/block.png")
upperPipePic = pygame.image.load("./img/upperPipe.png")
lowerPipePic = pygame.image.load("./img/lowerPipe.png")
backgroundPic = pygame.image.load("./img/background.png")
cloudPic = pygame.image.load("./img/cloud.png")
singlePlayer = None

def init():
	"""This method is called whenever the game is started. This may be one of these cases
	1) First start (no matter if user or AI plays)
	2) If user plays: He died and clicked to restart
	3) If AI plays: The whole generation went extinct. This is a restart
	
	The method initializes Pipes, Clouds, the singleplayer bird, AI Birds

	INPUT: None
	OUTPUT: None"""

	global player, running, score, multiPlayer, singlePlayer
	
	#Initialize Pipes
	while (len(pipes) > 0): #Kill existing
		pipes.pop(0)
	initPipe()
	initPipe(w = WIDTH + WIDTH/2)

	#Initialize clouds
	while (len(clouds) > 0): #Kill existing
		clouds.pop(0)
	initCloud(w = 0)
	initCloud(w = WIDTH/2)
	initCloud(w = WIDTH)

	#Reset some global variables
	score = 0
	running = True

	if (not AI): #User plays: Initialize exactly one bird.
		multiPlayer = []
		singlePlayer = bird.Boord(HEIGHT)
		multiPlayer.append(singlePlayer)
	else:
		singlePlayer = bird.Boord(HEIGHT)
		if (len(birdsToBreed) == 0): #This is the first init. If a new generation is born, we will go on in the else below.
			for _ in range(BIRDS):
				#First time initialization of birds.
				multiPlayer.append(bird.Boord(HEIGHT))
		else:
			#Atleast one death happened
			multiPlayer = []
			#keep the best bird of generation without mutation
			_ = bird.Boord(HEIGHT)
			_.setWeights(birdsToBreed[0].weights)
			multiPlayer.append(_)
			
			#also keep the best of all time alive without mutation
			_ = bird.Boord(HEIGHT)
			_.setWeights(bestWeights)
			multiPlayer.append(_)
			
			for _ in range(int(BIRDS/3)): #Breed and mutate the two best birds of the generation a couple of times
				multiPlayer.append(bird.Boord(HEIGHT, birdsToBreed[0], birdsToBreed[1]))
			for _ in range(int(BIRDS/3)): #Breed and mutate the best bird of the generation a couple of times
				multiPlayer.append(bird.Boord(HEIGHT, birdsToBreed[0]))
			for _ in range(int(BIRDS/3)-2): #Breed and mutate the second best bird of the generation a couple of times
				multiPlayer.append(bird.Boord(HEIGHT, birdsToBreed[1]))
			
			if (ReplayBest): #Used to replay a very good bird
				multiPlayer[2].setWeights(Gen788BestOfBest)
			
			
			
def initPipe(w = WIDTH):
	"""Initializes a pipe, which will scroll in from the right

	INPUT: w - The width of the screen. The pipe will be created to the right of it
	OUTPUT: the initiated pipe inside of the global pipes list
	"""
	return pipes.append(pipe.pipe(w, HEIGHT))
	
def initCloud(w = WIDTH):
	"""Initializes a cloud, which will scroll in from the right, but slower than a pipe

	INPUT: w - The width of the screen. The cloud will be created to the right of it
	OUTPUT: the initiated cloud inside of the global clouds list
	"""
	return clouds.append(cloud.cloud(w, HEIGHT))


def draw(window):
	""" The draw method, which is called within the FPS or as soon as possible (if slower)
	It handles the background, clouds, pipes, player(s) and information

	INPUT: window - Here will be drawn.
	OUTPUT: None
	"""
	#print background
	window.blit(backgroundPic, (0,0))
	
	#print clouds
	for c in clouds:
		window.blit(cloudPic, (c.x, c.y))
		
	#print pipes
	for p in pipes:
		window.blit(upperPipePic, (p.x, p.uppery-HEIGHT-160))
		window.blit(lowerPipePic, (p.x, p.lowery))
		
	#birds
	for player in multiPlayer:
		if (player.alive):
			topleft = (BLOCKSIZE, player.y)
			rot = player.velocity*-5
			if (rot < -90): # Look down, not backwards. silly block
				rot = -90
			rotated_block = pygame.transform.rotate(blockPic, rot)
			new_rect = rotated_block.get_rect(center = blockPic.get_rect(topleft = topleft).center)
			
			window.blit(rotated_block, new_rect.topleft)
			if (birdView): # Draw what the birs can see
				pygame.draw.line(window, (255, 255, 255), (20 + BLOCKSIZE/2, player.y + BLOCKSIZE/2), (BLOCKSIZE/2 + player.distanceX, player.y + BLOCKSIZE/2))
				pygame.draw.line(window, (0, 255, 0), (20 + BLOCKSIZE/2, player.y + BLOCKSIZE/2), (20 + BLOCKSIZE/2, player.y + player.distanceTop))
				pygame.draw.line(window, (0, 0, 255), (20 + BLOCKSIZE/2, player.y + BLOCKSIZE/2), (20 + BLOCKSIZE/2, player.y + player.distanceBot))
				
	
#Let's roll! err.. fly!
init()

while True: # the game loop.
	draw(window) # Draw the fancy things.

	#Button controlling
	for event in pygame.event.get():
		if (event.type == 5) and (running) and (singlePlayer.alive): #click
			singlePlayer.velocity = -15
			print("clicked")
		elif (event.type == 5) and (not running) and (not singlePlayer.alive):
			init() #restart
		elif (event.type == 2): #keydown
			if (event.key == pygame.K_LEFT):
				FPSSES -= 15
			elif (event.key == pygame.K_RIGHT):	
				FPSSES += 15
			elif (event.key == 113):
				pygame.quit()
				sys.exit()
	
	if (running): #Atleast one bird is alive - Let's calculate
		#moveClouds
		for c in clouds:
			c.moveLeft()
			if (c.x < -120): #Cloud out of sight? spawn new
				initCloud()
				clouds.pop(0)
			
		#Pipe Handling including collision check
		for p in pipes:
			#Is Pipe gone? Pop it and spawn new one)
			if (p.x < -30):
				initPipe()
				pipes.pop(0)
				score += 1 #yay, score! (we passed a pipe)
				for player in multiPlayer: #Reward living birds
					if (player.alive):
						player.fitness += 3
				
			#Check if player collided with upper or lower pipe
			if ( ((p.x >= 20) and (p.x <= 20+BLOCKSIZE)) or ((p.x+20 >= 20) and (p.x+20 <= 20+BLOCKSIZE)) ): #pipe in X reach
				for player in multiPlayer: 
					if ( (player.alive) and ((player.y <= p.uppery) or (player.y >= p.lowery)) ): # also in y?
						#alive player hits a pipe
						player.alive = False
						player.fitness -= 1
			
			p.x -= 4 # Move the pipe to the left
		
		#Bird logic. 
		# Includes boundary checks (upper,lower end of screen)
		# Inputs to the neural net (what does the bird see)
		# FeedForward throught the neural net to decide if to jump
		noAlive = 0
		currentfitness = 0
		for player in multiPlayer:
			if (player.alive):
				#Velocity and upper/lower bounds handling (did the bird hit the ground/ceil)
				player.velocity += 1
				if (player.y + player.velocity > HEIGHT-BLOCKSIZE): #LowerBounds
					player.y = HEIGHT-BLOCKSIZE
					player.alive = False
					player.fitness -= 1
				elif (player.y + player.velocity < 1): #UpperBounds
					player.y = 0
					player.velocity = 0
					player.alive = False
					player.fitness -= 1
				else:
					player.y += player.velocity
					noAlive += 1
				
				#Update what the bird sees to make decisions
				p = pipes[0] # Closest pipe
				
				player.distanceTop = p.uppery - player.y
				player.distanceBot = p.lowery - player.y
				player.distanceX = p.x
				player.fitness += 0.01
				currentfitness = player.fitness
				
				#Jump or not?
				if ( (AI) and (player.thinkIfJump()) ):
					player.velocity = -15
	
		#TODO set highscore for non ai
	
		if (noAlive == 0):
			running = False #Everybody is dead. so sad. - Endscreentime
		
		#Report new Highscore if beaten
		for i in range(len(multiPlayer)):
			player = multiPlayer[i]
			if ( (player.fitness > highscore) and (not player.bestReported) ):
				player.bestReported = True
				print("New Highscore in Generation {} with score {}. Genes: {}".format(generation, score, player.weights))
		
		#Draw score and information
		text = font.render("Score {}".format(score), True, (0, 0, 128))
		window.blit(text,(WIDTH/2 - text.get_width() // 2, 0))
		text = littlefont.render("Fitness {}".format(round(currentfitness, 2)), True, (0, 0, 128))
		window.blit(text,(WIDTH - text.get_width(), 0))
		text = littlefont.render("Generation/Try {}".format(generation), True, (0, 0, 128))
		window.blit(text,(WIDTH - text.get_width(), text.get_height()))
		text = littlefont.render("Highscore {}".format(round(maxscore, 2)), True, (0, 0, 128))
		window.blit(text,(WIDTH - text.get_width(), text.get_height()*2))
		text = littlefont.render("Best generation {}".format(highgen), True, (0, 0, 128))
		window.blit(text,(WIDTH - text.get_width(), text.get_height()*3))
		text = littlefont.render("Blocks alive {}".format(noAlive), True, (0, 0, 128))
		window.blit(text,(WIDTH - text.get_width(), text.get_height()*4))
		text = littlefont.render("Max FPS: {} (KeyLeft and KeyRight to change)".format(FPSSES), True, (0, 0, 128))
		window.blit(text,(WIDTH - text.get_width(), text.get_height()*5))
		text = littlefont.render("Press q to quit".format(FPSSES), True, (0, 0, 128))
		window.blit(text,(WIDTH - text.get_width(), text.get_height()*6))
		
	else: #Player is dead (only seen, if user plays)
		text = font.render("You is ded.", True, (128, 0, 0))
		window.blit(text,(WIDTH/2 - text.get_width() // 2, HEIGHT/2 - text.get_height() // 2))
		text = font.render("Score {}".format(score), True, (128, 0, 0))
		window.blit(text,(WIDTH/2 - text.get_width() // 2, 0))
		text = littlefont.render("Highscore {}".format(round(maxscore, 2)), True, (128, 0, 0))
		window.blit(text,(WIDTH - text.get_width(), text.get_height()*2))

		if (AI): # Let' start breeding the corpses.
			birdsToBreed = []
			bestBird = -1
			bestFitness = -10
			for h in range(2): #Best two birds are taken
				for i in range(len(multiPlayer)): #Find the best bird
					player = multiPlayer[i]
					if (player.fitness > bestFitness):
						bestFitness = player.fitness
						bestBird = i
				if ( (h == 1) and (bestFitness > highscore) ): 
					#new highscore! Let's keep the bird and update our scores
					allTimeBestBird = multiPlayer[bestBird]
					bestWeights = copy.deepcopy(multiPlayer[bestBird].weights)
					print("highscore beaten {} - Generation {}".format(bestWeights, generation))
					highscore = bestFitness
					highgen = generation
					maxscore = score

				#store the (two) best birds in the breeding list	
				birdsToBreed.append(copy.deepcopy(multiPlayer[bestBird]))
				multiPlayer.pop(i)
			
			print("Best genes of this generation: {}".format(birdsToBreed[0].weights))
			generation += 1
			init() #Here we go again
			

	pygame.display.update()
	fps.tick(FPSSES)