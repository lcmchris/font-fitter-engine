from font_fitter_engine.algo import Algo, BlurAlgo
from font_fitter_engine.loader import Loader, TTF_Raster_Loader, TTF_Paths_Loader
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

    def run(
        self,
    ):
        output = self.loader.process()
        calculated_spaces = self.searcher.search(output=output)
        print(calculated_spaces)


if __name__ == "__main__":
    loader = TTF_Raster_Loader(
        path=f"{Path(__file__).parent.parent.parent}/testing_files/SourceSerif4_18pt-Medium.ttf",
        glyph_set=BASE_SET,
        save_dir="outputs/",
    )
    algo = BlurAlgo(glyph_set=BASE_SET, blur_radius=50)
    searcher = BinomialSearcher(algo=algo, glyph_set=BASE_SET, target=100)
    engine = SpacingEngine(loader=loader, searcher=searcher)
    engine.run()
