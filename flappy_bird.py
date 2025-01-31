import sys
import pygame as pg
from config import game_config

class FlappyBirdGame:
	def __init__(self):

		self.init_render()
		self.reset()

	def init_render(self):
		pg.init()
		self.clock = pg.time.Clock()
		self.screen = pg.display.set_mode(game_config.Dimensions)


	def reset(self):
		self.game_over = False

	def check_events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()


	def step(self):
		self.check_events()

		self.screen.fill(game_config.BG_COLOR)
		self.clock.tick(game_config.fps)
		pg.display.update()
