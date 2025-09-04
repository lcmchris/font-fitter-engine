from font_fitter_engine.algo import Algo, BlurAlgo
from font_fitter_engine.loader import Loader,TTFLoader
from typing import Literal

class SpacingEngine():
    def __init__(self, loader, algo, strategy=Literal['singular']) -> None:
        
        self.loader :Loader = loader
        self.algo: Algo  = algo

    
    def run():
        pass
        



if __name__ == '__main__':
    loader = TTFLoader()
    algo = BlurAlgo()
    
    engine = SpacingEngine(
        algo=algo,
        loader=loader
    )