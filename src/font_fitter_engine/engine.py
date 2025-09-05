from font_fitter_engine.algo import Algo
from font_fitter_engine.algo_gaussian_blur.gaussain_blur import BlurAlgo
from font_fitter_engine.algo_sdf.sdf_visual_density_calculator import (
    SDFVisualDensityAlgo,
    SDFVisualAreaAlgo,
)
from font_fitter_engine.algo_sdf.raster_2_sfd_generator import Raster2SDFGenerator
from font_fitter_engine.loader import Loader, TTF_Loader
from font_fitter_engine.searcher import Searcher, BinomialSearcher, StepSearcher
from typing import Literal
from font_fitter_engine.strategy import BASE_SET
from pathlib import Path


class SpacingEngine:
    def __init__(
        self,
        loader,
        searcher,
    ) -> None:
        self.loader: Loader = loader
        self.searcher: Searcher = searcher

    def run(self, path):
        path_b = Path(path)
        if not path_b.is_dir():
            raise NotImplementedError("Path should be a directory")
        for file in path_b.iterdir():
            self.loader.load(path=file)
            img_out = self.loader.process()
            calculated_spaces = self.searcher.search(img_out=img_out)
            print(calculated_spaces)

    def validate(self, path: str):
        """
        Supply a path that is a directory or file.
        """
        path_b = Path(path)
        if not path_b.is_dir():
            raise NotImplementedError("Path should be a directory")

        validation_dict = {}
        for file in path_b.iterdir():
            filename = file.name
            self.loader.load(path=file)
            img_out = self.loader.process()
            spacing = self.loader.get_spacing()

            for glyph in loader.glyph_set:
                img = img_out[glyph].array
                height, width, c = img.shape
                glyph_spacing = spacing[glyph]
                lsb = glyph_spacing.lsb

                rsb = glyph_spacing.lsb
                center_x = width // 2
                sdf_array = self.searcher.transform.generate(img)
                x1 = center_x - lsb
                y1 = 0
                x2 = center_x
                y2 = height

                area = (x1, y1, x2, y2)
                for algo in self.searcher.algos:
                    calculated_darkness = algo.calculate(sdf_array, area)
                    if validation_dict.get(filename, None) is None:
                        validation_dict[filename] = {}

                    if validation_dict[filename].get(algo, None) is None:
                        validation_dict[filename][algo] = {}
                    if validation_dict[filename][algo].get(glyph, None) is None:
                        validation_dict[filename][algo][glyph] = {}

                    validation_dict[filename][algo][glyph]["calc_val"] = (
                        calculated_darkness
                    )
                    validation_dict[filename][algo][glyph]["lsb"] = lsb

        print(validation_dict)


if __name__ == "__main__":
    loader = TTF_Loader(
        glyph_set=[
            "a",
            "b",
            "c",
            "d",
            "t",
            "l",
            "i",
            "o",
            "v",
            "y",
            "x",
            "H",
            "M",
            "A",
            "B",
            "Y",
            "T",
        ],
        save_dir="outputs/",
    )
    # algo = BlurAlgo(blur_radius=20)
    algos = [SDFVisualDensityAlgo(), SDFVisualAreaAlgo()]
    searcher = StepSearcher(
        algos=algos, glyph_set=BASE_SET, step_size=2, transform=Raster2SDFGenerator()
    )
    engine = SpacingEngine(loader=loader, searcher=searcher)
    # engine.run("/home/chrisl/.repo/font-fitter-engine/testing_files/")
    engine.validate("/home/chrisl/.repo/font-fitter-engine/testing_files_fonts/")
