import dataclasses


@dataclasses.dataclass
class FlappyBirdConfig:
	Dimensions: tuple[int, int] = (800, 650)
	BG_COLOR: tuple[int, int, int] = (20, 20, 20)
	fps: int = 10


game_config = FlappyBirdConfig()