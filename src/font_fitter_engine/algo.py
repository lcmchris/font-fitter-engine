from PIL import ImageFilter
from PIL import Image
import numpy as np


class Algo:
    def __init__(self, glyph_set: list[tuple[str, str]]) -> None:
        self.glyph_set = glyph_set

    def calculate(self, *args, **kwargs) -> float:
        raise NotImplementedError()

    @staticmethod
    def get_concat_h(im1: Image.Image, im2: Image.Image, gap: int):
        dst = Image.new(
            "RGBA", (im1.width + im2.width + gap, im1.height), color=(0, 0, 0)
        )
        dst.paste(im1, (0, 0))
        dst.paste(im2, (im1.width + gap, 0))
        return dst


class BlurAlgo(Algo):
    def __init__(self, glyph_set, blur_radius: int) -> None:
        self.blur_radius = blur_radius
        super().__init__(glyph_set=glyph_set)

    @classmethod
    def get_dummy_img(
        cls,
        height,
        color: tuple[int, int, int],
        width=50,
    ):
        return Image.new("RGBA", size=(width, height), color=color)

    @staticmethod
    def grayscale_to_color(image: Image.Image, new_color=(255, 0, 0)):
        new_image = Image.new("RGBA", image.size, "WHITE")
        new_image.paste(image, (0, 0), image)
        new_image = new_image.convert("RGBA")

        ##recolor
        data = np.array(new_image)
        red, green, blue, alpha = data.T
        not_white_areas = ~((red == 255) & (blue == 255) & (green == 255))
        data[..., :-1][not_white_areas.T] = new_color
        white_areas = (red == 255) & (blue == 255) & (green == 255)
        data[..., :-1][white_areas.T] = (0, 0, 0)
        return Image.fromarray(data)

    def calculate(self, pair: tuple[str, str], imgs: dict[str, Image.Image], gap: int):
        left_color = (255, 0, 0)
        right_color = (0, 0, 255)
        left, right = pair
        if left == "None" and right == "None":
            raise ValueError("Both in glyph set is None!")

        elif left == "None":
            right_img = imgs[right]
            right_img = self.grayscale_to_color(right_img, right_color)
            left_img = self.get_dummy_img(right_img.height, left_color)

        elif right == "None":
            left_img = imgs[left]
            left_img = self.grayscale_to_color(left_img, left_color)
            right_img = self.get_dummy_img(left_img.height, right_color)

        else:
            left_img = self.grayscale_to_color(imgs[left], left_color)
            right_img = self.grayscale_to_color(imgs[right], right_color)

        combined = self.get_concat_h(left_img, right_img, gap)

        combined = combined.filter(ImageFilter.GaussianBlur(radius=self.blur_radius))

        return self.calc_metric(combined, pair)

    @staticmethod
    def calc_metric(im: Image.Image, pair) -> int:
        data = np.array(im)  # "data" is a height x width x 4 numpy array
        red, green, blue, alpha = data.T  # Temporarily unpack the bands for readability

        violet_areas = (red > 0) & (blue > 0)

        data[..., :-1][violet_areas.T] = (255, 255, 255)

        Image.fromarray(data).save(f"outputs/{pair[0]}_{pair[1]}_overlap.png")

        return violet_areas.sum().item()
