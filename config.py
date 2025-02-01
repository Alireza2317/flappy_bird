import dataclasses
from typing import Tuple, TypeAlias

Color: TypeAlias = Tuple[int, int, int]




@dataclasses.dataclass
class FlappyBirdConfig:
	Dimensions: tuple[int, int] = (800, 650)
	BG_COLOR: Color = (20, 20, 20)
	fps: int = 60
	speed: int = 3

	# ground attributes
	ground_level: int = 500
	ground_thickness: int = 5
	ground_color: Color = (220, 220, 220)

	# pipes attributes
	pipe_width: int = 30
	pipe_gap: int = 50
	pipe_color: Color = (200, 0, 0)
	pipe_min_size: int = 100

	# player attributes
	player_x: int = 50

config = FlappyBirdConfig()