# Sloppy-Block
A genetic neural network learning approach to solve a flappy bird clone.
Play yourself, let AI play

#TODO Prerequisites/Python modules etc.

## Description:
TODO
add gifs

## Prerequisites
TODO

## Installation and running
Download all files and start by typing `python main.py`
There are a few command line arguments, which may be passed:
* `--replayBest --humanPlayer --noBirdView --lowDetails`
	* `--replayBest (-r)`: Gives one of the AI birds provenly good genes
	* `--humanPlayer (-p)`: Allows the human to fly instead of the birds
	* `--noBirdView (-b)`: Disables the bird view (colored lines)
	* `--lowDetails (-d)`: Reduces details and thus increases FPS
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
* `Other Files` - Other files are git related (readme/screenshots)

## Authors
Myself, but feel free to contribute :)

## Acknowledgements
* Udacity (https://www.udacity.com)
* Tutorials, and, of course, StackOverflow

# Licensing
The code is published under `GPL3`: https://www.gnu.org/licenses/gpl-3.0.en.html