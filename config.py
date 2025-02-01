import dataclasses
from typing import Tuple, TypeAlias

Color: TypeAlias = Tuple[int, int, int]




@dataclasses.dataclass
class FlappyBirdConfig:
	Dimensions: tuple[int, int] = (800, 650)
	BG_COLOR: Color = (20, 20, 20)
	fps: int = 60
	speed: int = 2

	# ground attributes
	ground_level: int = 550
	ground_thickness: int = 5
	ground_color: Color = (220, 220, 220)

	# pipes attributes
	pipe_width: int = 30
	pipe_gap: int = 100
	pipe_color: Color = ground_color
	pipe_min_size: int = 100

	pipes_distance_range: tuple[int, int] = (Dimensions[0] // 5, Dimensions[0] // 1.8)

	# player attributes
	player_x: int = 50
	player_width: int = 30
	player_height: int = 50
	player_color: Color = (120, 50, 220)

config = FlappyBirdConfig()