import dataclasses
from typing import Tuple, TypeAlias

Color: TypeAlias = Tuple[int, int, int]




@dataclasses.dataclass
class FlappyBirdConfig:
	Dimensions: tuple[int, int] = (800, 650)
	BG_COLOR: Color = (20, 20, 20)
	fps: int = 60
	ground_level: int = 500
	ground_thickness: int = 5
	ground_color: Color = (220, 220, 220)


config = FlappyBirdConfig()