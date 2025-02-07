from game import FlappyBirdGame

game = FlappyBirdGame()

while True:
	game.step()

	if game.game_over:
		game.reset()
