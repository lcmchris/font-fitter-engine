from multiprocessing import Pool
from font_fitter_engine.algo import Algo


class Searcher:
    """How do we search?"""

    def __init__(self, glyph_set: list[tuple[str, str]], algo: Algo) -> None:
        self.glyph_set = glyph_set
        self.algo = algo
        pass

    def search(self, output) -> dict[tuple[str, str], int]:
        raise NotImplementedError


class BinomialSearcher(Searcher):
    def __init__(
        self,
        glyph_set,
        algo,
        min_gap: int = 0,
        max_gap: int = 200,
        limit: int = 40,
        target: int = 100,
    ) -> None:
        self.min_gap = min_gap
        self.max_gap = max_gap
        self.limit = limit
        self.target = target
        self.boundary = 10

        super().__init__(glyph_set=glyph_set, algo=algo)

    def search(self, output):
        """create search plan"""
        final_result = {}
        for pair in self.glyph_set:
            idx = 0
            calc_val = -100
            max_g = self.max_gap
            min_g = self.min_gap

            max_val = calc_val = self.algo.calculate(pair, output, max_g)
            min_val = calc_val = self.algo.calculate(pair, output, min_g)
            direction = 1 if max_val - min_val > 0 else -1
            while True:
                idx += 1
                mid = (max_g + min_g) // 2
                if (
                    idx > self.limit
                    or (
                        calc_val < self.target + self.boundary
                        and calc_val > self.target - self.boundary
                    )
                    or mid == min_g
                    or mid == max_g
                ):
                    break

                calc_val = self.algo.calculate(pair, output, mid)

                if calc_val > self.target + self.boundary:
                    if direction:
                        min_g = mid
                    else:
                        max_g = mid
                elif calc_val < self.target - self.boundary:
                    if direction:
                        max_g = mid
                    else:
                        min_g = mid

            final_result[pair] = mid
        return final_result
