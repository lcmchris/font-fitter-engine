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

INPUT_DIR = "testing_files_img"
OUTPUT_DIR = "outputs/sdf_generator_reports/"

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
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif')
    image_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(image_extensions)]
    
    if not image_files:
        print(f"No image files found in {INPUT_DIR}")
        return
    
    print(f"Found {len(image_files)} image files to process")
    
    sdf_generator = Raster2SDFGenerator()
    
    for image_file in image_files:
        input_path = os.path.join(INPUT_DIR, image_file)
        output_filename = os.path.splitext(image_file)[0] + "-sdf.csv"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        print(f"\nProcessing: {image_file}")
        print(f"Loading image: {input_path}")
        
        try:
            pixel_array = load_image_as_array(input_path)
            print(f"Image shape: {pixel_array.shape}")
            print(f"Pixel value range: {pixel_array.min()} to {pixel_array.max()}")
            
            print("Generating SDF...")
            sdf_array = sdf_generator.generate_sdf(pixel_array)
            
            print(f"SDF shape: {sdf_array.shape}")
            print(f"SDF value range: {sdf_array.min():.3f} to {sdf_array.max():.3f}")
            print(f"SDF data type: {sdf_array.dtype}")
            
            print(f"Saving SDF to CSV: {output_path}")
            save_sdf_as_csv(sdf_array, output_path)
            print(f"Successfully processed {image_file}")
            
        except Exception as e:
            print(f"Error processing {image_file}: {str(e)}")
            continue
    
    print(f"\nBatch processing completed! Processed {len(image_files)} files.")

if __name__ == "__main__":
    main()
