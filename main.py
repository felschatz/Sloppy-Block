import sys
import copy
import pygame
import numpy as np
import bird
import pipe
import cloud

#Initialize constants
WIDTH = 640 #screensize
HEIGHT = 480 #screensize
BLOCKSIZE = 20 #Blocks Fatness for bounding box
BIRDS = 90 #No of Blocks to spawn
FPSSES = 60 #Increase by pressing +/-
VELOCITYGAIN = -13 #Global difficulty setting ;)
startInputGenes = 	[[-0.25244961, -0.02443948, -0.04505735],
					 [ 0.12788692, -0.80005974, -0.13429437],
					 [-0.04354413, -0.1765287,   0.02494303],
					 [-0.21573609,  0.03459365,  0.07858856],
					 [-0.38443484, -0.00344752, -0.19479629]]
startHiddenGenes =	[[-0.49624301],
					 [ 0.1133263 ],
					 [-0.00213796]]

ReplayBest = False #Set to true, if you want to use trained network
AI = True # Set to false, if you want to play yourself
birdView = True # Set to false, if you don't want to see what the birds see
HIGHDETAILS = True # Set to false to efficiently train.

for opt in sys.argv:
	if (opt == "main.py"):
		continue
	elif ( (opt == "-h") or (opt == "--help") ):
		print("main.py --replayBest --humanPlayer --noBirdView --lowDetails")
		print("--replayBest (-r): Gives one of the AI birds provenly good genes")
		print("--humanPlayer (-p): Allows the human to fly instead of the" \
				" birds (play the game yourself)")
		print("--noBirdView (-b): Disables the bird view (colored lines)")
		print("--lowDetails (-d): Reduces details and thus increases FPS " \
				"(good for training)")
		print("--help (-h): Show help")
		sys.exit()
	elif opt in ("-r", "--replayBest"):
		ReplayBest = True
	elif opt in ("-p", "--humanPlayer"):
		AI = False
	elif opt in ("-b", "--noBirdView"):
		birdView = False
	elif opt in ("-d", "--lowDetails"):
		HIGHDETAILS = False
	else:
		print("Unknown argument.\r\n")
		print("main.py --replayBest --humanPlayer --noBirdView --lowDetails")
		print("--replayBest (-r): Gives one of the AI birds provenly good genes")
		print("--humanPlayer (-p): Allows the human to fly instead of the "\
		 		"birds (play the game yourself)")
		print("--noBirdView (-b): Disables the bird view (colored lines)")
		print("--lowDetails (-d): Reduces details and thus increases FPS " \
				"(good for training)")
		print("--help (-h): Show help")
		sys.exit()

#pygame initialization
pygame.init()
fps = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Sloppy Block')
blockPic = pygame.image.load("./img/block.png")
upperPipePic = pygame.image.load("./img/upperPipe.png")
lowerPipePic = pygame.image.load("./img/lowerPipe.png")
backgroundPic = pygame.image.load("./img/background.png")
cloudPic = pygame.image.load("./img/cloud.png")
pygame.display.set_icon(blockPic) #set Icon

#GlobalVariable Setup
bestInputWeights = [0,0,0,0,0]
bestHiddenWeights = [0,0,0]
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
highscore = 0
highgen = 0
allTimeBestBird = None
maxscore = 0
singlePlayer = None
globalFitness = 0.0
respawn = False

def init():
	"""This method is called whenever the game is started.
		This may be one of these cases
		1) First start (no matter if user or AI plays)
		2) If user plays: He died and clicked to restart
		3) If AI plays: The whole generation went extinct. This is a restart
		The method initializes Pipes, Clouds, the singleplayer bird, AI Birds

	INPUT: None
	OUTPUT: None"""

	global player, running, score, multiPlayer, singlePlayer, respawn

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
		if (len(birdsToBreed) == 0):
			#This is the first init. New ones, are covered in the else below.
			for _ in range(BIRDS):
				#First time initialization of birds.
				multiPlayer.append(bird.Boord(HEIGHT))
		else:
			#Atleast one death happened
			multiPlayer = []
			#keep the best bird of generation without mutation
			_ = bird.Boord(HEIGHT)
			_.setWeights(birdsToBreed[0].inputWeights,
						birdsToBreed[0].hiddenWeights)
			multiPlayer.append(_)

			#also keep the best of all time alive without mutation
			_ = bird.Boord(HEIGHT)
			_.setWeights(birdsToBreed[0].inputWeights,
						birdsToBreed[0].hiddenWeights)
			multiPlayer.append(_)

			for _ in range(int(BIRDS/3)):
				#Breed and mutate the two generations best birds sometimes
				multiPlayer.append(bird.Boord(HEIGHT, birdsToBreed[0],
												birdsToBreed[1]))
			for _ in range(int(BIRDS/3)):
				#Breed and mutate the generations best bird a couple of times
				multiPlayer.append(bird.Boord(HEIGHT, birdsToBreed[0]))

			for _ in range(int(BIRDS/3)-2):
				if (respawn): #Bad genes - replace some.
					multiPlayer.append(bird.Boord(HEIGHT))
				else:
					#Breed and mutate the generations second best bird asometimes
					multiPlayer.append(bird.Boord(HEIGHT, birdsToBreed[1]))

			if (ReplayBest): #Used to replay a very good bird
				multiPlayer[2].setWeights(startInputGenes, startHiddenGenes)

			if (respawn):
				respawn = False
				print("Due to natural selection - one third of birds " +
						"receives new genes")

