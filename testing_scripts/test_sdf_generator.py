"""
Test script for Raster2SDFGenerator
Purpose: Load test image, convert to SDF, and save as CSV
"""

import numpy as np
import cv2
import csv
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.font_fitter_engine.algo_sdf.raster_2_sfd_generator import Raster2SDFGenerator

TEST_IMAGE_PATH = "../testing_files_img/test-s-512.png"
OUTPUT_CSV_PATH = "../outputs/test-s-512-sdf.csv"

def load_image_as_array(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Could not load image: {image_path}")
    return image

def save_sdf_as_csv(sdf_array, output_path):
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in sdf_array:
            writer.writerow(row)

def main():
    print(f"Loading test image: {TEST_IMAGE_PATH}")
    pixel_array = load_image_as_array(TEST_IMAGE_PATH)
    print(f"Image shape: {pixel_array.shape}")
    print(f"Pixel value range: {pixel_array.min()} to {pixel_array.max()}")
    
    print("Generating SDF...")
    sdf_generator = Raster2SDFGenerator()
    sdf_array = sdf_generator.generate_sdf(pixel_array)
    
    print(f"SDF shape: {sdf_array.shape}")
    print(f"SDF value range: {sdf_array.min():.3f} to {sdf_array.max():.3f}")
    print(f"SDF data type: {sdf_array.dtype}")
    
    print(f"Saving SDF to CSV: {OUTPUT_CSV_PATH}")
    save_sdf_as_csv(sdf_array, OUTPUT_CSV_PATH)
    
    print("Test completed successfully!")

if __name__ == "__main__":
    main()
