import typer
from font_fitter_engine.algo_sdf.sdf_visual_density_calculator import (
    SDFVisualDensityAlgo,
    SDFVisualAreaAlgo,
)
from font_fitter_engine.searcher import StepSearcher
from font_fitter_engine.loader import TTF_Loader
from font_fitter_engine.engine import SpacingEngine
from font_fitter_engine.algo_sdf.raster_2_sfd_generator import Raster2SDFGenerator
from enum import Enum
from typing_extensions import Annotated


BASE_SET: list[str] = ["a", "b", "H", "c", "y", "O"]


app = typer.Typer()


class StyleEnum(str, Enum):
    run = "run"
    validate = "validate"


@app.command("main")
def main(
    style: Annotated[StyleEnum, typer.Argument(help="run or validate")],
    font_file_path: Annotated[str, typer.Argument()],
):
    print("Starting font-fitter-engine...")

    loader = TTF_Loader(
        glyph_set=BASE_SET,
        save_dir="outputs/",
    )
    algos = [SDFVisualDensityAlgo(), SDFVisualAreaAlgo()]
    searcher = StepSearcher(
        algos=algos, glyph_set=BASE_SET, step_size=2, transform=Raster2SDFGenerator()
    )
    engine = SpacingEngine(loader=loader, searcher=searcher)
    if style == "run":
        engine.run(font_file_path)
    elif style == "validate":
        engine.validate(font_file_path)
    else:
        raise NotImplementedError(f"Style {style} not implemented")
