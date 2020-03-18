# Sloppy-Block

## Description:
A genetic neural network learning approach to solve a flappy bird clone.
You may choose to either play yourself (by providing the -p command line parameter) or let the AI play.
If you would like to get a deeper understanding about what is happening and how the project grew over time, have a look at [This blog post](https://medium.com/@christian_deveaux/a-genetic-algorithm-solving-flappy-bird-using-data-science-87bcd981cefd) and of course the code itself.

Enjoy!

![Sloppy Block AI Gameplay](https://cdn-images-1.medium.com/max/800/1*8B636GWDV3arTgVhhi_YHQ.gif)

## Motivation and Summary
As a passionate gamer, who is diving into the field of data science, I was thinking about a project to put my skills to use and is a challenge at the same time.
What better way than to program a game, which an AI learns to play using data science methods.
I have heard from genetic algorithms before, but never programmed them myself.

As you can see from the embedded gifs, the machine is able to master the game, which fulfills the goal I have set to myself. Nevertheless I made further improvements and tweaks to the code after the initial completion of the project to smoothen out the game. For example, the graphics were introduced after the AI mastered the game. The inputs of the neural network went through some changes as well. Bird's view was implemented, etc. etc.

I hope you have a little bit of fun/learning effect when going through the code/game. I definitely enjoyed programming it.

![Sloppy Block AI Training](https://cdn-images-1.medium.com/max/600/1*nYnD-fJXfajOrCWzD6Vtxg.gif)

## Prerequisites/Python modules

The following environment was used to build this project:
* python 3.7.4
* conda 4.7.12
* pyGame 1.9.6
* numpy 1.16.5

## Installation and running
Download all files and start by typing `python main.py`
There are a few command line arguments, which may be passed. By default none of them are active.
* `--replayBest --humanPlayer --noBirdView --lowDetails`
	* `--replayBest (-r)`: Gives one of the AI birds provenly good genes
	* `--humanPlayer (-p)`: Allows the human to fly instead of the birds (play the game yourself)
	* `--noBirdView (-b)`: Disables the bird view (colored lines)
	* `--lowDetails (-d)`: Reduces details and thus increases FPS (good for training)
	* `--help (-h)`: Show help

### Repository structure
* `/img` - Assets used in the application
  * `background.png` - The background picture
  * `block.png` - A sloppy block (The player/AI)
	* `cloud.png` - A cloud in the background, which scrolls from right to left
	* `lowerpipe.png` - A picture for the lower boundary of a pipe pair
	* `upperpipe.png` - A picture for the upper boundary of a pipe pair
* `bird.py` - The bird class - Contains the neural network and the genetic algorithm
* `cloud.py` - The cloud class - Just there for a nice view
* `main.py` - The game logic itself, which instantiates the other classes and runs the main game loop
* `pipe.py` - The pipe class - The obstacles in the game are defined here
* `README.md` - This file

## Authors
Myself, but feel free to contribute :)

## Acknowledgements
* Udacity (https://www.udacity.com)
* Tutorials, and, of course, StackOverflow

# Licensing
The code is published under `GPL3`: https://www.gnu.org/licenses/gpl-3.0.en.html
