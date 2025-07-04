import numpy as np
import random
import math
from shapely import wkt
from shapely.ops import transform
from pyproj import Transformer
import matplotlib.pyplot as plt
from matplotlib import ticker
from tqdm import tqdm

random.seed(100)

def genRaster(INPUT_BBOX, spatial_resolution=None):
    """
    Generate simulated raster within the INPUT_BBOX at a given spatial resolution.
    """
    min_lon, min_lat, max_lon, max_lat = INPUT_BBOX
    center_lon = (min_lon + max_lon) / 2
    center_lat = (min_lat + max_lat) / 2

    utm_zone = int((center_lon + 180) / 6) + 1
    proj_string = f"+proj=utm +zone={utm_zone} +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
    transformer = Transformer.from_crs("EPSG:4326", proj_string, always_xy=True)

    # Convert lat/lon bbox to UTM meters
    (min_x, min_y) = transformer.transform(min_lon, min_lat)
    (max_x, max_y) = transformer.transform(max_lon, max_lat)

    width_m = max_x - min_x
    height_m = max_y - min_y

    cols = int(width_m // spatial_resolution)
    rows = int(height_m // spatial_resolution)

    # Generate a raster with values based on sin/cos pattern for illustration
    # x = np.linspace(0, np.pi * 1, cols)
    # y = np.linspace(0, np.pi * 1, rows)
    # xv, yv = np.meshgrid(x, y)
    # raster = np.sin(xv) * np.cos(yv)

    # Generate arbitrary raster values: random noise + soft gradient for illustration
    gradient = np.linspace(0.2, 0.8, cols)
    raster = np.tile(gradient, (rows, 1))

    # Add smoothed noise
    noise = np.random.rand(rows, cols) * 0.3
    raster += noise

    # Normalize to 0–1
    raster = (raster - raster.min()) / (raster.max() - raster.min())

    return raster

def plotBoundingBox(ax, bbox, color='red', linestyle='--', linewidth=2):
    """Draws a bounding box (min_lon, min_lat, max_lon, max_lat) on ax."""
    min_lon, min_lat, max_lon, max_lat = bbox
    x = [min_lon, max_lon, max_lon, min_lon, min_lon]
    y = [min_lat, min_lat, max_lat, max_lat, min_lat]
    ax.plot(x, y, color=color, linestyle=linestyle, linewidth=linewidth)


# def vizRaster(rasters, INPUT_BBOX=None, titles=None, iteration=0):
#     """
#     Visualize multiple raster arrays in subplots within a single figure.
#     """
#     n = len(rasters)
#     cols = min(5, n)
#     rows = math.ceil(n / cols)

#     fig, axes = plt.subplots(rows, cols, figsize=(5*cols, 4*rows))

#     # if n > 1:
#     #     axes = axes.flatten()
#     # else:
#     #     axes = [axes]

#     min_lon, min_lat, max_lon, max_lat = INPUT_BBOX
#     for i, raster in enumerate(rasters):
#         ax = axes[i]

#         # Get lat/lon extent for georeferencing the raster
#         # height, width = raster.shape
#         extent = [min_lon, max_lon, min_lat, max_lat]

#         im = ax.imshow(raster, cmap='nipy_spectral_r', extent=extent, origin='lower', aspect='auto')
#         plotBoundingBox(ax, INPUT_BBOX, color='red', linestyle='--', linewidth=2)
#         ax.set_title(titles[i] if titles else f"Raster {i}", fontsize=15)
#         ax.set_xlabel("Longitude", fontsize=9)
#         ax.set_ylabel("Latitude", fontsize=9)
#         ax.tick_params(labelsize=10)

#     for j in range(len(rasters), len(axes)):
#         axes[j].axis('off')

#     # fig.suptitle(f'Geo-referenced Rasters (v{iteration})', fontsize=16, fontweight='bold')
#     plt.tight_layout(rect=[0, 0.03, 1, 0.95])
#     plt.show()

def vizRaster(rasters, INPUT_BBOX=None, titles=None, iteration=0):
    n = len(rasters)
    cols = min(5, n)
    rows = math.ceil(n / cols)

    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))
    axes = np.array(axes).reshape(-1)  # Flatten in case of single row/col

    min_lon, min_lat, max_lon, max_lat = INPUT_BBOX
    padding_x = (max_lon - min_lon) * 0.1
    padding_y = (max_lat - min_lat) * 0.1

    view_min_lon = min_lon - padding_x
    view_max_lon = max_lon + padding_x
    view_min_lat = min_lat - padding_y
    view_max_lat = max_lat + padding_y

    for i, raster in enumerate(rasters):
        ax = axes[i]

        # Display raster image in grayscale
        ax.imshow(raster, cmap='gist_gray', extent=[min_lon, max_lon, min_lat, max_lat], # gist_gray, jet
                  origin='lower', aspect='auto')

        # Set axis limits with padding (for visual gap)
        ax.set_xlim(view_min_lon, view_max_lon)
        ax.set_ylim(view_min_lat, view_max_lat)

        # Draw the INPUT_BBOX in red dashed
        plotBoundingBox(ax, INPUT_BBOX, color='red', linestyle='--', linewidth=3)

        # Set axis ticks to match image style
        ax.set_xticks(np.linspace(view_min_lon, view_max_lon, 4))
        ax.set_yticks(np.linspace(view_min_lat, view_max_lat, 5))
        ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.2f}"))
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.2f}"))

        # Style
        ax.set_title(titles[i] if titles else f"Raster {i}", fontsize=20, fontweight='bold')
        ax.set_xlabel("Longitude", fontsize=15)
        ax.set_ylabel("Latitude", fontsize=15)
        ax.tick_params(labelsize=15)
        ax.spines['top'].set_color('black')
        ax.spines['right'].set_color('black')
        ax.spines['bottom'].set_color('black')
        ax.spines['left'].set_color('black')

    # Turn off any unused axes
    for j in range(n, len(axes)):
        axes[j].axis('off')

    fig.suptitle(f'Geo-referenced Rasters (v{iteration})', fontsize=16, fontweight='bold')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

def main(iteration=0):
    INPUT_BBOX = [11.3607, 48.0615, 11.7232, 48.2482]  # Munich BBOX
    rasters = []
    titles = []

    for spatial_resolution in [2000, 1000, 500, 250, 50]: 
        raster = genRaster(INPUT_BBOX, spatial_resolution)
        rasters.append(raster)
        titles.append(f"{spatial_resolution}m x {spatial_resolution}m")

    try:
        vizRaster(rasters, INPUT_BBOX, titles, iteration=iteration)
    except Exception as e:
        print(f"Visualization failed: {e}")

if __name__ == "__main__":
    main(0)
