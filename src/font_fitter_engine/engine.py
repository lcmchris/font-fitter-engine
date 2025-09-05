from font_fitter_engine.algo import Algo
from font_fitter_engine.algo_gaussian_blur.gaussain_blur import BlurAlgo
from font_fitter_engine.algo_sdf.sdf_visual_density_calculator import (
    SDFVisualDensityAlgo,
)
from font_fitter_engine.algo_sdf.raster_2_sfd_generator import Raster2SDFGenerator
from font_fitter_engine.loader import Loader, TTF_Loader
from font_fitter_engine.searcher import Searcher, BinomialSearcher
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
        self.loader
        output = self.loader.process()
        calculated_spaces = self.searcher.search(output=output)
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
            self.loader.load(path=file.as_posix())
            spacing = self.loader.get_spacing()
            imgs = self.loader.process()

            for glyph in loader.glyph_set:
                img = imgs[glyph]
                height, width = img.shape
                center_x, center_y = width // 2, height // 2

                test_areas = [
                    # ("Full image", (0, 0, width, height)),
                    ("Left RSB small", (center_x - 80, 0, center_x, height)),
                    # ("Left RSB medium", (center_x - 130, 0, center_x, height)),
                    # ("Left RSB large", (center_x - 150, 0, center_x, height)),
                    # ("Right RSB small", (center_x, 0, center_x + 80, height)),
                    # ("Right RSB medium", (center_x, 0, center_x + 130, height)),
                    # ("Right RSB large", (center_x, 0, center_x + 150, height)),
                ]
                for test_area in test_areas:
                    calculated_darkness = self.searcher.algo.calculate(
                        img=imgs[glyph], calculation_area=test_area[1]
                    )
                    if validation_dict.get(filename, None) is None:
                        validation_dict[filename] = {}
                    if validation_dict.get(glyph, None) is None:
                        validation_dict[filename][glyph] = {}

                    validation_dict[filename][glyph][test_area[0]] = calculated_darkness

        print(validation_dict)


if __name__ == "__main__":
    loader = TTF_Loader(
        glyph_set=BASE_SET,
        save_dir="outputs/",
    )
    # algo = BlurAlgo(blur_radius=20)
    algo = SDFVisualDensityAlgo()
    searcher = BinomialSearcher(algo=algo, glyph_set=BASE_SET, target=100)
    engine = SpacingEngine(loader=loader, searcher=searcher)
    engine.validate("/home/chrisl/.repo/font-fitter-engine/testing_files/")
