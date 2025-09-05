"""
Raster2SDFGenerator
Purpose: Converts a 2D pixel array to a signed distance field (SDF) array
Inputs: 2D array of pixel values (0-255 or 0.0-1.0)
Outputs: 2D array of SDF values (raw distance values in pixels)
"""

from font_fitter_engine.algo import Algo
import numpy as np
from scipy import ndimage
from scipy.spatial.distance import cdist

PIXEL_THRESHOLD_8BIT = 128
PIXEL_THRESHOLD_NORMALIZED = 0.5
DEFAULT_OUT_OF_BOUNDS_VALUE = -1.0


class Raster2SDFGenerator(Algo):
    def __init__(self):
        pass

    def generate_sdf(self, pixel_array):
        binary_mask = self._create_binary_mask(pixel_array)
        inside_distances = self._calculate_inside_distances(binary_mask)
        outside_distances = self._calculate_outside_distances(binary_mask)
        sdf_array = self._combine_distances(
            inside_distances, outside_distances, binary_mask
        )

        return sdf_array

    def _create_binary_mask(self, pixel_array):
        if pixel_array.max() > 1.0:
            threshold = PIXEL_THRESHOLD_8BIT
        else:
            threshold = PIXEL_THRESHOLD_NORMALIZED

        return pixel_array > threshold

    def _calculate_inside_distances(self, binary_mask):
        return ndimage.distance_transform_edt(binary_mask)

    def _calculate_outside_distances(self, binary_mask):
        return ndimage.distance_transform_edt(~binary_mask)

    def _combine_distances(self, inside_distances, outside_distances, binary_mask):
        sdf_array = np.zeros_like(inside_distances, dtype=np.float32)
        sdf_array[binary_mask] = inside_distances[binary_mask]
        sdf_array[~binary_mask] = -outside_distances[~binary_mask]
        return sdf_array
