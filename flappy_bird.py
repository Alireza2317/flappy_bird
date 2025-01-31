from config import FlappyBirdConfig

class FlappyBirdGame:
	def __init__(self, config: FlappyBirdConfig):
		self.cfg = config
		self.reset()
		
	def reset(self):
		self.game_over = False

	def step(self):
		pass