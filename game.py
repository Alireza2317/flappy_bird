import sys
import random
import pygame as pg
from collections import deque
from config import config
from components import Ground, PipesPair
from bird import Bird


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

		self.reset()


	def init_render(self):
		"""	Initializes the game screen and pygame clock."""

		pg.init()
		pg.display.set_caption('Flappy Bird')

		self.clock = pg.time.Clock()
		self.screen = pg.display.set_mode(config.Dimensions)
		self.font = pg.font.Font(pg.font.get_default_font(), 24)


	def reset(self):
		""" Resets the game to its initial state. """

		self.score: int = 0
		self.game_over = False
		self.passed_pipe = False

		self.next_pipe_x: int = config.Dimensions[0] + config.pipes_distance_range[0]

		self.pipes: deque[PipesPair] = deque([PipesPair()])
		self.bird = Bird()

		self.screen.fill(config.BG_COLOR)


	def check_events(self):
		""" Checks for pygame events. """

		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()

			if event.type == pg.KEYDOWN:
				if event.key == pg.K_UP:
					self.bird.flap()
					self.bird.flapping = False


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
			pipe.update()

			# move all the pipes to the left
			pipe.x -= config.speed

			# check if the bird has passed the pipe
			if pipe.x + config.pipe_width <= config.bird_x:
				pipe.passed = True

		# if the first pipe is off the screen to the left, remove it
		if self.pipes[0].x + config.pipe_width <= 0:
			self.pipes.popleft()


	def update_text(self):
		text_sf = self.font.render(
			f'Score: {self.score:>3}', True, config.ground_color
		)

		self.screen.blit(text_sf, (10, (config.Dimensions[1]-config.ground_level) // 2 + config.ground_level))


	def update_screen(self):
		self.screen.fill(config.BG_COLOR)
		self.ground.draw(self.screen)

		for pipe in self.pipes:
			pipe.draw(self.screen)

		self.bird.draw(self.screen)

		self.update_text()

		self.clock.tick(config.fps)
		pg.display.flip()


	def update(self):
		""" Updates all the components and the bird. """

		self.bird.update()
		self.update_pipes()


	def bird_collided(self):
		""" Checks wether the bird collided with the pipes or the ground. """

		colide_ground = self.bird.collided(self.ground.rect)
		colide_top_pipe = self.bird.collided(self.pipes[0].top_rect)
		colide_bottom_pipe = self.bird.collided(self.pipes[0].bottom_rect)

		return (colide_ground or colide_top_pipe or colide_bottom_pipe)


	def step(self):
		"""
		One step in the game loop.
		Running the game, handling logic and user input and updating the game on the screen.
		"""

		# check for user input
		self.check_events()

		# check if the bird hit any of the pipes or the ground:
		if self.bird_collided():
			self.bird.dead = True
			self.game_over = True

		if not self.pipes[0].passed:
			self.passed_pipe = False

		if self.pipes[0].passed and not self.passed_pipe:
			self.score += 1
			self.passed_pipe = True





		self.update()

		self.update_screen()
