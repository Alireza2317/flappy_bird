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


class PipesPair:
	def __init__(self):
		self.init_rects()

		self.passed = False
		self.off_screen_left = False


	def init_rects(self):
		self.x = config.Dimensions[0]
		self.top_y = random.randint(100, config.ground_level - 100)
		self.bottom_y = self.top_y + config.pipe_gap

		self.top_rect = pg.Rect(
			self.x, 0,
			config.pipe_width, self.top_y
		)
		self.bottom_rect = pg.Rect(
			self.x, self.top_y + config.pipe_gap,
			config.pipe_width, self.bottom_y - config.ground_level
		)


	def draw(self, screen: pg.Surface):
		pg.draw.rect(screen, config.pipe_color, self.top_rect)
		pg.draw.rect(screen, config.pipe_color, self.bottom_rect)


	def update(self):
		self.x -= config.speed

		if self.x + config.pipe_width <= config.player_x:
			self.passed = True

		if self.x < -config.pipe_width:
			self.off_screen_left = True
		