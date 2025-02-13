import numpy as np
from typing import Callable

np.random.seed(23)


class Network:
	"""
	A very basic neural network for training the flappy-bird game.
	There are 4 input neurons, no hidden layers and only one output neuron.
	The 4 inputs represent:
		- the first 3 neurons are the bird's vision:
			- vertical distance to the top pipe
			- vertical distance to the bottom pipe
			- horizental distance to the pipe
		- the bias neuron

	The binary output:
		0: no flap
		1: flap
	"""

