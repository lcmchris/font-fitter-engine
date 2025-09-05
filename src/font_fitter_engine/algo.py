from PIL import ImageFilter
from PIL import Image
import numpy as np
from typing import Literal


class Algo:
    def __init__(
        self,
    ) -> None:
        pass

    def calculate(
        self, img: np.ndarray, calculation_area: tuple[int, int, int, int]
    ) -> float:
        raise NotImplementedError()