def initPipe(w = WIDTH):
	"""Initializes a pipe, which will scroll in from the right

	INPUT: w - The width of the screen.
				The pipe will be created to the right of it
	OUTPUT: the initiated pipe inside of the global pipes list
	"""
	dist = 0
	for p in pipes:
		dist = p.x
	return pipes.append(pipe.pipe(w, HEIGHT, dist))

def initCloud(w = WIDTH):
	"""Initializes a cloud, which will scroll in from the right,
		but slower than a pipe

	INPUT: w - The width of the screen.
				The cloud will be created to the right of it
	OUTPUT: the initiated cloud inside of the global clouds list
	"""
	return clouds.append(cloud.cloud(w, HEIGHT))


def draw(window):
	""" The draw method, which is called within the FPS
			or as soon as possible (if slower)
	It handles the background, clouds, pipes, player(s) and information
	If the static variable HIGHDETAILS is set
		it will print all birds and nice pictures and rotations.
	If HIGHDETAILS is not set
	 	only one bird will be drawn
		also everything is rectangles instead of pictures

	INPUT: window - Here will be drawn.
	OUTPUT: None
	"""
	#Low Detail mode.
	if (not HIGHDETAILS):
		pygame.draw.rect(window, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
		for p in pipes:
			pygame.draw.rect(window, (255, 0, 0), (p.x, 0, 30, p.uppery))
			pygame.draw.rect(window, (255, 0, 0), (p.x, p.lowery, 30, HEIGHT))

	if (HIGHDETAILS):
		#print background
		window.blit(backgroundPic, (0,0))

		#print clouds
		for c in clouds:
			window.blit(cloudPic, (c.x, c.y))

		#print pipes
		for p in pipes:
			window.blit(upperPipePic, (p.x, p.uppery-HEIGHT-160))
			window.blit(lowerPipePic, (p.x, p.lowery))

	if (AI):
		drawNeuralNet(window)

	#birds
	drewBird = False
	for player in multiPlayer:

		if (player.alive):
			if (HIGHDETAILS):
				topleft = (BLOCKSIZE, player.y)
				rot = player.velocity*-5
				if (rot < -90): # Look down, not backwards. silly block
					rot = -90
				rotated_block = pygame.transform.rotate(blockPic, rot)
				new_rect = rotated_block.get_rect(
						center = blockPic.get_rect(topleft = topleft).center)

				window.blit(rotated_block, new_rect.topleft)

				if ( (birdView) and (AI) ): # Draw what the birds can see
					pygame.draw.line(window, (0, 255, 0),
									(20 + BLOCKSIZE/2, player.y + BLOCKSIZE/2),
									(BLOCKSIZE/2 + player.distanceX,
									player.y + player.distanceTop))
					pygame.draw.line(window, (0, 0, 255),
									(20 + BLOCKSIZE/2, player.y + BLOCKSIZE/2),
									(BLOCKSIZE/2 + player.distanceX,
									player.y + player.distanceBot))
					pygame.draw.line(window, (255, 255, 255),
									(20 + BLOCKSIZE/2, player.y + BLOCKSIZE/2),
									(20 + BLOCKSIZE/2,
									player.y + BLOCKSIZE/2 + player.velocity))
					pygame.draw.line(window, (255, 255, 255),
									(20 + BLOCKSIZE/2, player.y + BLOCKSIZE/2),
									(20 + BLOCKSIZE/2,
									player.y + BLOCKSIZE/2 - player.velocity))
			elif ( (not HIGHDETAILS) and (not drewBird) ):
				#Low detail mode - just one bird to draw
				pygame.draw.rect(window, (0, 255, 0),
									(20,  player.y, BLOCKSIZE, BLOCKSIZE))
				drewBird = True

def drawScores(alive, score, highscore, fitness=None, gen=None, maxGen=None,
				noAlive=None, FPS=None):
	"""Draw scores on screen. Score content depends on the fact,
		if the player(s) is/are alive

	INPUT:  alive - Which details to draw? If not alive:
	 				The player played himself
					and does not need all pieces of information
			WIDTH - The global width
			HEIGHT - The global height
			fitness - The current fitness
			gen - The current generation
			maxGen - The generation with the highest score
			noAlive - The number of alive birds
			FPS - The frames per second, which are currently set
			score - The current score
			highscore - The best score, which was currently achieved
	OUTPUT: None"""

	textColor = (0, 0, 128)
	if (not HIGHDETAILS):
		textColor = (0, 128, 0)
	if (alive):
		text = font.render("Score {}".format(score), True, textColor)
		window.blit(text,(WIDTH/2 - text.get_width() // 2, 0))
		text = littlefont.render("Fitness {}".format(round(fitness, 2)), True,
									textColor)
		window.blit(text,(WIDTH - text.get_width(), 0))
		text = littlefont.render("Generation/Try {}".format(gen), True,
									textColor)
		window.blit(text,(WIDTH - text.get_width(), text.get_height()))
		text = littlefont.render("Highscore {}".format(round(maxscore, 2)),
									True, textColor)
		window.blit(text,(WIDTH - text.get_width(), text.get_height()*2))
		text = littlefont.render("Best generation {}".format(maxGen), True,
									textColor)
		window.blit(text,(WIDTH - text.get_width(), text.get_height()*3))
		text = littlefont.render("Blocks alive {}".format(noAlive), True,
									textColor)
		window.blit(text,(WIDTH - text.get_width(), text.get_height()*4))
		text = littlefont.render("Max FPS: {} (KeyLeft and KeyRight to change)"
									.format(FPSSES), True, textColor)
		window.blit(text,(WIDTH - text.get_width(), text.get_height()*5))
		text = littlefont.render("Press q to quit, d to toggle details, b to toggle bird view".format(FPS), True, textColor)
		window.blit(text,(WIDTH - text.get_width(), text.get_height()*6))
	else:
		text = font.render("You is ded.", True, (128, 0, 0))
		window.blit(text,(WIDTH/2 - text.get_width() // 2,
							HEIGHT/2 - text.get_height() // 2))
		text = font.render("Score {}".format(score), True, (128, 0, 0))
		window.blit(text,(WIDTH/2 - text.get_width() // 2, 0))
		text = littlefont.render("Highscore {}".format(round(highscore, 2)),
									True, (128, 0, 0))
		window.blit(text,(WIDTH - text.get_width(), text.get_height()*2))

def drawNeuralNet(window):
	"""This function draws the neural net onto the screen

	INPUT: None
	OUTPUT: None"""

	#Get alive bird and its weights to draw nicely later
	birdo = getAliveBird()
	if (birdo == None):
		return

	birdBrainInput = birdo.inputWeights
	birdBrainHidden = birdo.hiddenWeights

	minInput = np.min(birdBrainInput)
	maxInput = np.max(birdBrainInput)
	meanInput = np.sum(birdBrainInput) / len(birdBrainInput)

	normInput = (birdBrainInput - minInput)/(maxInput-minInput)

	minHidden = np.min(birdBrainHidden)
	maxHidden = np.max(birdBrainHidden)
	meanHidden = np.sum(birdBrainHidden) / len(birdBrainHidden)

	normHidden = (birdBrainHidden - minHidden)/(maxHidden-minHidden)

	pygame.draw.circle(window, (255,0,0), (WIDTH-200, HEIGHT-250), 10, 1)
	pygame.draw.circle(window, (255,0,0), (WIDTH-200, HEIGHT-200), 10, 1)
	pygame.draw.circle(window, (255,0,0), (WIDTH-200, HEIGHT-150), 10, 1)
	pygame.draw.circle(window, (255,0,0), (WIDTH-200, HEIGHT-100), 10, 1)
	pygame.draw.circle(window, (255,0,0), (WIDTH-200, HEIGHT-50), 10, 1)

	pygame.draw.line(window, (normInput[0][0]*255, 255-normInput[0][0]*255, 0),
					(WIDTH-200+10, HEIGHT-250),
					(WIDTH-125-10, HEIGHT-200), 1)

	pygame.draw.line(window, (normInput[0][1]*255, 255-normInput[0][1]*255, 0),
					(WIDTH-200+10, HEIGHT-250),
					(WIDTH-125-10, HEIGHT-150), 1)

	pygame.draw.line(window, (normInput[0][2]*255, 255-normInput[0][2]*255, 0),
					(WIDTH-200+10, HEIGHT-250),
					(WIDTH-125-10, HEIGHT-100), 1)

	pygame.draw.line(window, (normInput[1][0]*255, 255-normInput[1][0]*255, 0),
					(WIDTH-200+10, HEIGHT-200),
					(WIDTH-125-10, HEIGHT-200), 1)
	pygame.draw.line(window, (normInput[1][1]*255, 255-normInput[1][1]*255, 0),
					(WIDTH-200+10, HEIGHT-200),
					(WIDTH-125-10, HEIGHT-150), 1)
	pygame.draw.line(window, (normInput[1][2]*255, 255-normInput[1][2]*255, 0),
					(WIDTH-200+10, HEIGHT-200),
					(WIDTH-125-10, HEIGHT-100), 1)

	pygame.draw.line(window, (normInput[2][0]*255, 255-normInput[2][0]*255, 0),
					(WIDTH-200+10, HEIGHT-150),
					(WIDTH-125-10, HEIGHT-200), 1)
	pygame.draw.line(window, (normInput[2][1]*255, 255-normInput[2][1]*255, 0),
					(WIDTH-200+10, HEIGHT-150),
					(WIDTH-125-10, HEIGHT-150), 1)
	pygame.draw.line(window, (normInput[2][2]*255, 255-normInput[2][2]*255, 0),
					(WIDTH-200+10, HEIGHT-150),
					(WIDTH-125-10, HEIGHT-100), 1)

	pygame.draw.line(window, (normInput[3][0]*255, 255-normInput[3][0]*255, 0),
					(WIDTH-200+10, HEIGHT-100),
					(WIDTH-125-10, HEIGHT-200), 1)
	pygame.draw.line(window, (normInput[3][1]*255, 255-normInput[3][1]*255, 0),
					(WIDTH-200+10, HEIGHT-100),
					(WIDTH-125-10, HEIGHT-150), 1)
	pygame.draw.line(window, (normInput[3][2]*255, 255-normInput[3][2]*255, 0),
					(WIDTH-200+10, HEIGHT-100),
					(WIDTH-125-10, HEIGHT-100), 1)

	pygame.draw.line(window, (normInput[4][0]*255, 255-normInput[4][0]*255, 0),
					(WIDTH-200+10, HEIGHT-50),
					(WIDTH-125-10, HEIGHT-200), 1)
	pygame.draw.line(window, (normInput[4][1]*255, 255-normInput[4][1]*255, 0),
					(WIDTH-200+10, HEIGHT-50),
					(WIDTH-125-10, HEIGHT-150), 1)
	pygame.draw.line(window, (normInput[4][2]*255, 255-normInput[4][2]*255, 0),
					(WIDTH-200+10, HEIGHT-50),
					(WIDTH-125-10, HEIGHT-100), 1)

	pygame.draw.circle(window, (255,0,0), (WIDTH-125, HEIGHT-200), 10, 1)
	pygame.draw.circle(window, (255,0,0), (WIDTH-125, HEIGHT-150), 10, 1)
	pygame.draw.circle(window, (255,0,0), (WIDTH-125, HEIGHT-100), 10, 1)

	pygame.draw.line(window, (normHidden[0]*255, 255-normHidden[0]*255, 0),
					(WIDTH-125+10, HEIGHT-200),
					(WIDTH-50-10, HEIGHT-150), 1)
	pygame.draw.line(window, (normHidden[1]*255, 255-normHidden[1]*255, 0),
					(WIDTH-125+10, HEIGHT-150),
					(WIDTH-50-10, HEIGHT-150), 1)
	pygame.draw.line(window, (normHidden[2]*255, 255-normHidden[2]*255, 0),
					(WIDTH-125+10, HEIGHT-100),
					(WIDTH-50-10, HEIGHT-150), 1)

	pygame.draw.circle(window, (255,0,0), (WIDTH-50, HEIGHT-150), 10, 1)

def getAliveBird():
	"""Returns a random alive bird.

	INPUT: None
	OUTPUT: BirdObject or None, if no bird is alive"""
	for player in multiPlayer:
		if (player.alive):
			return player

	return None

#Let's roll! err.. fly!
init()

while True: # the game loop.
	draw(window) # Draw the fancy things.
	currentfitness = 0.0

	#Button controlling
	for event in pygame.event.get():
		if (event.type == 5) and (running): #click
			if (not AI):
				singlePlayer.velocity = VELOCITYGAIN
			if (AI):
				print("Score of alive birds:")
				for i in range(len(multiPlayer)):
					player = multiPlayer[i]
					if (player.alive):
						print("Genes of {}: Input: {}\n Hidden: {}".format(i,
								player.inputWeights, player.hiddenWeights))
		elif (event.type == 5) and (not running) and (not singlePlayer.alive):
			init() #restart
		elif (event.type == 2): #keydown
			if (event.key == pygame.K_LEFT):
				FPSSES -= 15
			elif (event.key == pygame.K_RIGHT):
				FPSSES += 15
			elif (event.key == 113): #q
				pygame.quit()
				sys.exit()
			elif (event.key == 100): #d
				HIGHDETAILS = not HIGHDETAILS
			elif (event.key == 98): #b
				birdView = not birdView

	if (running): #Atleast one bird is alive - Let's calculate
		#moveClouds
		for c in clouds:
			c.moveLeft()
			if (c.x < -140): #Cloud out of sight? spawn new
				initCloud()
				clouds.pop(0)

		#Pipe Handling including collision check
		for p in pipes:
			#Is Pipe gone? Pop it and spawn new one)
			if (p.x < -30):
				pipes.pop(0)
				initPipe()
				score += 1 #yay, score! (we passed a pipe)
				for player in multiPlayer: #Reward living birds
					if (player.alive):
						player.fitness += 3

			p.moveLeft() # Move the pipe to the left

		#Bird logic.
		# Includes boundary checks (upper,lower end of screen)
		# Inputs to the neural net (what does the bird see)
		# FeedForward through the neural net to decide if to jump
		noAlive = 0

		p = pipes[0] # Closest pipe

		for player in multiPlayer:
			if (player.alive):
				player.velocity += 1
				#Did the bird hit anything?
				player.handleCollision(HEIGHT, BLOCKSIZE, p)
				if (player.alive):
					player.y += player.velocity
					noAlive += 1
				#Update what the bird sees to make decisions
				player.processBrain(p.uppery, p.lowery, p.x)
				currentfitness = player.fitness
				globalFitness = player.fitness

				#Jump or not?
				if ( (AI) and (player.thinkIfJump()) ):
					player.velocity = VELOCITYGAIN

		if (noAlive == 0):
			running = False #Everybody is dead. so sad. - Endscreentime

		#Report new Highscore if beaten
		for i in range(len(multiPlayer)):
			player = multiPlayer[i]
			if ( (player.fitness > highscore) and (not player.bestReported) ):
				player.bestReported = True
				print("New Highscore in Generation {} with score {}. " \
						"Genes: {}\n{}".format(generation, score,
								player.inputWeights, player.hiddenWeights))

		#Draw score and information
		drawScores(alive=True, fitness=currentfitness, gen=generation,
					maxGen=highgen, noAlive=noAlive, FPS=FPSSES, score=score,
					highscore=maxscore)

	else: #Player is dead (only seen, if user plays)
		if (not AI): #User played - highscore set?
			if (score > maxscore):
				maxscore = score
				highgen = generation

			drawScores(alive=False, score=score, highscore=maxscore)

		if (AI): # Let' start breeding the corpses.
			if ( (score > 0) or (maxscore > 0) or (globalFitness > 0.2) ):
				#Only if atleast one bird made it through one pipe
				birdsToBreed = []
				for h in range(2): #Best two birds are taken
					bestBird = -1
					bestFitness = -10
					for i in range(len(multiPlayer)): #Find the best bird
						player = multiPlayer[i]
						if (player.fitness > bestFitness):
							bestFitness = player.fitness
							bestBird = i
							if (bestFitness >= highscore):
								highscore = bestFitness
					if ( (h == 1) and (bestFitness >= highscore) ):
						#new highscore! Let's keep the bird and update our scores
						allTimeBestBird = multiPlayer[bestBird]
						bestInputWeights =  copy.deepcopy(
											multiPlayer[bestBird].inputWeights)
						bestHiddenWeights =  copy.deepcopy(
											multiPlayer[bestBird].hiddenWeights)
						print("highscore beaten {}\n{} - Generation {}"
								.format(player.inputWeights,
										player.hiddenWeights, generation))
						highscore = bestFitness
						highgen = generation
						maxscore = score

					#store the (two) best birds in the breeding list
					birdsToBreed.append(copy.deepcopy(multiPlayer[bestBird]))
					multiPlayer.pop(i)

				print("Best genes of this generation: {}\n{}"
						.format(birdsToBreed[0].inputWeights,
								birdsToBreed[0].hiddenWeights))

			#If no progress was made in the last 50 generations - new genes.
			if (generation-highgen > 50):
				respawn = True

			generation += 1
			init() #Here we go again

	#pygame updates
	pygame.display.update()
	fps.tick(FPSSES)
