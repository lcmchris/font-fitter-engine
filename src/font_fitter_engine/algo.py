from PIL import ImageFilter
from PIL import Image
import numpy as np
from typing import Literal


class Algo:
    def __init__(self, glyph_set: list[str]) -> None:
        self.glyph_set = glyph_set

    def calculate(
        self,
        glyph: str,
        imgs: dict[str, Image.Image],
    ) -> float:
        raise NotImplementedError()


class BlurAlgo(Algo):
    def __init__(self, glyph_set, blur_radius: int) -> None:
        self.blur_radius = blur_radius
        super().__init__(glyph_set=glyph_set)

    def calculate(
        self,
        glyph: str,
        imgs: dict[str, Image.Image],
        spacing: int,
        direction: Literal["lsb", "rsb"],
    ):
        img = imgs[glyph]
        new_canvas = Image.new("RGBA", (1000, 1000))
        # Find center pixel of outer image
        center_x, center_y = (new_canvas.width // 2), (new_canvas.height // 2)

        # Offset inner image to align its center
        im2_x = center_x - (img.width // 2)
        im2_y = center_y - (img.height // 2)
        new_canvas.paste(img, (im2_x, im2_y))

        combined = new_canvas.filter(ImageFilter.GaussianBlur(radius=self.blur_radius))

        data = np.array(combined)  # "data" is a height x width x 4 numpy array

        np.zeros
        h, w, c = data.shape
        mid = w // 2
        split = data[:, mid - (spacing + img.width // 2) : mid, :]

        # split[..., :-1][dark_areas.T] = (0, 0)
        Image.fromarray(split).save(
            f"outputs/split_blurr_{glyph}.png",
        )
        return split.sum().item()
