"""
SDFVisualDensityCalculator
Purpose: Calculate the visual density (darkness) of a specific area within an SDF array
Inputs: calculation_area coordinates (x1, y1, x2, y2) and sdf_array
Outputs: area_visual_density (single float value)
"""

import numpy as np
from font_fitter_engine.algo import Algo
from .raster_2_sfd_generator import Raster2SDFGenerator


class SDFVisualDensityAlgo(Algo):
    def __init__(
        self,
    ):
        self.generator = Raster2SDFGenerator()
        return super().__init__()

    def calculate(self, img, calculation_area):
        sdf_array = self.generator.generate_sdf(img)
        x1, y1, x2, y2 = calculation_area

        zone_sdf = sdf_array[y1:y2, x1:x2]
        area_visual_density = np.sum(zone_sdf)
        return float(area_visual_density)
