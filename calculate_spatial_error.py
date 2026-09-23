import numpy as np
from pathlib import Path


# --------------------------------------------------
# Paths
# --------------------------------------------------

DATA_DIR = Path("data/spatial_demo")


# --------------------------------------------------
# Load spatial temperature grids
# --------------------------------------------------

real_temperature = np.load(
    DATA_DIR / "real_temperature_grid.npy"
)

predicted_temperature = np.load(
    DATA_DIR / "predicted_temperature_grid.npy"
)

depths = np.load(
    DATA_DIR / "depths.npy"
)


print("Real temperature shape:", real_temperature.shape)
print("Predicted temperature shape:", predicted_temperature.shape)
print("Depths:", depths)


# --------------------------------------------------
# Calculate absolute error
# --------------------------------------------------

absolute_error = np.abs(
    predicted_temperature - real_temperature
)


# --------------------------------------------------
# Calculate RMSE for each depth
# --------------------------------------------------

depth_rmse = np.sqrt(
    np.mean(
        (predicted_temperature - real_temperature) ** 2,
        axis=(1, 2)
    )
)


# --------------------------------------------------
# Calculate MAE for each depth
# --------------------------------------------------

depth_mae = np.mean(
    absolute_error,
    axis=(1, 2)
)


# --------------------------------------------------
# Print results
# --------------------------------------------------

print("\nDepth-wise spatial error:")

for i, depth in enumerate(depths):

    print(
        f"Depth {depth:4.0f} m | "
        f"MAE = {depth_mae[i]:.4f} °C | "
        f"RMSE = {depth_rmse[i]:.4f} °C"
    )


# --------------------------------------------------
# Save results
# --------------------------------------------------

np.save(
    DATA_DIR / "absolute_error_grid.npy",
    absolute_error
)

np.save(
    DATA_DIR / "depth_mae.npy",
    depth_mae
)

np.save(
    DATA_DIR / "depth_rmse.npy",
    depth_rmse
)


print("\nSpatial error calculation completed successfully.")