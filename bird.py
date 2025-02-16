import sys
import random
import pygame as pg
from config import config, Color, VisionType
from neural_net import Network


class Bird:
	""" Bird's coordinates and navigation. """

	def __init__(self, color: Color = config.bird_color):
		# the bird's x coordinate is fixed
		# only the y coordinate changes
		# initally put the bird in the middle
		self.y: int = random.randint(
			int(config.ground_level * 0.25),
			int(config.ground_level * 0.75)
		)

		self.color = color

		self.brain: Network = Network()

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
		if self.y_velocity > 0.1 * config.flap_velocity:
			self._flap = False

		self.shape = pg.Rect(
			config.bird_x, self.y,
			config.bird_width, config.bird_height
		)


	def draw(self, screen: pg.Surface) -> None:
		""" Draw the bird shape on the given screen. """
		if not self.dead:
			pg.draw.rect(
				screen,
				self.color,
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

		if not self._flap and not self.reached_ceil():
			self.y_velocity = config.flap_velocity

			# lock flapping
			self._flap = True


	def decide(self, vision: VisionType = None):
		""" Decide flap or idle, based on the vision. """

		decision = random.uniform(0, 1)

		if decision > 0.972:
			self.flap()


class BirdPopulation:
	""" A population(generation) of birds. """

	def __init__(self, size: int = 50):
		self.size: int = size

		self.reset()


	def reset(self) -> None:
		""" Recreates all the birds. """

		self.birds: list[Bird] = []

		for _ in range(self.size):
			random_color: Color = (
				random.randint(80, 255), random.randint(80, 255), random.randint(80, 255)
			)
			self.birds.append(Bird(random_color))


	def update(self, screen: pg.Surface) -> None:
		""" Makes a move for all birds and updates and draws them."""

		dead_birds: list[int] = []

		for bird in self.birds:
			if bird.dead:
				dead_birds.append(bird)
			else:
				bird.decide()
				bird.update()
				bird.draw(screen)

		for dbird in dead_birds:
			self.birds.remove(dbird)


	def extinct(self) -> bool:
		""" Returns True if all the birds died, else False. """

		for bird in self.birds:
			if not bird.dead:
				return False

		return True


	def __len__(self) -> int:
		return len(self.birds)


def main():
	from components import Ground
	#random.seed()

	pg.init()
	s = pg.display.set_mode(config.Dimensions)

	g = Ground()
	g.draw(s)

	p = BirdPopulation(5)

	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()


		s.fill(config.BG_COLOR)
		g.draw(s)

		p.update(s)

		pg.display.flip()

if __name__ == '__main__':
	main()
