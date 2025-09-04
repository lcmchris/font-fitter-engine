from font_fitter_engine.algo import Algo, BlurAlgo
from font_fitter_engine.loader import Loader, TTF_Raster_Loader
from typing import Literal
from font_fitter_engine.strategy import BASE_SET
from pathlib import Path


class SpacingEngine:
    def __init__(self, loader, algo, strategy=Literal["singular"]) -> None:
        self.loader: Loader = loader
        self.algo: Algo = algo

    def run(
        self,
    ):
        output = self.loader.process()
        calculated_spaces = self.algo.calculate_spacing(output=output)
        pass


if __name__ == "__main__":
    loader = TTF_Raster_Loader(
        path=f"{Path(__file__).parent}/examples/BigshotOne-Regular.ttf",
        glyph_set=BASE_SET,
        save_dir="outputs/",
    )
    algo = BlurAlgo(glyph_set=BASE_SET)
    engine = SpacingEngine(algo=algo, loader=loader)
    engine.run()
