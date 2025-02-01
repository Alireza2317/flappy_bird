from game import FlappyBirdGame

def main():
	game = FlappyBirdGame()

	while True:
		game.step()

		if game.game_over:
			game.reset()


if __name__ == '__main__':
	main()
