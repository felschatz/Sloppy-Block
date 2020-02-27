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

		Noteworthy that it does not jump to time the pipe (so it will pass the pipe in the middle). this might eb solved with a deeper neural network
		better fitness algorithm. adapt weights stronger, which failed (hit upper pipe? bad fitness on upper pipe distance - hit ground? bad fitness there)
		Mutation method change - instead of taking average of first two birds - exchange whole genes

		Screenshots of complex and easy network with connections

		Possible Improvement: Only breed if died not too far from each other.

		core differences to the known original:
			Harder. The jumping power is far closer to the length of the pipe opening
			Harder. The original has the pipe opening starting closer to the middle
			Harder. The pipe distance varies and is not always the same

		Making the game easier (decrease jump strength, increase distance between the pipes) makes the network learn much faster, since the error tolerance is higher

		tackle local optimum problem, if no improvement has been made over 10 generations

		adapt mutations based on score (the higher the score, the lower the mutation)

		dependencies

		BirdView, singleplayer, etc. via variables on run

		scaling the weights between 0 and 1 did not lead to any usable results and thus was cancelled.


		Think about hidden layer

			# Network size
			N_input = 4
			N_hidden = 3
			N_output = 2

			np.random.seed(42)
			# Make some fake data
			X = np.random.randn(4)

			weights_input_to_hidden = np.random.normal(0, scale=0.1, size=(N_input, N_hidden))
			weights_hidden_to_output = np.random.normal(0, scale=0.1, size=(N_hidden, N_output))


			# TODO: Make a forward pass through the network

			hidden_layer_in = np.dot(X, weights_input_to_hidden)
			hidden_layer_out = sigmoid(hidden_layer_in) # TODO should be relu

			print('Hidden-layer Output:')
			print(hidden_layer_out)

			output_layer_in = np.dot(hidden_layer_out, weights_hidden_to_output)
			output_layer_out = sigmoid(output_layer_in)

			print('Output-layer Output:')
			print(output_layer_out)
"""

#Initialize constants
WIDTH = 640 #screensize
HEIGHT = 480 #screensize
BLOCKSIZE = 20 #Blocks Fatness for bounding box
BIRDS = 90 #No of Blocks to spawn
startWithGenes = [-0.00929749, -1.00681071,  0.18271884,  0.05724841, -0.00808077]
#Agent1
#[-0.00929749, -1.00681071,  0.18271884,  0.05724841,  0.03691923]
#[-0.00929749, -1.00681071,  0.18271884,  0.05724841, -0.00808077]
#Agent2
#[ 4.91317090e-04, -1.35293646e+00,  2.38520797e-01, -1.33855450e-02, 5.96446731e-01]
#Agent3
#[ 0.00629361 -1.77223725 -0.47061318 -0.08176     0.07842931]
#[ 0.00629361 -1.77223725 -0.41061318 -0.15676     0.10342931]
#[ 0.00629361 -1.79723725 -0.35561318 -0.08176     0.05842931]
#[ 0.00629361 -1.77223725 -0.37561318 -0.08176     0.07842931]
#[ 0.00629361 -1.82723725 -0.47061318 -0.08176     0.07842931]
#[-0.01370639 -1.85723725 -0.50061318 -0.08176     0.07842931]
#[ 0.00629361 -1.77223725 -0.34561318 -0.08176     0.15342931]
#[-0.01870639 -1.77223725 -0.46061318 -0.08176     0.07842931]
#[ 0.00629361 -1.84723725 -0.44061318 -0.08176     0.07842931]
#[ 0.00629361 -1.77223725 -0.47061318 -0.08176     0.00342931]
#Agent4
#[-0.02561535 -0.97467903 -0.02342398  0.00120641 -0.09594272]
#Agent5
#[-0.03757691 -1.08349227  0.06785001  0.02430801  0.10286512]
#[-0.03757691 -0.90849227 -0.03714999 -0.01569199  0.10286512]
#Agent6 (previous 2500+, now 5500+)
#[0.07501671614310677, -1.8986725080550475, 0.11944445335069942, 0.10365745399374016, -0.23842049490076667]
#Agent7 (previous 1600+, now 100.000)
#[-0.019484295705243557, -1.3649741315987505, -0.1789322087070267, 0.021642987041061858, 0.017495788379428195]

FPSSES = 60 #Increase by pressing +/-
VELOCITYGAIN = -13 #Global difficulty setting ;)

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
bestWeights = [0,0,0,0,0]
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

def init():
	"""This method is called whenever the game is started.
		This may be one of these cases
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
			_.setWeights(birdsToBreed[0].weights)
			multiPlayer.append(_)

			#also keep the best of all time alive without mutation
			_ = bird.Boord(HEIGHT)
			_.setWeights(bestWeights)
			multiPlayer.append(_)

			for _ in range(int(BIRDS/3)):
				#Breed and mutate the two generations best birds sometimes
				multiPlayer.append(bird.Boord(HEIGHT, birdsToBreed[0],
												birdsToBreed[1]))
			for _ in range(int(BIRDS/3)):
				#Breed and mutate the generations best bird a couple of times
				multiPlayer.append(bird.Boord(HEIGHT, birdsToBreed[0]))
			for _ in range(int(BIRDS/3)-2):
				#Breed and mutate the generations second best bird asometimes
				multiPlayer.append(bird.Boord(HEIGHT, birdsToBreed[1]))

			if (ReplayBest): #Used to replay a very good bird
				multiPlayer[2].setWeights(startWithGenes)



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

				if (birdView): # Draw what the birds can see
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
		text = littlefont.render("Press q to quit".format(FPS), True, textColor)
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
						print("Genes of {}: {}".format(i, player.weights))
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
				print("New Highscore in Generation {} with score {}. Genes: {}"
						.format(generation, score, player.weights))

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

			bestFitness = -10
			if ( (score > 0) or (maxscore > 0) or (globalFitness > 0.2) ):
				#Only if atleast one bird made it through one pipe
				birdsToBreed = []
				bestBird = -1
				for h in range(2): #Best two birds are taken
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
						bestWeights = copy.deepcopy(multiPlayer[bestBird].weights)
						print("highscore beaten {} - Generation {}"
								.format(bestWeights, generation))
						highscore = bestFitness
						highgen = generation
						maxscore = score

					#store the (two) best birds in the breeding list
					birdsToBreed.append(copy.deepcopy(multiPlayer[bestBird]))
					multiPlayer.pop(i)

				print("Best genes of this generation: {}"
						.format(birdsToBreed[0].weights))


			generation += 1
			init() #Here we go again

	#pygame updates
	pygame.display.update()
	fps.tick(FPSSES)
