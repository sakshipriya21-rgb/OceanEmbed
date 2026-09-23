import numpy as np
import os
import matplotlib.pyplot as plt

# Create output directory
os.makedirs("frontend/images/spatial_demo", exist_ok=True)

# Load spatial demonstration data
real_grid = np.load(
    "data/spatial_demo/real_temperature_grid.npy"
)

prediction_grid = np.load(
    "data/spatial_demo/predicted_temperature_grid.npy"
)

latitudes = np.load(
    "data/spatial_demo/latitudes.npy"
)

longitudes = np.load(
    "data/spatial_demo/longitudes.npy"
)

depths = np.load(
    "data/spatial_demo/depths.npy"
)

# Depths that we want to visualize
selected_depths = [0, 100, 200, 500, 1000]

for depth in selected_depths:

    # Find depth index
    depth_index = np.where(depths == depth)[0][0]

    # Extract temperature fields
    real_temperature = real_grid[depth_index]
    predicted_temperature = prediction_grid[depth_index]

    # -----------------------------
    # Real GLORYS map
    # -----------------------------

    plt.figure(figsize=(7, 5))

    image = plt.imshow(
        real_temperature,
        origin="lower",
        extent=[
            longitudes.min(),
            longitudes.max(),
            latitudes.min(),
            latitudes.max()
        ],
        aspect="auto"
    )

    plt.colorbar(image, label="Temperature (°C)")

    plt.xlabel("Longitude (°E)")
    plt.ylabel("Latitude (°N)")
    plt.title(
        f"Real GLORYS12V1 Temperature at {depth} m"
    )

    plt.tight_layout()

    plt.savefig(
        f"frontend/images/spatial_demo/"
        f"real_glorys_{depth}m.png",
        dpi=200
    )

    plt.close()

    # -----------------------------
    # OceanEmbed prediction map
    # -----------------------------

    plt.figure(figsize=(7, 5))

    image = plt.imshow(
        predicted_temperature,
        origin="lower",
        extent=[
            longitudes.min(),
            longitudes.max(),
            latitudes.min(),
            latitudes.max()
        ],
        aspect="auto"
    )

    plt.colorbar(image, label="Temperature (°C)")

    plt.xlabel("Longitude (°E)")
    plt.ylabel("Latitude (°N)")
    plt.title(
        f"OceanEmbed Predicted Temperature at {depth} m"
    )

    plt.tight_layout()

    plt.savefig(
        f"frontend/images/spatial_demo/"
        f"oceanembed_{depth}m.png",
        dpi=200
    )

    plt.close()

    print(f"Created maps for {depth} m")

print("\nSpatial temperature maps created successfully.")