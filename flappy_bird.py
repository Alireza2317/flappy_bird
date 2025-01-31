import sys
import pygame as pg
from typing import Optional
from config import FlappyBirdConfig

class FlappyBirdGame:
	def __init__(self, config: FlappyBirdConfig):
		self.cfg = config

		self.init_render()
		self.reset()

	def init_render(self):
		pg.init()
		self.clock = pg.time.Clock()
		self.screen = pg.display.set_mode(self.cfg.Dimensions)


	def reset(self):
		self.game_over = False

	def check_events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()


	def step(self):
		self.check_events()

		self.screen.fill(self.cfg.BG_COLOR)
		self.clock.tick(self.cfg.fps)
		pg.display.update()