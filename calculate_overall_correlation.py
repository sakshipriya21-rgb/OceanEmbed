import numpy as np
from pathlib import Path


DATA_DIR = Path("data/spatial_demo")

real_temperature = np.load(
    DATA_DIR / "real_temperature_grid.npy"
)

predicted_temperature = np.load(
    DATA_DIR / "predicted_temperature_grid.npy"
)

real_values = real_temperature.flatten()
predicted_values = predicted_temperature.flatten()

correlation = np.corrcoef(
    real_values,
    predicted_values
)[0, 1]

print(
    f"Overall demonstration correlation: {correlation:.4f}"
)

np.save(
    DATA_DIR / "overall_correlation.npy",
    np.array(correlation)
)

print("Overall correlation saved successfully.")