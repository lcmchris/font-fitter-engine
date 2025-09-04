class Algo:
    def __init__(self, glyph_set) -> None:
        self.glyph_set = glyph_set

    @classmethod
    def calculate_spacing(cls, output):
        raise NotImplementedError()


from PIL import ImageFilter
from PIL.Image import Image


class BlurAlgo(Algo):
    def __init__(self, glyph_set) -> None:
        super().__init__(glyph_set=glyph_set)

    def calculate_spacing(self, output: dict[str, Image]):
        imgs = self.blur(imgs=output)

        for left, right in self.glyph_set:
            if left is None:
                pass
            if right is None:
                pass

        return

    @classmethod
    def blur(cls, imgs: dict[str, Image], radius=30):
        for glyph, img in imgs.items():
            img = img.filter(ImageFilter.GaussianBlur(radius=radius))

        return imgs
