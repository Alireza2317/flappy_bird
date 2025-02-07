from game import FlappyBirdGameAI

game = FlappyBirdGameAI()

while True:
	game.step()

	if game.game_over:
		game.reset()
