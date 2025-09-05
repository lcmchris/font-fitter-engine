"""
Test script for SFDTargetSpaceSearcher
Purpose: Orchestrate all SDF components and generate CSV reports of search progress
"""

import sys
import os
import csv
import numpy as np
import cv2
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.font_fitter_engine.algo_sdf.raster_2_sfd_generator import Raster2SDFGenerator
from src.font_fitter_engine.algo_sdf.sdf_visual_density_calculator import SDFVisualDensityCalculator
from src.font_fitter_engine.algo_sdf.sdf_target_space_searcher import SFDTargetSpaceSearcher

TESTING_FILES_DIR = "testing_files_img"
OUTPUTS_DIR = "outputs/search_repots/"
TARGET_DENSITIES = [200000, 300000, 800000, 900000]
DEFAULT_STEP_SIZE = 2

def load_image_as_array(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Could not load image: {image_path}")
    return image

def get_test_images():
    test_images = []
    for filename in os.listdir(TESTING_FILES_DIR):
        if filename.endswith('.png'):
            name_without_ext = os.path.splitext(filename)[0]
            test_images.append({
                'filename': filename,
                'name': name_without_ext,
                'path': os.path.join(TESTING_FILES_DIR, filename)
            })
    return test_images

def save_search_results_to_csv(results, output_path, target_density):
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Side', 'Step', 'Search Area x_min', 'Search Area x_max', 'Area Density', 'Difference from target', 'Selected'])
        
        left_steps = results['left_step_densities']
        right_steps = results['right_step_densities']
        
        best_left_diff = results['left_density_diff']
        best_right_diff = results['right_density_diff']
        
        for i, step in enumerate(left_steps):
            is_selected = step['density_diff'] == best_left_diff
            writer.writerow([
                'Left',
                i + 1,
                step['area'][0],
                step['area'][2],
                step['density'],
                step['density_diff'],
                is_selected
            ])
        
        for i, step in enumerate(right_steps):
            is_selected = step['density_diff'] == best_right_diff
            writer.writerow([
                'Right',
                i + 1,
                step['area'][0],
                step['area'][2],
                step['density'],
                step['density_diff'],
                is_selected
            ])

def test_single_image(image_info, target_density):
    print(f"Processing {image_info['name']} with target density {target_density}")
    
    pixel_array = load_image_as_array(image_info['path'])
    height, width = pixel_array.shape
    center_x = width // 2
    
    sdf_generator = Raster2SDFGenerator()
    sdf_array = sdf_generator.generate_sdf(pixel_array)
    
    searcher = SFDTargetSpaceSearcher(step_size=DEFAULT_STEP_SIZE)
    results = searcher.search_optimal_areas(sdf_array, center_x, height, target_density)
    
    output_filename = f"{image_info['name']}-{target_density}.csv"
    output_path = os.path.join(OUTPUTS_DIR, output_filename)
    save_search_results_to_csv(results, output_path, target_density)
    
    print(f"Results saved to: {output_path}")
    print(f"Left optimal area: {results['optimal_area_left']} (density: {results['left_achieved_density']:.2f}, diff: {results['left_density_diff']:.2f})")
    print(f"Right optimal area: {results['optimal_area_right']} (density: {results['right_achieved_density']:.2f}, diff: {results['right_density_diff']:.2f})")
    print()

def main():
    if not os.path.exists(OUTPUTS_DIR):
        os.makedirs(OUTPUTS_DIR)
    
    test_images = get_test_images()
    
    if not test_images:
        print(f"No PNG images found in {TESTING_FILES_DIR}")
        return
    
    print(f"Found {len(test_images)} test images")
    print(f"Testing with target densities: {TARGET_DENSITIES}")
    print()
    
    for image_info in test_images:
        for target_density in TARGET_DENSITIES:
            try:
                test_single_image(image_info, target_density)
            except Exception as e:
                print(f"Error processing {image_info['name']} with target density {target_density}: {e}")
                print()
    
    print("All tests completed!")

if __name__ == "__main__":
    main()
