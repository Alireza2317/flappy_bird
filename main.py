from config import FlappyBirdConfig
from flappy_bird import FlappyBirdGame

def main():
	conf = FlappyBirdConfig()

	game = FlappyBirdGame(conf)

	while True:
		game.step()

		if game.game_over:
			game.reset()


if __name__ == '__main__':
	main()
