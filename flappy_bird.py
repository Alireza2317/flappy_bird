import sys
import random
import pygame as pg
from collections import deque
from config import config
from components import Ground, PipesPair


random.seed(23)

class FlappyBirdGame:
	"""
	Flappy Bird game class.

	Attributes:
		pipes (deque[PipesPair]): The deque of pipes.
		next_pipe_x (int): The x-coordinate of the next pipe to generate.
		ground (Ground): The ground object.
		game_over (bool): Whether the game is over.

	Methods:
		init_render(): Initializes the game screen.
		reset(): Resets the game state.
		check_events(): Checks for events.
		generate_pipes(): Generates a new pipes pair.
		update_pipes(): Updates the pipes.
		step(): Runs a single step of the game.

	"""

	def __init__(self):
		self.init_render()

		self.ground = Ground()
		self.pipes: deque[PipesPair] = deque([PipesPair()])

		self.reset()


	def init_render(self):
		"""	Initializes the game screen and pygame clock."""

		pg.init()
		pg.display.set_caption('Flappy Bird')

		self.clock = pg.time.Clock()
		self.screen = pg.display.set_mode(config.Dimensions)


	def reset(self):
		""" Resets the game to its initial state. """

		self.game_over = False
		self.next_pipe_x: int = config.Dimensions[0] + config.pipes_distance_range[0]

		self.screen.fill(config.BG_COLOR)


	def check_events(self):
		""" Checks for pygame events. """

		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()


	def _generate_pipes(self) -> None:
		"""
		Generates a new pipes pair and randomly generates the next pipe x coordinate.
		"""

		# add a new pair of pipes at the end of the screen
		self.pipes.append(PipesPair())

		# the distance between the next pipe and the end of the screen(newborn pipe)
		random_distance: int  = random.randint(*config.pipes_distance_range)

		# since the last pipe is at the end of the screen, the next pipe will be farther outside
		self.next_pipe_x = config.Dimensions[0] + random_distance


	def update_pipes(self):
		"""
		Updates the pipes by moving them to the left and generating new pipes if needed.
		"""

		# move the next pipe x coordinate to the left
		self.next_pipe_x -= config.speed

		# generate new pipes if the next pipe x coordinate is at the end of the screen
		# which means it should be drawn now
		if self.next_pipe_x <= config.Dimensions[0]:
			self._generate_pipes()

		# skip the update if there are no pipes yet
		if not self.pipes:
			return


		for pipe in self.pipes:
			# update the pipe rects
			pipe.update_rects()

			# move all the pipes to the left
			pipe.x -= config.speed

			# check if the bird has passed the pipe
			if pipe.x + config.pipe_width <= config.bird_x:
				pipe.passed = True

		# if the first pipe is off the screen to the left, remove it
		if self.pipes[0].x + config.pipe_width <= 0:
			self.pipes.popleft()


	def update_screen(self):
		self.screen.fill(config.BG_COLOR)
		self.ground.draw(self.screen)

		for pipe in self.pipes:
			pipe.draw(self.screen)

		self.clock.tick(config.fps)
		pg.display.flip()


	def step(self):
		self.check_events()

		self.update_pipes()

		self.update_screen()
