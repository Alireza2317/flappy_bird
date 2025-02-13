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

	def __init__(self):
		self.input: np.ndarray = np.zeros((4,))
		self.weights: np.ndarray = np.random.random((4,))
		self.activation: Callable = self.sigmoid

		self.forward()


	def forward(self) -> None:
		self.output_neuron: float = self.activation(
			self.weights.T @ self.input
		)


	@staticmethod
	def sigmoid(z: float) -> float:
		return 1 / (1 + np.exp(-z))
