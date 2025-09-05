from font_fitter_engine.algo import Algo
from PIL import Image
from typing import Literal
import numpy as np


class BlurAlgo(Algo):
    def __init__(self, blur_radius: int) -> None:
        self.blur_radius = blur_radius
        super().__init__()

    def calculate(
        self,
        glyph: str,
        imgs: dict[str, Image.Image],
        spacing: int,
        direction: Literal["lsb", "rsb"],
    ):
        img = imgs[glyph].convert("LA")
        new_canvas = Image.new("LA", (1000, 1000), color=(0, 0))
        # Find center pixel of outer image
        center_x, center_y = (new_canvas.width // 2), (new_canvas.height // 2)

        # Offset inner image to align its center
        im2_x = center_x - (img.width // 2)
        im2_y = center_y - (img.height // 2)
        new_canvas.paste(img, (im2_x, im2_y))

        combined = new_canvas.filter(
            Image.ImageFilter.GaussianBlur(radius=self.blur_radius)
        )

        data = np.array(combined)  # "data" is a height x width x 4 numpy array

        h, w, c = data.shape
        mid = w // 2
        split = data[:, mid - (spacing + img.width // 2) : mid]
        luminance = split[:, :, 0]
        alpha = split[:, :, 1]
        area = np.sum(alpha > 0).item()

        Image.fromarray(split).save(
            f"outputs/split_blurr_{glyph}.png",
        )
        return area
