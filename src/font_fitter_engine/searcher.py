from font_fitter_engine.algo import Algo
from font_fitter_engine.loader import ImgOut
from font_fitter_engine.algo_sdf.raster_2_sfd_generator import Transform
import numpy as np


class Searcher:
    """How do we search?"""

    def __init__(
        self, glyph_set: list[str], algos: list[Algo], transform: Transform
    ) -> None:
        self.glyph_set = glyph_set
        self.algos = algos
        self.transform = transform
        pass

    def search(self, img_out) -> dict[str, int]:
        raise NotImplementedError


class StepSearcher(Searcher):
    def __init__(
        self,
        glyph_set: list[str],
        algos: list[Algo],
        transform: Transform,
        target_densities: list[int] = [
            100,
            200,
            300,
        ],
        step_size=2,
    ) -> None:
        self.target_densities = target_densities
        self.step_size = 2

        super().__init__(glyph_set, algos=algos, transform=transform)

    def search(self, img_out: dict[str, ImgOut]):
        output = {}
        for algo in self.algos:
            for glyph in self.glyph_set:
                for target_density in self.target_densities:
                    img_out_glyph = img_out[glyph]

                    sdf_array = self.transform.generate(img_out_glyph.array)

                    height, width, c = img_out_glyph.array.shape

                    left_result = self._search_left_side(
                        sdf_array=sdf_array,
                        center_x=width // 2,
                        height=height,
                        target_density=target_density,
                        algo=algo,
                    )
                    right_result = self._search_right_side(
                        sdf_array=sdf_array,
                        center_x=width // 2,
                        height=height,
                        target_density=target_density,
                        algo=algo,
                    )
                    if output.get(algo, None) is None:
                        output[algo] = {}

                    if output[algo].get(glyph, None) is None:
                        output[algo][glyph] = {}

                    lsb = (
                        left_result["area"][2]
                        - left_result["area"][0]
                        - img_out_glyph.glyph_size[0]
                    )
                    output[algo][glyph][target_density] = {
                        "lsb": lsb,
                        "optimal_area_left": left_result["area"],
                        "optimal_area_right": right_result["area"],
                        "left_density_diff": left_result["density_diff"],
                        "right_density_diff": right_result["density_diff"],
                        "left_achieved_density": left_result["achieved_density"],
                        "right_achieved_density": right_result["achieved_density"],
                        "left_step_densities": left_result["step_densities"],
                        "right_step_densities": right_result["step_densities"],
                    }
        print(output)
        return output

    def _search_left_side(
        self, sdf_array, center_x, height, target_density, algo: Algo
    ):
        step_densities = []

        width = self.step_size
        while center_x - width >= 0:
            x1 = center_x - width
            y1 = 0
            x2 = center_x
            y2 = height

            area = (x1, y1, x2, y2)
            achieved_density = algo.calculate(sdf_array, area)
            density_diff = abs(achieved_density - target_density)

            step_densities.append(
                {
                    "width": width,
                    "area": area,
                    "density": achieved_density,
                    "density_diff": density_diff,
                }
            )

            width += self.step_size

        best_step = min(step_densities, key=lambda x: x["density_diff"])

        return {
            "area": best_step["area"],
            "density_diff": best_step["density_diff"],
            "achieved_density": best_step["density"],
            "step_densities": step_densities,
        }

    def _search_right_side(
        self, sdf_array, center_x, height, target_density, algo: Algo
    ):
        step_densities = []

        width = self.step_size
        while center_x + width < sdf_array.shape[1]:
            x1 = center_x
            y1 = 0
            x2 = center_x + width
            y2 = height

            area = (x1, y1, x2, y2)
            achieved_density = algo.calculate(sdf_array, area)
            density_diff = abs(achieved_density - target_density)

            step_densities.append(
                {
                    "width": width,
                    "area": area,
                    "density": achieved_density,
                    "density_diff": density_diff,
                }
            )

            width += self.step_size

        best_step = min(step_densities, key=lambda x: x["density_diff"])

        return {
            "area": best_step["area"],
            "density_diff": best_step["density_diff"],
            "achieved_density": best_step["density"],
            "step_densities": step_densities,
        }

    def _calculate_density(self, sdf_array: np.ndarray, calculation_area):
        x1, y1, x2, y2 = calculation_area
        zone_sdf = sdf_array[y1:y2, x1:x2]
        area_visual_density = np.sum(zone_sdf) // (
            zone_sdf.shape[0] * zone_sdf.shape[1]
        )
        return float(area_visual_density)


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
        for glyph in self.glyph_set:
            idx = 0
            calc_val = -100
            max_g = self.max_gap
            min_g = self.min_gap

            max_val = calc_val = self.algo.calculate(glyph, output, max_g)
            min_val = calc_val = self.algo.calculate(glyph, output, min_g)
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

                calc_val = self.algo.calculate(glyph, output, mid)

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

            final_result[glyph] = mid
        return final_result
