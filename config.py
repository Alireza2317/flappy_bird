import dataclasses
from typing import Tuple, TypeAlias

Color: TypeAlias = Tuple[int, int, int]
VisionType: TypeAlias = tuple[float, float, float]


@dataclasses.dataclass
class FlappyBirdConfig:
	Dimensions: tuple[int, int] = (1250, 900)
	BG_COLOR: Color = (20, 20, 20)
	fps: int = 60
	speed: float = 2.5

	# ground attributes
	ground_level: int = int(Dimensions[1] * 0.85)
	ground_thickness: int = 5
	ground_color: Color = (220, 220, 220)

	# pipes attributes
	pipe_width: int = 30
	pipe_gap: int = 250
	pipe_color: Color = ground_color
	pipe_min_size: int = 100

	pipes_distance_range: tuple[int, int] = (Dimensions[0] // 4, Dimensions[0] // 1.8)

	# bird attributes
	bird_x: int = 50
	bird_width: int = 30
	bird_height: int = 45
	bird_color: Color = (108, 206, 238)


	gravity_step: float = speed / 40
	gravity_max_velocity: float = speed
	flap_velocity: float = -gravity_max_velocity * 0.8


config = FlappyBirdConfig()