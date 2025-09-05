from font_fitter_engine.algo import Algo, BlurAlgo
from font_fitter_engine.algo_sdf.raster_2_sfd_generator import Raster2SDFGenerator
from font_fitter_engine.loader import Loader, TTF_Raster_Loader
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
            output = self.loader.load(path=path)
            spacing = self.loader.get_spacing()
            imgs = self.loader.process()

            validation_dict = {}
            for glyph in loader.glyph_set:
                for direction in ["lsb", "rsb"]:
                    calculated_darkness = self.searcher.algo.calculate(
                        glyph=glyph,
                        imgs=imgs,
                        spacing=spacing[glyph][direction],
                        direction=direction,
                    )

                    if validation_dict.get(glyph, None) is None:
                        validation_dict[glyph] = {}
                    validation_dict[glyph][direction] = calculated_darkness

            print(validation_dict)

        else:
            raise NotImplementedError("Not yet!")
            ##todo


if __name__ == "__main__":
    loader = TTF_Raster_Loader(
        glyph_set=BASE_SET,
        save_dir="outputs/",
    )
    algo = BlurAlgo(glyph_set=BASE_SET, blur_radius=20)
    searcher = BinomialSearcher(algo=algo, glyph_set=BASE_SET, target=100)
    engine = SpacingEngine(loader=loader, searcher=searcher)
    engine.validate(
        "/home/chrisl/.repo/font-fitter-engine/testing_files/Actor-Regular.ttf"
    )
