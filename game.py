import sys
import random
import pygame as pg
from collections import deque
from typing import TypeAlias
from config import config, VisionType
from components import Ground, PipesPair
from bird import Bird, BirdPopulation

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

		self.new_pipe_x: int = config.Dimensions[0] + config.pipes_distance_range[0]

		self.pipes: deque[PipesPair] = deque([PipesPair()])
		self.bird = Bird()

		self._previous_next_pipe = self.pipes[0]

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


	def _generate_pipes(self) -> None:
		"""
		Generates a new pipes pair and randomly generates the next pipe x coordinate.
		"""

		# add a new pair of pipes at the end of the screen
		self.pipes.append(PipesPair())

		# the distance between the next pipe and the end of the screen(newborn pipe)
		random_distance: int  = random.randint(*config.pipes_distance_range)

		# since the last pipe is at the end of the screen, the next pipe will be farther outside
		self.new_pipe_x = config.Dimensions[0] + random_distance


	def update_pipes(self):
		"""
		Updates the pipes by moving them to the left and generating new pipes if needed.
		"""

		# move the next pipe x coordinate to the left
		self.new_pipe_x -= config.speed

		# generate new pipes if the next pipe x coordinate is at the end of the screen
		# which means it should be drawn now
		if self.new_pipe_x <= config.Dimensions[0]:
			self._generate_pipes()

		# skip the update if there are no pipes yet
		if self.next_pipe is None:
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
		if self.next_pipe.x + config.pipe_width <= 0:
			self.pipes.popleft()


	@property
	def next_pipe(self) -> PipesPair | None:
		""" Returns the first pipe which is not passed. """

		if self.pipes:
			for pipe in self.pipes:
				if not pipe.passed:
					return pipe
		return None


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


	def check_collisions(self) -> None:
		""" Checks wether the bird collided with the pipes or the ground. """

		colide_ground = self.bird.collided(self.ground.rect)

		colide_top_pipe = False
		colide_bottom_pipe = False

		if self.next_pipe is not None:
			colide_top_pipe = self.bird.collided(self.next_pipe.top_rect)
			colide_bottom_pipe = self.bird.collided(self.next_pipe.bottom_rect)

		if (colide_ground or colide_top_pipe or colide_bottom_pipe):
			self.bird.dead = True
			self.game_over = True


	def update_score(self):
		"""
		Updates the score based on the bird's position and the number of pipes it passed.
		"""

		if not self.pipes:
			return

		if self.next_pipe != self._previous_next_pipe:
			self.score += 1
			self._previous_next_pipe = self.next_pipe


	def step(self):
		"""
		One step in the game loop.
		Running the game, handling logic and user input and updating the game on the screen.
		"""

		# check for user input
		self.check_events()

		# check if the bird hit any of the pipes or the ground:
		self.check_collisions()

		# update the current score based on the bird passing the pipe
		self.update_score()

		# update all the components and the bird
		self.update()

		# update the visual elements on the screen
		self.update_screen()



class FlappyBirdGameAI(FlappyBirdGame):
	def __init__(self):
		super().__init__()

		self.update_visions()


	def reset(self):
		super().reset()

		del self.bird

		self.population = BirdPopulation()


	def check_events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()

			if event.type == pg.KEYDOWN:
				if event.key == pg.K_KP_PLUS:
					config.speed = min(config.speed+1, config.bird_width-1)
				if event.key == pg.K_KP_MINUS:
					config.speed = max(config.speed-1, 1)


	def check_collisions(self) -> None:
		for bird in self.population.birds:
			colide_ground = bird.collided(self.ground.rect)

			colide_top_pipe = False
			colide_bottom_pipe = False

			if self.next_pipe is not None:
				colide_top_pipe = bird.collided(self.next_pipe.top_rect)
				colide_bottom_pipe = bird.collided(self.next_pipe.bottom_rect)

			if (colide_ground or colide_top_pipe or colide_bottom_pipe):
				bird.dead = True

		if self.population.extinct():
			self.game_over = True


	def update_text(self):
		score_text_sf = self.font.render(
			f'Score: {self.score:>3}', True, config.ground_color
		)

		alives_text_sf = self.font.render(
			f'Alive Birds: {len(self.population):>3}', True, config.ground_color
		)

		self.screen.blit(
			score_text_sf, (10, (config.Dimensions[1]-config.ground_level) // 3 + config.ground_level)
		)
		self.screen.blit(
			alives_text_sf, (10, 2 * (config.Dimensions[1]-config.ground_level) // 3 + config.ground_level)
		)


	def update(self):
		self.population.update(self.screen, visions=self.visions)
		self.update_pipes()


	def update_screen(self):
		self.screen.fill(config.BG_COLOR)
		self.ground.draw(self.screen)

		for pipe in self.pipes:
			pipe.draw(self.screen)


		for bird in self.population.birds:
			bird.draw(self.screen)

		self.update_visions(draw=True)

		self.update_text()

		self.clock.tick(config.fps)
		pg.display.flip()


	def _draw_visions(self, bird: Bird, vision: VisionType) -> None:
		""" Draw the vision lines for the bird based on vision parameters. """

		# from bird to the pipes(horizental distance)
		pg.draw.line(
			self.screen, bird.color,
			(config.bird_x, bird.shape.centery),
			(config.bird_x + int(vision[2] * config.ground_level), bird.shape.centery),
			width=1
		)

		# from bird to the top pipe and bottom pipe (vertical distance)
		pg.draw.line(
			self.screen, bird.color,
			(bird.shape.centerx, self.next_pipe.top_y),
			(bird.shape.centerx, self.next_pipe.bottom_y),
			width=1
		)


	def update_visions(self, draw: bool = True) -> None:
		"""
		Updating the vision of each bird in the population.
		Args:
			draw: wether to draw the vision lines or not.

		Each vision contains 3 elements:
			- vertical distance to the top pipe
			- vertical distance to the bottom pipe
			- horizental distance to the pipe
		"""

		# if there are still no pipes
		if not self.pipes:
			return

		self.visions: list[VisionType] = []

		for bird in self.population.birds:
			# elements in vision
			# first element is vertical distance to top pipe
			v1: float = max(0, bird.shape.centery - self.next_pipe.top_y)

			# second element is vertical distance to bottom pipe
			v2: float = max(0, self.next_pipe.bottom_y - bird.shape.centery)

			# third element is horizental distance to pipes
			v3: float = max(0, self.next_pipe.x - config.bird_x)

			# normalize all vision elements
			v1 /= config.ground_level
			v2 /= config.ground_level
			v3 /= config.ground_level

			# update visions list
			vision: VisionType = (v1, v2, v3)
			self.visions.append(vision)

			if draw:
				self._draw_visions(bird, vision)


	def step(self):
		self.check_events()

		self.check_collisions()

		self.update_score()

		self.update()
		self.update_screen()

