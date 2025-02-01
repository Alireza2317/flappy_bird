import random
import sys
import pygame as pg
from config import config

random.seed(23)

class Ground:
	"""
	Represents the ground

    Attributes:
        y (int): The y-coordinate of the ground, set to the ground level from config.
        rect (pg.Rect): The rectangle representing the ground.
	"""

	def __init__(self):
		# y coordinate of the ground
		self.y = config.ground_level

		# rect object
		self.rect = pg.Rect(
			0, self.y,
			config.Dimensions[0],
			config.ground_thickness
		)


	def draw(self, screen: pg.Surface):
		# draw the ground on the given screen
		pg.draw.rect(screen, config.ground_color, self.rect)


class PipesPair:
	"""
	Represents a pair of pipes

	Attributes:
		x (int): The x-coordinate of the pipes.
		top_y (int): The y-coordinate of the top pipe.
		bottom_y (int): The y-coordinate of the bottom pipe.
		top_rect (pg.Rect): The rectangle representing the top pipe.
		bottom_rect (pg.Rect): The rectangle representing the bottom pipe.
		passed (bool): Whether the player has passed the pipes.
		off_screen_left (bool): Whether the pipes are off the screen to the left.
	"""

	def __init__(self):
		self.init_coordinates()
		self.update_rects()

		self.passed = False
		self.off_screen_left = False


	def init_coordinates(self) -> None:
		"""
		Initialize the rectangles of the pipes.
		All pipes are initialized to be off the screen to the right.
		"""

		# x coordinate of the pipes, off the screen at the end
		self.x = config.Dimensions[0] - config.pipe_width

		# randomly generate the opening y coordinates
		self.top_y = random.randint(
			config.pipe_min_size,
			config.ground_level - config.pipe_gap - config.pipe_min_size
		)
		self.bottom_y = self.top_y + config.pipe_gap


	def update_rects(self) -> None:
		"""	Initialize the rectangles of the pipes.	"""

		# create the rects, based on the x coordinate which is variable
		self.top_rect = pg.Rect(
			self.x, 0,
			config.pipe_width, self.top_y
		)
		self.bottom_rect = pg.Rect(
			self.x, self.bottom_y,
			config.pipe_width, config.ground_level - self.bottom_y
		)


	def draw(self, screen: pg.Surface) -> None:
		"""	Draw the pipes on the given screen. """

		pg.draw.rect(screen, config.pipe_color, self.top_rect)
		pg.draw.rect(screen, config.pipe_color, self.bottom_rect)


	def __repr__(self):
		return f'PipesPair(ty={self.top_y}, by={self.bottom_y}, x={self.x})'


if __name__ == '__main__':
	pg.init()

	screen = pg.display.set_mode(config.Dimensions)
	clock = pg.time.Clock()

	ground = Ground()
	pipes = PipesPair()


	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()

		screen.fill(config.BG_COLOR)
		ground.draw(screen)


		pipes.x -= 10
		pipes.update_rects()
		pipes.draw(screen)

		clock.tick(40)
		pg.display.flip()