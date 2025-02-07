import sys
import random
import pygame as pg
from config import config, Color



class Bird:
	""" Bird's coordinates and navigation. """

	def __init__(self, color: Color = config.bird_color):
		# the bird's x coordinate is fixed
		# only the y coordinate changes
		# initally put the bird in the middle

		self.color = color

		self.reset()

		# create the shape
		self.update()



	def reset(self) -> None:
		self._flap: bool = False
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
		# unlock flapping feature if bird starts going down
		#if self.y_velocity > 0:
		if self.y_velocity > 0.25 * config.flap_velocity:
			self._flap = False


		# unlock flapping feature if bird starts going down
		#if self.y_velocity > 0:
		if self.y_velocity > 0.25 * config.flap_velocity:
			self._flap = False

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
		if not self._flap and not self.reached_ceil():
			self.y_velocity = config.flap_velocity

			# lock flapping
			self._flap = True
		""" Returns wether the bird has reached the top of the screen. """

		return self.y <= 0


	def flap(self) -> None:
		""" Make the bird flap. """

		if not self._flap and not self.reached_ceil():
			self.y_velocity = config.flap_velocity

			# lock flapping
			self._flap = True


	def decide(self):
		if random.uniform(0, 1) > 0.57:
			self.flap()



class BirdPopulation:
	""" A population(generation) of birds. """

	def __init__(self, size: int):
		self.size: int = size

		self.reset()


	def reset(self):
		""" Recreates all the birds. """

		self.birds: list[Bird] = []

		for _ in range(self.size):
			random_color: Color = (
				random.randint(80, 255), random.randint(80, 255), random.randint(80, 255)
			)
			self.birds.append(Bird(random_color))


	def update(self):
		""" Makes a move for all birds and updates and draws them."""

		for bird in self.birds:
			if bird.dead:
				pass
			else:
				bird.decide()
				bird.update()
				bird.draw()


	def extinct(self):
		""" Returns True if all the birds died, else False. """

		for bird in self.birds:
			if not bird.dead:
				return False

		return True



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
