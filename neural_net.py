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
		self.activation: Callable[[float], float] = self.sigmoid

		self.forward()


	def forward(self, in_vector: np.ndarray | None = None) -> float:
		"""
		Performs a feed forward with the given input vector or self.input
		Returns the output value as a float.
		"""

		if in_vector is None:
			in_vector = self.input

		self.output_neuron: float = self.activation(
			self.weights.T @ in_vector
		)

		return self.output_neuron


	@staticmethod
	def sigmoid(z: float) -> float:
		return 1 / (1 + np.exp(-z))


def main():
	model = Network()
	in_vector = np.array([0.2, 0.1, 0.7, 0.4])
	model.forward(in_vector)

	print(model.weights)
	print(model.output_neuron)

if __name__ == '__main__':
	main()
