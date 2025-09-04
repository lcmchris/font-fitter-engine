"""
SDFGradientAnalyser
Purpose: Analyzes gradient changes across a measured zone in an SDF array
Inputs: SDF array and measured_zone coordinates (x1, y1, x2, y2)
Outputs: Statistical summary dictionary with gradient metrics
"""

import numpy as np
from scipy import ndimage

SMOOTH_THRESHOLD = 0.5
ROUGH_THRESHOLD = 2.0


class SDFGradientAnalyser:
    def __init__(self):
        pass
    
    def analyze_gradient(self, sdf_array, measured_zone):
        x1, y1, x2, y2 = measured_zone
        zone_sdf = sdf_array[y1:y2, x1:x2]
        
        gradient_x, gradient_y = self._calculate_gradients(zone_sdf)
        gradient_magnitude = self._calculate_gradient_magnitude(gradient_x, gradient_y)
        
        return self._generate_statistical_summary(gradient_magnitude)
    
    def _calculate_gradients(self, zone_sdf):
        gradient_x = ndimage.sobel(zone_sdf, axis=1)
        gradient_y = ndimage.sobel(zone_sdf, axis=0)
        return gradient_x, gradient_y
    
    def _calculate_gradient_magnitude(self, gradient_x, gradient_y):
        return np.sqrt(gradient_x**2 + gradient_y**2)
    
    def _generate_statistical_summary(self, gradient_magnitude):
        mean_gradient = np.mean(gradient_magnitude)
        max_gradient = np.max(gradient_magnitude)
        gradient_variance = np.var(gradient_magnitude)
        
        smooth_regions = np.sum(gradient_magnitude < SMOOTH_THRESHOLD)
        rough_regions = np.sum(gradient_magnitude > ROUGH_THRESHOLD)
        total_pixels = gradient_magnitude.size
        
        smoothness_ratio = smooth_regions / total_pixels
        roughness_ratio = rough_regions / total_pixels
        
        return {
            'mean_gradient': float(mean_gradient),
            'max_gradient': float(max_gradient),
            'gradient_variance': float(gradient_variance),
            'smooth_regions': int(smooth_regions),
            'rough_regions': int(rough_regions),
            'smoothness_ratio': float(smoothness_ratio),
            'roughness_ratio': float(roughness_ratio),
            'total_pixels': int(total_pixels)
        }
    
    def analyze_directional_gradients(self, sdf_array, measured_zone):
        x1, y1, x2, y2 = measured_zone
        zone_sdf = sdf_array[y1:y2, x1:x2]
        
        gradient_x, gradient_y = self._calculate_gradients(zone_sdf)
        
        return {
            'horizontal_gradient': {
                'mean': float(np.mean(np.abs(gradient_x))),
                'variance': float(np.var(gradient_x)),
                'max': float(np.max(np.abs(gradient_x)))
            },
            'vertical_gradient': {
                'mean': float(np.mean(np.abs(gradient_y))),
                'variance': float(np.var(gradient_y)),
                'max': float(np.max(np.abs(gradient_y)))
            }
        }
    
    def get_gradient_profile(self, sdf_array, measured_zone, axis='horizontal'):
        x1, y1, x2, y2 = measured_zone
        zone_sdf = sdf_array[y1:y2, x1:x2]
        
        if axis == 'horizontal':
            profile = np.mean(zone_sdf, axis=0)
        else:
            profile = np.mean(zone_sdf, axis=1)
        
        return profile.tolist()
    
    def calculate_consistency_score(self, gradient_stats):
        variance_penalty = gradient_stats['gradient_variance'] * 10
        roughness_penalty = gradient_stats['roughness_ratio'] * 5
        smoothness_bonus = gradient_stats['smoothness_ratio'] * 2
        
        consistency_score = 100 - variance_penalty - roughness_penalty + smoothness_bonus
        return max(0, min(100, consistency_score))
