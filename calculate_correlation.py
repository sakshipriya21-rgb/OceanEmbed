import numpy as np
from pathlib import Path


DATA_DIR = Path("data/spatial_demo")

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


print("\nDepth-wise Pearson correlation:")

correlations = []

for i, depth in enumerate(depths):

    real_values = real_temperature[i].flatten()
    predicted_values = predicted_temperature[i].flatten()

    correlation = np.corrcoef(
        real_values,
        predicted_values
    )[0, 1]

    correlations.append(correlation)

    print(
        f"Depth {depth:4.0f} m | "
        f"Correlation = {correlation:.4f}"
    )


correlations = np.array(correlations)

np.save(
    DATA_DIR / "depth_correlation.npy",
    correlations
)


print("\nCorrelation calculation completed successfully.")