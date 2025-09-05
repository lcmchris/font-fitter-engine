"""
Test script for SDFVisualDensityCalculator
Purpose: Test visual density calculation with different areas on SDF data
"""

import sys
import os
import numpy as np
import cv2
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.font_fitter_engine.algo_sdf.raster_2_sfd_generator import Raster2SDFGenerator
from src.font_fitter_engine.algo_sdf.sdf_visual_density_calculator import SDFVisualDensityCalculator

TEST_IMAGE_PATH = "testing_files_img/test-s-512.png"
OUTPUT_CSV_PATH = "outputs/test-s-512-sdf.csv"

def load_image_as_array(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Could not load image: {image_path}")
    return image

def test_density_calculations():
    print("Loading test image...")
    pixel_array = load_image_as_array(TEST_IMAGE_PATH)
    print(f"Image shape: {pixel_array.shape}")
    
    print("Generating SDF...")
    sdf_generator = Raster2SDFGenerator()
    sdf_array = sdf_generator.generate_sdf(pixel_array)
    print(f"SDF shape: {sdf_array.shape}")
    print(f"SDF value range: {sdf_array.min():.3f} to {sdf_array.max():.3f}")
    
    print("\nTesting SDFVisualDensityCalculator...")
    density_calculator = SDFVisualDensityCalculator()
    
    height, width = sdf_array.shape
    center_x, center_y = width // 2, height // 2
    
    test_areas = [
        ("Full image", (0, 0, width, height)),
        ("Left RSB small", (center_x-80, 0, center_x, height)),
        ("Left RSB medium", (center_x-130, 0, center_x, height)),
        ("Left RSB large", (center_x-150, 0, center_x, height)),
        ("Right RSB small", (center_x, 0, center_x+80, height)),
        ("Right RSB medium", (center_x, 0, center_x+130, height)),
        ("Right RSB large", (center_x, 0, center_x+150, height)),
    ]
    
    print("\nDensity calculations:")
    print("-" * 60)
    
    for area_name, (x1, y1, x2, y2) in test_areas:
        density = density_calculator.calculate_density(sdf_array, (x1, y1, x2, y2))
        area_size = (x2 - x1) * (y2 - y1)
        avg_density = density / area_size
        
        print(f"{area_name:25} | Area: {x1:3},{y1:3},{x2:3},{y2:3} | "
              f"Size: {area_size:6} | Total: {density:10.2f} | Avg: {avg_density:8.4f}")
    
    print("\nTesting with different zone sizes (center area):")
    print("-" * 60)
    
    zone_sizes = [32, 64, 128, 256]
    for size in zone_sizes:
        x1 = center_x - size // 2
        y1 = center_y - size // 2
        x2 = center_x + size // 2
        y2 = center_y + size // 2
        
        density = density_calculator.calculate_density(sdf_array, (x1, y1, x2, y2))
        area_size = size * size
        avg_density = density / area_size
        
        print(f"Center {size:3}x{size:3} | Area: {x1:3},{y1:3},{x2:3},{y2:3} | "
              f"Size: {area_size:6} | Total: {density:10.2f} | Avg: {avg_density:8.4f}")

def main():
    test_density_calculations()
    print("\nTest completed successfully!")

if __name__ == "__main__":
    main()
