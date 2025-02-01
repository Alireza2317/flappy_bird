import sys
import pygame as pg
from config import config


class Bird:
	""" Bird's coordinates and navigation. """

	def __init__(self):
		# the bird's x coordinate is fixed
		# only the y coordinate changes
		# initally put the bird in the middle
		self.y: int = config.Dimensions[1] // 2

		# create the shape
		self.update()

		self.reset()


	def reset(self) -> None:
		self.flap: bool = False
		self.dead: bool = False


	def update(self) -> None:
		""" Update the pygame shape from the current coordinates. """

		self.shape = pg.Rect(
			config.player_x, self.y,
			config.player_width, config.player_height
		)


	def draw(self, screen: pg.Surface) -> None:
		""" Draw the bird shape on the given screen. """

		pg.draw.rect(
			screen,
			config.player_color,
			self.shape
		)


	def collided(self, shape: pg.Rect) -> bool:
		""" Returns wether the bird hit the given shape or not. """

		return pg.Rect.colliderect(self.shape, shape)


	def reached_ceil(self) -> bool:
		""" Returns wether the bird has reached the top of the screen. """

		return self.y <= 0


	


def main():
	pg.init()
	s = pg.display.set_mode(config.Dimensions)

	p = Bird()

	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()


		p.draw(s)

		pg.display.flip()

if __name__ == '__main__':
	main()
