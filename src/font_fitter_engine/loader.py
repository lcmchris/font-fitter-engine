from fontTools import ttLib
from pathlib import Path
from fontTools.pens import freetypePen
from PIL.Image import Image


class Loader:
    def __init__(
        self,
        path,
        glyph_set: list[tuple[str | None, str | None]],
        save_dir: str | None = None,
    ) -> None:
        self.path = path
        self.glyph_set = glyph_set
        self.save_dir = save_dir
        pass

    def process(self):
        raise NotImplementedError


class TTF_Raster_Loader(Loader):
    def __init__(self, path, glyph_set, save_dir) -> None:
        super().__init__(path=path, glyph_set=glyph_set, save_dir=save_dir)

    def process(
        self,
    ):
        ttfont = self.load(path=self.path)
        imgs = self.rasterise(ttfont=ttfont, glyph_set=self.glyph_set)
        self.save(imgs=imgs, save_dir=self.save_dir)

        return imgs

    @classmethod
    def load(cls, path: str):
        path_b = Path(path)
        return ttLib.TTFont(path_b)

    @classmethod
    def save(cls, imgs: dict[str, Image], save_dir: str | None = "outputs/"):
        if save_dir is None:
            return
        for glyph, img in imgs.items():
            fmt = "png"
            img.save(fp=save_dir + f"{glyph}.{fmt}", format=fmt)

    @classmethod
    def rasterise(cls, ttfont: ttLib.TTFont, glyph_set) -> dict[str, Image]:
        pen = freetypePen.FreeTypePen(glyphSet=None)

        all_glyphs_unique = set()
        for left, right in glyph_set:
            if left is not None:
                all_glyphs_unique.add(left)
            if right is not None:
                all_glyphs_unique.add(right)

        images = {}
        glyph_set = ttfont.getGlyphSet()
        for glyph in all_glyphs_unique:
            glyph_set[glyph].draw(pen=pen)
            images[glyph] = pen.image()
        return images
