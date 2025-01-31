import random
import pygame as pg
from config import config

random.seed(23)

class Ground:
	def __init__(self):
		self.x, self.y = 0, config.ground_level

		self.rect = pg.Rect(
			self.x, self.y,
			config.Dimensions[0],
			config.ground_thickness
		)

	def draw(self, screen: pg.Surface):
		pg.draw.rect(screen, config.ground_color, self.rect)


class Pipes:
	pass