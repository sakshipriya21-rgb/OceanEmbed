import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


DATA_DIR = Path("data/spatial_demo")
OUTPUT_DIR = Path("frontend/images")

depths = np.load(DATA_DIR / "depths.npy")
depth_rmse = np.load(DATA_DIR / "depth_rmse.npy")


plt.figure(figsize=(8, 5))

plt.plot(
    depths,
    depth_rmse,
    marker="o",
    linewidth=2
)

plt.xlabel("Depth (m)")
plt.ylabel("RMSE (°C)")
plt.title("Depth-wise Spatial Reconstruction Error")

plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "depth_wise_rmse.png",
    dpi=150
)

plt.close()

print("Depth-wise RMSE chart created successfully.")