"""
SDF Heatmap Visualizer
Purpose: Create heatmap visualizations of SDF data
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

DEFAULT_FIGURE_SIZE = (12, 10)
DEFAULT_DPI = 300
ZERO_THRESHOLD = 0.5
CONTOUR_LEVELS = 20
FILLED_CONTOUR_LEVELS = 50
DEFAULT_INPUT_CSV = "../outputs/test-s-512-sdf.csv"
DEFAULT_HEATMAP_OUTPUT = "../outputs/test-s-512-sdf-heatmap.png"
DEFAULT_CONTOUR_OUTPUT = "../outputs/test-s-512-sdf-contour.png"


def visualize_sdf_heatmap(csv_file, output_image=None):
    sdf_array = np.loadtxt(csv_file, delimiter=",")

    plt.figure(figsize=DEFAULT_FIGURE_SIZE)

    # Create heatmap with custom colormap
    im = plt.imshow(sdf_array, cmap="RdBu_r", aspect="equal")

    # Add colorbar
    cbar = plt.colorbar(im, label="SDF Value (pixels)")

    # Customize plot
    plt.title("Signed Distance Field Heatmap", fontsize=16)
    plt.xlabel("X Position (pixels)", fontsize=12)
    plt.ylabel("Y Position (pixels)", fontsize=12)

    # Add grid for better readability
    plt.grid(True, alpha=0.3)

    # Show statistics
    print(f"SDF Statistics:")
    print(f"  Shape: {sdf_array.shape}")
    print(f"  Min value: {sdf_array.min():.2f}")
    print(f"  Max value: {sdf_array.max():.2f}")
    print(f"  Mean value: {sdf_array.mean():.2f}")
    print(f"  Zero crossings: {np.sum(np.abs(sdf_array) < ZERO_THRESHOLD)}")

    if output_image:
        plt.savefig(output_image, dpi=DEFAULT_DPI, bbox_inches="tight")
        print(f"Heatmap saved to: {output_image}")

    plt.show()


def visualize_sdf_contours(csv_file, output_image=None):
    sdf_array = np.loadtxt(csv_file, delimiter=",")

    plt.figure(figsize=DEFAULT_FIGURE_SIZE)

    # Create contour plot
    contours = plt.contour(
        sdf_array, levels=CONTOUR_LEVELS, colors="black", alpha=0.6, linewidths=0.5
    )
    plt.clabel(contours, inline=True, fontsize=8)

    # Add filled contours
    plt.contourf(sdf_array, levels=FILLED_CONTOUR_LEVELS, cmap="RdBu_r", alpha=0.8)

    plt.colorbar(label="SDF Value (pixels)")
    plt.title("SDF Contour Plot", fontsize=16)
    plt.xlabel("X Position (pixels)", fontsize=12)
    plt.ylabel("Y Position (pixels)", fontsize=12)

    if output_image:
        plt.savefig(output_image, dpi=DEFAULT_DPI, bbox_inches="tight")
        print(f"Contour plot saved to: {output_image}")

    plt.show()


if __name__ == "__main__":
    # Visualize the test SDF data
    visualize_sdf_heatmap(DEFAULT_INPUT_CSV, DEFAULT_HEATMAP_OUTPUT)
    visualize_sdf_contours(DEFAULT_INPUT_CSV, DEFAULT_CONTOUR_OUTPUT)
