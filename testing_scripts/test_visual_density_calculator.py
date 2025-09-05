"""
Test script for SDFVisualDensityCalculator
Purpose: Test visual density calculation with different areas on SDF data
"""

import sys
import os
import csv
import numpy as np
import cv2

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.font_fitter_engine.algo_sdf.raster_2_sfd_generator import Raster2SDFGenerator
from src.font_fitter_engine.algo_sdf.sdf_visual_density_calculator import (
    SDFVisualDensityAlgo,
)

INPUT_DIR = "testing_files_img"
OUTPUT_DIR = "outputs/visual_density_reports/"


def load_image_as_array(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Could not load image: {image_path}")
    return image


def ensure_output_directory():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_results_to_csv(filename, results):
    csv_path = os.path.join(
        OUTPUT_DIR, f"{os.path.splitext(filename)[0]}_density_report.csv"
    )

    with open(csv_path, "w", newline="") as csvfile:
        fieldnames = [
            "area_name",
            "coordinates",
            "area_size",
            "total_density",
            "avg_density",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow(result)

    print(f"Results saved to: {csv_path}")
    return csv_path


def process_single_image(image_path):
    filename = os.path.basename(image_path)
    print(f"\nProcessing: {filename}")
    print("=" * 50)

    pixel_array = load_image_as_array(image_path)
    print(f"Image shape: {pixel_array.shape}")

    print("Generating SDF...")
    sdf_generator = Raster2SDFGenerator()
    sdf_array = sdf_generator.generate_sdf(pixel_array)
    print(f"SDF shape: {sdf_array.shape}")
    print(f"SDF value range: {sdf_array.min():.3f} to {sdf_array.max():.3f}")

    print("\nTesting SDFVisualDensityCalculator...")
    density_calculator = SDFVisualDensityAlgo()

    height, width = sdf_array.shape
    center_x, center_y = width // 2, height // 2

    test_areas = [
        ("Full image", (0, 0, width, height)),
        ("Left RSB small", (center_x - 80, 0, center_x, height)),
        ("Left RSB medium", (center_x - 130, 0, center_x, height)),
        ("Left RSB large", (center_x - 150, 0, center_x, height)),
        ("Right RSB small", (center_x, 0, center_x + 80, height)),
        ("Right RSB medium", (center_x, 0, center_x + 130, height)),
        ("Right RSB large", (center_x, 0, center_x + 150, height)),
    ]

    print("\nDensity calculations:")
    print("-" * 60)

    results = []
    for area_name, (x1, y1, x2, y2) in test_areas:
        density = density_calculator.calculate(sdf_array, (x1, y1, x2, y2))
        area_size = (x2 - x1) * (y2 - y1)
        avg_density = density / area_size

        print(
            f"{area_name:25} | Area: {x1:3},{y1:3},{x2:3},{y2:3} | "
            f"Size: {area_size:6} | Total: {density:10.2f} | Avg: {avg_density:8.4f}"
        )

        results.append(
            {
                "area_name": area_name,
                "coordinates": f"{x1},{y1},{x2},{y2}",
                "area_size": area_size,
                "total_density": density,
                "avg_density": avg_density,
            }
        )

    print("\nTesting with different zone sizes (center area):")
    print("-" * 60)

    zone_sizes = [32, 64, 128, 256]
    for size in zone_sizes:
        x1 = center_x - size // 2
        y1 = center_y - size // 2
        x2 = center_x + size // 2
        y2 = center_y + size // 2

        density = density_calculator.calculate(sdf_array, (x1, y1, x2, y2))
        area_size = size * size
        avg_density = density / area_size

        print(
            f"Center {size:3}x{size:3} | Area: {x1:3},{y1:3},{x2:3},{y2:3} | "
            f"Size: {area_size:6} | Total: {density:10.2f} | Avg: {avg_density:8.4f}"
        )

        results.append(
            {
                "area_name": f"Center {size}x{size}",
                "coordinates": f"{x1},{y1},{x2},{y2}",
                "area_size": area_size,
                "total_density": density,
                "avg_density": avg_density,
            }
        )

    csv_path = save_results_to_csv(filename, results)
    return results, csv_path


def process_directory():
    ensure_output_directory()

    if not os.path.exists(INPUT_DIR):
        raise ValueError(f"Input directory does not exist: {INPUT_DIR}")

    png_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".png")]

    if not png_files:
        print(f"No PNG files found in {INPUT_DIR}")
        return

    print(f"Found {len(png_files)} PNG files to process")

    all_results = {}

    csv_files_created = []

    for png_file in sorted(png_files):
        image_path = os.path.join(INPUT_DIR, png_file)
        try:
            results, csv_path = process_single_image(image_path)
            all_results[png_file] = results
            csv_files_created.append(csv_path)
        except Exception as e:
            print(f"Error processing {png_file}: {e}")
            continue

    print(f"\nProcessed {len(all_results)} files successfully")
    print(f"Created {len(csv_files_created)} CSV report files in {OUTPUT_DIR}")
    return all_results, csv_files_created


def main():
    process_directory()
    print("\nTest completed successfully!")


if __name__ == "__main__":
    main()
