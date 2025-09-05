"""
SDFVisualDensityCalculator
Purpose: Calculate the visual density (darkness) of a specific area within an SDF array
Inputs: calculation_area coordinates (x1, y1, x2, y2) and sdf_array
Outputs: area_visual_density (single float value)
"""

import numpy as np
from font_fitter_engine.algo import Algo


class SDFVisualDensityAlgo(Algo):
    def __init__(self):
        pass

    def calculate(self, sdf_array: np.ndarray, calculation_area):
        x1, y1, x2, y2 = calculation_area
        zone_sdf = sdf_array[y1:y2, x1:x2]
        area_visual_density = np.sum(zone_sdf) // (
            zone_sdf.shape[0] * zone_sdf.shape[1]
        )
        return float(area_visual_density)


class SDFVisualAreaAlgo(Algo):
    def __init__(self):
        pass

    def calculate(self, sdf_array: np.ndarray, calculation_area):
        x1, y1, x2, y2 = calculation_area
        zone_sdf = sdf_array[y1:y2, x1:x2]
        area_visual_density = np.sum(zone_sdf)
        return float(area_visual_density)
