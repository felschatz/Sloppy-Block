import sys
import copy
import pygame
import bird
import pipe

# todo: penalize weihths to mutate  worst link (top to bottom pipes)

#todo: when highscore is beat - give a hint about genes

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
"""

WIDTH = 640
HEIGHT = 480
BLOCKSIZE = 20
BIRDS = 90
Gen788BestOfBest = [ 1.39379687, -0.77627931, -0.59737657, -0.04154869]
FPSSES = 60

ReplayBest = False
AI = True # Set to false, if you want to play yourself

pygame.init()
fps = pygame.time.Clock()

window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32) # pygame.SRCALPHA
pygame.display.set_caption('Sloppy Block')

bestWeights = [0,0,0,0]
player = None
multiPlayer = []
pipes = []
score = 0
running = True
font = pygame.font.SysFont("comicsansms", 72)
littlefont = pygame.font.SysFont("comicsansms", 16)
endScreenSeen = False
generation = 1
birdsToBreed = []
highscore = -1
highgen = 0
allTimeBestBird = None
maxscore = -1
blockPic = pygame.image.load("./img/block.png")
upperPipePic = pygame.image.load("./img/upperPipe.png")
lowerPipePic = pygame.image.load("./img/lowerPipe.png")


def init():
	global player, running, score, multiPlayer, endScreenSeen
	#TODO if AI: 10 birds, else just one - Must be in an array of players
	player = bird.Boord(HEIGHT)
	while (len(pipes) > 0):
		pipes.pop(0)
	initPipe()
	initPipe(w = WIDTH + WIDTH/2)
	score = 0
	running = True
	if (AI):
		endScreenSeen = False
		if (len(birdsToBreed) == 0): #This is the first init. If a new generation is born, we will go on in the else below.
			for _ in range(BIRDS):
				multiPlayer.append(bird.Boord(HEIGHT))
		else:
			multiPlayer = []
			#keep the best bird if it was kind of fitness
			_ = bird.Boord(HEIGHT)
			_.setWeights(birdsToBreed[0].weights)
			multiPlayer.append(_)
			
			#also keep the best of all time alive
			_ = bird.Boord(HEIGHT)
			_.setWeights(bestWeights)
			multiPlayer.append(_)
			
			# We breed one thirdwith partner one third each of the birds alone just with mutation
			for _ in range(int(BIRDS/3)):
				multiPlayer.append(bird.Boord(HEIGHT, birdsToBreed[0], birdsToBreed[1]))
			for _ in range(int(BIRDS/3)):
				multiPlayer.append(bird.Boord(HEIGHT, birdsToBreed[0]))
			for _ in range(int(BIRDS/3)-2):
				multiPlayer.append(bird.Boord(HEIGHT, birdsToBreed[1]))
			
			if (ReplayBest): #Used to replay a very good bird
				multiPlayer[5].setWeights(Gen788BestOfBest)
			
			
			
def initPipe(w = WIDTH):
	return pipes.append(pipe.pipe(w, HEIGHT))

def draw(canvas):
	#background
	canvas.fill((0,0,0))
	
	#pipe
	for p in pipes:
		pygame.draw.rect(canvas, (255,0,0), (p.x, 0, 30, p.uppery))
		pygame.draw.rect(canvas, (255,0,0), (p.x, p.lowery, 30, HEIGHT-p.lowery))
		window.blit(lowerPipePic, (p.x, 640-p.uppery))
		window.blit(upperPipePic, (p.x, p.lowery))
		
		
		
	#bird
	if (not AI):
		pygame.draw.rect(canvas, (0,255,0), (BLOCKSIZE, player.y, BLOCKSIZE, BLOCKSIZE))
		window.blit(blockPic, (BLOCKSIZE, player.y))

	if (AI):
		i = 0
		for player in multiPlayer:
			if (player.alive):
				pygame.draw.rect(canvas, (0,255-i,0+i), (BLOCKSIZE, player.y, BLOCKSIZE, BLOCKSIZE))
				window.blit(blockPic, (BLOCKSIZE, player.y))
				i += 5
				i %= 255
	
init()

while True:
	draw(window)
	
	if (not AI): # Logic for manual gaming (only one bird and not training/fitness)
		#Button controlling
		for event in pygame.event.get():
			#print(event)
			if (event.type == 5): #click
				print("clicked")
				if (running):
					player.velocity = -10
				else:
					init()
			elif (event.type == 2): #keydown
				pygame.quit()
				sys.exit()
		
		if (running):
			#Collision check
			for p in pipes:
				#Is Pipe gone? Pop it and spawn new one)
				if (p.x < 0-30):
					initPipe()
					pipes.pop(0)
					score += 1 #yay, score!
				#Check if player collided with upper or lower pipe
				if ( ((p.x >= 20) and (p.x <= 20+BLOCKSIZE)) or ((p.x+20 >= 20) and (p.x+20 <= 20+BLOCKSIZE)) ): #X is correct, might be hitting on y
					if ( (player.y <= p.uppery) or (player.y >= p.lowery) ):
						running = False	
				p.x -= 4
			
			#Velocity and upper/lower bounds handling
			player.velocity += 1
			if (player.y + player.velocity > HEIGHT-BLOCKSIZE): #LowerBounds
				player.y = HEIGHT-BLOCKSIZE
				running = False
			elif (player.y + player.velocity < 1): #UpperBounds
				player.y = 0
				player.velocity = 0
				running = False
			else:
				player.y += player.velocity
			

		
			#Draw score
			text = font.render("Score {}".format(score), True, (0, 128, 0))
			window.blit(text,(WIDTH/2 - text.get_width() // 2, 0))
		
		else: #Player is dead
			text = font.render("You is ded.", True, (128, 0, 0))
			window.blit(text,(WIDTH/2 - text.get_width() // 2, HEIGHT/2 - text.get_height() // 2))
			text = font.render("Score {}".format(score), True, (128, 0, 0))
			window.blit(text,(WIDTH/2 - text.get_width() // 2, 0))
				
	else: # AI is in control
		#Button controlling
		for event in pygame.event.get():
			if (event.type == 5): #click
				print("clicked")
				if (not running):
					init()
			elif (event.type == 2): #keydown
				if (event.key == pygame.K_LEFT):
					FPSSES -= 15
				elif (event.key == pygame.K_RIGHT):	
					FPSSES += 15
				else:
					pygame.quit()
					sys.exit()
		
		if (running):
			#Collision check
			for p in pipes:
				#Is Pipe gone? Pop it and spawn new one)
				if (p.x < 0-30):
					initPipe()
					pipes.pop(0)
					score += 1 #yay, score!
					for player in multiPlayer:
						if (player.alive):
							player.fitness += 3
					# TODO: increase fitness for living birds
					
				#TODO for b in birds
				#Check if player collided with upper or lower pipe
				if ( ((p.x >= 20) and (p.x <= 20+BLOCKSIZE)) or ((p.x+20 >= 20) and (p.x+20 <= 20+BLOCKSIZE)) ): #birds might be hitting pipes - check Y next
					for player in multiPlayer:
						if ( (player.alive) and ((player.y <= p.uppery) or (player.y >= p.lowery)) ):
							#alive player hits a pipe
							player.alive = False
							player.fitness -= 1
				
				p.x -= 4
			
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
					player.distanceBot = p.lowery + player.y
					player.distanceX = p.x
					player.fitness += 0.01
					currentfitness = player.fitness
					
					#Jump or not?
					if (player.thinkIfJump()):
						player.velocity = -10
		
			if (noAlive == 0):
				running = False #Everybody is dead. so sad.
			
			#Report new Highscore
			for i in range(len(multiPlayer)):
				player = multiPlayer[i]
				if ( (player.fitness > highscore) and (not player.bestReported) ):
					player.bestReported = True
					print("New Highscore in Generation {} with score {}. Genes: {}".format(generation, score, player.weights))
			
			#Draw score
			text = font.render("Score {}".format(score), True, (0, 128, 0))
			window.blit(text,(WIDTH/2 - text.get_width() // 2, 0))
			text = littlefont.render("Fitness {}".format(round(currentfitness, 2)), True, (0, 128, 0))
			window.blit(text,(0, 0))
			text = littlefont.render("Generation {}".format(generation), True, (0, 128, 0))
			window.blit(text,(0, text.get_height()))
			text = littlefont.render("Highscore {}".format(round(maxscore, 2)), True, (0, 128, 0))
			window.blit(text,(0, text.get_height()*2))
			text = littlefont.render("Best generation {}".format(highgen), True, (0, 128, 0))
			window.blit(text,(0, text.get_height()*3))
			text = littlefont.render("Blocks alive {}".format(noAlive), True, (0, 128, 0))
			window.blit(text,(0, text.get_height()*4))
			text = littlefont.render("Speed: {} (KeyLeft and KeyRight to change)".format(FPSSES), True, (0, 128, 0))
			window.blit(text,(0, text.get_height()*5))
			
			
		else: #Player is dead
			text = font.render("You is ded.", True, (128, 0, 0))
			window.blit(text,(WIDTH/2 - text.get_width() // 2, HEIGHT/2 - text.get_height() // 2))
			text = font.render("Score {}".format(score), True, (128, 0, 0))
			window.blit(text,(WIDTH/2 - text.get_width() // 2, 0))
			text = littlefont.render("Generation {}".format(generation), True, (0, 128, 0))
			window.blit(text,(0, text.get_height() + 5))
			
			
			if (not endScreenSeen):
				endScreenSeen = True
				#TODO get fittest birds, Update network weights slightly, initialize new networks
				#TODO Should be top three birds who live on - potentially breed with mutations?!
				birdsToBreed = []
				bestBird = -1
				bestFitness = -10
				for h in range(2):
					for i in range(len(multiPlayer)):
						player = multiPlayer[i]
						if (player.fitness > bestFitness):
							bestFitness = player.fitness
							bestBird = i
					if ( (h == 1) and (bestFitness > highscore) ):
						allTimeBestBird = multiPlayer[bestBird]
						bestWeights = copy.deepcopy(multiPlayer[bestBird].weights)
						print("highscore beaten \n{} - Generation {}".format(bestWeights, generation))
						highscore = bestFitness
						highgen = generation
						maxscore = score
						
					birdsToBreed.append(copy.deepcopy(multiPlayer[bestBird]))
					multiPlayer.pop(i)
				
				print("Best genes of this generation: {}".format(birdsToBreed[0].weights))
				#print("The best bird had a fitness of {}. It will be bred with the second best ({}) and the offspring will live on to fly or die another round!".format(birdsToBreed[0].fitness, birdsToBreed[1].fitness))
				#print(birdsToBreed[0].weights)
				#todo reinit or something
				#todo overwrite the other boords with the best boord instead of initializing everything. Could give the weights to the bird constructor.
				#multiPlayer[bestBird].alive = True
				generation += 1
				init()
			

	pygame.display.update()
	fps.tick(FPSSES)