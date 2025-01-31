import sys
import pygame as pg
from config import config
from components import Ground

class FlappyBirdGame:
	def __init__(self):
		self.init_render()
		self.reset()

		self.ground = Ground()

	def init_render(self):
		pg.init()
		self.clock = pg.time.Clock()
		self.screen = pg.display.set_mode(config.Dimensions)


	def reset(self):
		self.game_over = False

	def check_events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()


	def update_screen(self):
		#self.screen.fill(config.BG_COLOR)
		self.clock.tick(config.fps)
		pg.display.flip()


	def step(self):
		self.check_events()

		self.ground.draw(self.screen)

		self.update_screen()