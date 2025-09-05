"""
SFDTargetSpaceSearcher
Purpose: Find optimal width of calculation areas that achieve target visual density
Inputs: sdf_array, center_x, height, target_density, step_size, max_width
Outputs: optimal_area_left, optimal_area_right, left_density_diff, right_density_diff
"""

import numpy as np

DEFAULT_STEP_SIZE = 2


class SFDTargetSpaceSearcher:
    def __init__(self, step_size=DEFAULT_STEP_SIZE):
        self.step_size = step_size

    def search_optimal_areas(self, sdf_array, center_x, height, target_density):
        left_result = self._search_left_side(
            sdf_array, center_x, height, target_density
        )
        right_result = self._search_right_side(
            sdf_array, center_x, height, target_density
        )

        return {
            "optimal_area_left": left_result["area"],
            "optimal_area_right": right_result["area"],
            "left_density_diff": left_result["density_diff"],
            "right_density_diff": right_result["density_diff"],
            "left_achieved_density": left_result["achieved_density"],
            "right_achieved_density": right_result["achieved_density"],
            "left_step_densities": left_result["step_densities"],
            "right_step_densities": right_result["step_densities"],
        }

    def _search_left_side(self, sdf_array, center_x, height, target_density):
        step_densities = []

        width = self.step_size
        while center_x - width >= 0:
            x1 = center_x - width
            y1 = 0
            x2 = center_x
            y2 = height

            area = (x1, y1, x2, y2)
            achieved_density = self._calculate_density(sdf_array, area)
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

    def _search_right_side(self, sdf_array, center_x, height, target_density):
        step_densities = []

        width = self.step_size
        while center_x + width < sdf_array.shape[1]:
            x1 = center_x
            y1 = 0
            x2 = center_x + width
            y2 = height

            area = (x1, y1, x2, y2)
            achieved_density = self._calculate_density(sdf_array, area)
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

    # def _calculate_density(self, sdf_array, calculation_area):
    #     x1, y1, x2, y2 = calculation_area
    #     zone_sdf = sdf_array[y1:y2, x1:x2]
    #     area_visual_density = np.sum(zone_sdf)
    #     return float(area_visual_density)
