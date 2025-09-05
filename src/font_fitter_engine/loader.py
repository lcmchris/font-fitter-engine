from fontTools import ttLib
from pathlib import Path
from fontTools.pens import freetypePen, svgPathPen
from fontTools.ttLib.tables._c_m_a_p import table__c_m_a_p
from fontTools.ttLib.tables._h_m_t_x import table__h_m_t_x
from fontTools.ttLib.tables._g_l_y_f import table__g_l_y_f
from PIL.Image import Image


class Loader:
    def __init__(
        self,
        glyph_set: list[str],
        save_dir: str | None = None,
    ) -> None:
        self.glyph_set = glyph_set
        self.save_dir = save_dir
        pass

    def process(self):
        raise NotImplementedError

    def load(self, path: str):
        raise NotImplementedError

    def get_spacing(self) -> dict[str, dict[str, int]]:
        raise NotImplementedError


class TTF_Raster_Loader(Loader):
    def __init__(self, glyph_set, save_dir) -> None:
        self.ttf_font = None
        super().__init__(glyph_set=glyph_set, save_dir=save_dir)

    def process(
        self,
    ) -> dict[str, Image]:
        if self.ttf_font is None:
            raise ValueError("Not Loaded yet.")
        imgs = self.rasterise(ttfont=self.ttf_font, glyph_set=self.glyph_set)
        self.save(imgs=imgs, save_dir=self.save_dir)

        return imgs

    def get_spacing(
        self,
    ):
        if self.ttf_font is None:
            raise ValueError("Not Loaded yet.")
        glyph_codes = [ord(i) for i in self.glyph_set]
        cmap: table__c_m_a_p = self.ttf_font.getBestCmap()
        hmtx: table__h_m_t_x = self.ttf_font.get("hmtx", None)
        glyf: table__g_l_y_f = self.ttf_font.get("glyf", None)

        glyph_spacing = {}
        for glyph_code in glyph_codes:
            glyph_name = cmap[glyph_code]
            advance, lsb = hmtx[glyph_name]
            xMin = 0
            yMin = 0
            xMax = 0
            yMax = 0
            rsb = 0
            if glyf.get(glyph_name, None) is None:
                pass
            elif glyf[glyph_name].numberOfContours > 0:
                xMin = glyf[glyph_name].xMin
                yMin = glyf[glyph_name].yMin
                xMax = glyf[glyph_name].xMax
                yMax = glyf[glyph_name].yMax
                rsb = glyf[glyph_name].xMax - advance

            glyph_spacing[chr(glyph_code)] = {
                "advance": advance,
                "lsb": lsb,
                "rsb": rsb,
                "xMin": xMin,
                "yMin": yMin,
                "xMax": xMax,
                "yMax": yMax,
            }
        return glyph_spacing

    def load(self, path: str):
        path_b = Path(path)
        self.ttf_font = ttLib.TTFont(path_b)

    @classmethod
    def save(cls, imgs: dict[str, Image], save_dir: str | None = "outputs/"):
        if save_dir is None:
            return
        for glyph, img in imgs.items():
            fmt = "png"
            img.save(fp=save_dir + f"{glyph}.{fmt}", format=fmt)

    @classmethod
    def rasterise(
        cls, ttfont: ttLib.TTFont, glyph_set, asarray: bool = False
    ) -> dict[str, Image]:
        images = {}
        full_glyph_set = ttfont.getGlyphSet()
        for glyph in glyph_set:
            pen = freetypePen.FreeTypePen(glyphSet=None)
            full_glyph_set[glyph].draw(pen=pen)

            if asarray:
                images[glyph] = pen.array()
            else:
                images[glyph] = pen.image()
        return images
