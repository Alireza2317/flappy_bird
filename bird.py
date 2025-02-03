import sys
import random
import pygame as pg
from config import config


class Bird:
	""" Bird's coordinates and navigation. """

	def __init__(self):
		# the bird's x coordinate is fixed
		# only the y coordinate changes
		# initally put the bird in the middle
		self.y: int = config.Dimensions[1] // 2

		self.reset()

		# create the shape
		self.update()



	def reset(self) -> None:
		self.flapping: bool = False
		self.dead: bool = False
		self.y_velocity: float = 0


	def update(self) -> None:
		""" Update the pygame shape from the current coordinates. """

		# the bird goes down
		self.y += self.y_velocity

		# and the gravity pull gets stronger
		self.y_velocity = min(
			self.y_velocity + config.gravity_step,
			config.gravity_max_velocity
		)

		self.shape = pg.Rect(
			config.bird_x, self.y,
			config.bird_width, config.bird_height
		)


	def draw(self, screen: pg.Surface) -> None:
		""" Draw the bird shape on the given screen. """

		pg.draw.rect(
			screen,
			config.bird_color,
			self.shape
		)


	def collided(self, shape: pg.Rect) -> bool:
		""" Returns wether the bird hit the given shape or not. """

		return pg.Rect.colliderect(self.shape, shape)


	def reached_ceil(self) -> bool:
		""" Returns wether the bird has reached the top of the screen. """

		return self.y <= 0


	def flap(self) -> None:
		""" Make the bird flap. """

		if not self.flapping and not self.reached_ceil():
			self.flapping = True
			self.y_velocity = -config.gravity_max_velocity * 0.8


	def decide(self):
		if random.uniform(0, 1) > 0.57:
			self.flap()


def main():
	pg.init()
	s = pg.display.set_mode(config.Dimensions)

	p = Bird()

	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()

			if event.type == pg.KEYDOWN:
				if event.key == pg.K_UP:
					p.flap()
					p.flapping = False


		s.fill(config.BG_COLOR)
		p.draw(s)
		p.update()

		pg.display.flip()

if __name__ == '__main__':
	main()
