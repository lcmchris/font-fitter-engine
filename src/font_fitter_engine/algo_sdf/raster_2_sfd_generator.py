"""
Raster2SDFGenerator
Purpose: Converts a 2D pixel array to a signed distance field (SDF) array
Inputs: 2D array of pixel values (0-255 or 0.0-1.0)
Outputs: 2D array of SDF values (raw distance values in pixels)
"""

import numpy as np
from scipy import ndimage
from scipy.spatial.distance import cdist

PIXEL_THRESHOLD_8BIT = 128
PIXEL_THRESHOLD_NORMALIZED = 0.5
DEFAULT_OUT_OF_BOUNDS_VALUE = -1.0


class Raster2SDFGenerator:
    def __init__(self):
        pass
    
    def generate_sdf(self, pixel_array):
        binary_mask = self._create_binary_mask(pixel_array)
        inside_distances = self._calculate_inside_distances(binary_mask)
        outside_distances = self._calculate_outside_distances(binary_mask)
        sdf_array = self._combine_distances(inside_distances, outside_distances, binary_mask)
        
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
    
    
    def get_sdf_at_position(self, sdf_array, x, y):
        height, width = sdf_array.shape
        if 0 <= x < width and 0 <= y < height:
            return sdf_array[y, x]
        return DEFAULT_OUT_OF_BOUNDS_VALUE
    
    def combine_sdf_arrays(self, sdf_array_1, sdf_array_2):
        return sdf_array_1 + sdf_array_2
    
    def calculate_darkness_profile(self, combined_sdf, region_bounds=None):
        if region_bounds:
            x1, y1, x2, y2 = region_bounds
            region = combined_sdf[y1:y2, x1:x2]
        else:
            region = combined_sdf
        
        positive_values = region[region > 0]
        if len(positive_values) > 0:
            return {
                'mean_darkness': np.mean(positive_values),
                'variance': np.var(positive_values),
                'max_darkness': np.max(positive_values),
                'total_darkness': np.sum(positive_values)
            }
        return {
            'mean_darkness': 0.0,
            'variance': 0.0,
            'max_darkness': 0.0,
            'total_darkness': 0.0
        }
