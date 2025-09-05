from fontTools import ttLib
from pathlib import Path
from fontTools.pens import freetypePen
from fontTools.ttLib.tables._c_m_a_p import table__c_m_a_p
from fontTools.ttLib.tables._h_m_t_x import table__h_m_t_x
from fontTools.ttLib.tables._g_l_y_f import table__g_l_y_f
from fontTools.ttLib.tables._h_h_e_a import table__h_h_e_a
from fontTools.ttLib.scaleUpem import scale_upem
import numpy as np
from PIL import Image

from dataclasses import dataclass


@dataclass
class GlyphSpacing:
    xMin: int
    yMin: int
    xMax: int
    yMax: int
    advance: int
    lsb: int
    rsb: int
    ascent: int
    descent: int


@dataclass
class ImgOut:
    array: np.ndarray
    center_x: int
    height: int
    glyph_size: tuple[
        int,
        int,
    ]  # x1,y1


class Loader:
    def __init__(
        self,
        glyph_set: list[str],
        save_dir: str | None = None,
    ) -> None:
        self.glyph_set = glyph_set
        self.save_dir = save_dir
        pass

    def process(self) -> dict[str, ImgOut]:
        raise NotImplementedError

    def load(self, path: Path) -> None:
        raise NotImplementedError

    def get_spacing(self) -> dict[str, GlyphSpacing]:
        raise NotImplementedError


class TTF_Loader(Loader):
    def __init__(self, glyph_set, save_dir) -> None:
        self.ttf_font = None
        super().__init__(glyph_set=glyph_set, save_dir=save_dir)

    def process(
        self,
    ) -> dict[str, ImgOut]:
        if self.ttf_font is None:
            raise ValueError("Not Loaded yet.")
        imgs = self.rasterise(ttfont=self.ttf_font, glyph_set=self.glyph_set)
        spacing = self.get_spacing()
        normalized_imgs = self.normalize(imgs, spacing)
        self.save(imgs=normalized_imgs, save_dir=self.save_dir)

        imgs_array = {
            glyph: ImgOut(
                array=np.array(img),
                center_x=imgs[glyph].width // 2,
                height=imgs[glyph].height,
                glyph_size=imgs[glyph].size,
            )
            for glyph, img in normalized_imgs.items()
        }
        return imgs_array

    def get_spacing(
        self,
    ):
        if self.ttf_font is None:
            raise ValueError("Not Loaded yet.")
        glyph_codes = [ord(i) for i in self.glyph_set]
        cmap: table__c_m_a_p = self.ttf_font.getBestCmap()
        hmtx: table__h_m_t_x = self.ttf_font.get("hmtx", None)
        hhea: table__h_h_e_a = self.ttf_font.get("hhea", None)
        glyf: table__g_l_y_f = self.ttf_font.get("glyf", None)
        glyph_spacing: dict[str, GlyphSpacing] = {}

        for glyph_code in glyph_codes:
            glyph_name = cmap[glyph_code]
            advance, lsb = hmtx[glyph_name]
            xMin = 0
            yMin = 0
            xMax = 0
            yMax = 0
            rsb = 0
            ascent = hhea.ascent
            descent = hhea.descent
            if glyf.get(glyph_name, None) is None:
                pass
            elif glyf[glyph_name].numberOfContours > 0:
                xMin = glyf[glyph_name].xMin
                yMin = glyf[glyph_name].yMin
                xMax = glyf[glyph_name].xMax
                yMax = glyf[glyph_name].yMax
                rsb = glyf[glyph_name].xMax - advance

            glyph_spacing[chr(glyph_code)] = GlyphSpacing(
                advance=advance,
                lsb=lsb,
                rsb=rsb,
                xMin=xMin,
                yMin=yMin,
                xMax=xMax,
                yMax=yMax,
                ascent=ascent,
                descent=descent,
            )

        return glyph_spacing

    def load(self, path: str, scale: int = 1000) -> None:
        path_b = Path(path)
        self.ttf_font = ttLib.TTFont(path_b)
        scale_upem(self.ttf_font, scale)

    @classmethod
    def save(cls, imgs: dict[str, Image.Image], save_dir: str | None = "outputs/"):
        if save_dir is None:
            return
        for glyph, img in imgs.items():
            fmt = "png"
            img.save(fp=save_dir + f"{glyph}.{fmt}", format=fmt)

    @classmethod
    def rasterise(cls, ttfont: ttLib.TTFont, glyph_set) -> dict[str, Image.Image]:
        images = {}
        full_glyph_set = ttfont.getGlyphSet()
        for glyph in glyph_set:
            pen = freetypePen.FreeTypePen(glyphSet=None)
            full_glyph_set[glyph].draw(pen=pen)
            images[glyph] = pen.image()
        return images

    @staticmethod
    def grayscale_to_color(image: Image.Image, new_color=(255, 255, 255)):
        new_image = Image.new("RGBA", image.size, (255, 255, 255))
        new_image.paste(image, (0, 0), image)
        return new_image

    @classmethod
    def normalize(cls, imgs: dict[str, Image.Image], spacing: dict[str, GlyphSpacing]):
        """
        Height is  ascent + descent
        Width is width of glyph + 2x space left and right
        """
        SPACE = 400
        new_imgs = {}
        for glyph, img in imgs.items():
            img = cls.grayscale_to_color(img, (255, 255, 255))
            new_canvas = Image.new(
                mode="RGBA",
                size=(
                    img.width + SPACE * 2,
                    spacing[glyph].ascent - spacing[glyph].descent,
                ),
                color=(255, 255, 255),
            )

            new_canvas.paste(img, (SPACE, spacing[glyph].ascent - spacing[glyph].yMax))

            new_imgs[glyph] = new_canvas

        return new_imgs
