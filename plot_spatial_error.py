import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


DATA_DIR = Path("data/spatial_demo")
OUTPUT_DIR = Path("frontend/images/spatial_demo")


absolute_error = np.load(
    DATA_DIR / "absolute_error_grid.npy"
)

latitudes = np.load(
    DATA_DIR / "latitudes.npy"
)

longitudes = np.load(
    DATA_DIR / "longitudes.npy"
)

depths = np.load(
    DATA_DIR / "depths.npy"
)


selected_depths = [0, 100, 200, 500, 1000]


for depth in selected_depths:

    depth_index = np.where(depths == depth)[0][0]

    error_map = absolute_error[depth_index]

    plt.figure(figsize=(6, 5))

    plt.imshow(
        error_map,
        origin="lower",
        extent=[
            longitudes.min(),
            longitudes.max(),
            latitudes.min(),
            latitudes.max()
        ],
        aspect="auto"
    )

    plt.colorbar(
        label="Absolute Error (°C)"
    )

    plt.xlabel("Longitude (°E)")
    plt.ylabel("Latitude (°N)")

    plt.title(
        f"OceanEmbed Absolute Error at {depth} m"
    )

    plt.tight_layout()

    output_file = (
        OUTPUT_DIR /
        f"error_{depth}m.png"
    )

    plt.savefig(
        output_file,
        dpi=150
    )

    plt.close()

    print(
        f"Created error map for {depth} m"
    )


print(
    "\nSpatial error maps created successfully."
)