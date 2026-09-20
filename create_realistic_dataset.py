import numpy as np
import os

# ===================================================
# 1. Basic settings
# ===================================================

N = 5000
rng = np.random.default_rng(42)

os.makedirs("data/synthetic_realistic", exist_ok=True)

# ===================================================
# 2. Generate surface ocean variables
# ===================================================

SST = rng.uniform(24, 31, N)
SSS = rng.uniform(33, 36, N)
SSH = rng.uniform(-0.5, 0.5, N)

CURRENT_U = rng.uniform(-1, 1, N)
CURRENT_V = rng.uniform(-1, 1, N)

WIND_U = rng.uniform(-10, 10, N)
WIND_V = rng.uniform(-10, 10, N)

X = np.column_stack([
    SST,
    SSS,
    SSH,
    CURRENT_U,
    CURRENT_V,
    WIND_U,
    WIND_V
])

# ===================================================
# 3. Standard depths
# ===================================================

depths = np.array([
    0, 5, 10, 20, 30,
    50, 75, 100, 125, 150,
    200, 300, 500, 700, 1000
])

# ===================================================
# 4. Create realistic synthetic temperature profiles
# ===================================================

Y = np.zeros((N, len(depths)))

# Deep-ocean temperature varies slightly with
# salinity, sea-level anomaly and currents.
deep_temperature = (
    7.5
    + 0.30 * (SSS - 34.5)
    + 0.35 * SSH
    + 0.10 * CURRENT_U
    - 0.08 * CURRENT_V
)

# Thermocline depth varies slightly between samples.
thermocline_depth = (
    110
    + 12 * SSH
    - 8 * CURRENT_U
    + 5 * CURRENT_V
)

for i, depth in enumerate(depths):

    # Broad surface-to-deep cooling.
    base_temperature = (
        deep_temperature
        + (SST - deep_temperature)
        * np.exp(-depth / 350.0)
    )

    # Thermocline-like additional cooling.
    thermocline_effect = (
        0.7
        * (1 - np.exp(-depth / 20.0))
        * np.exp(
            -((depth - thermocline_depth) / 90.0) ** 2
        )
    )

    # Small influence from surface forcing.
    forcing_effect = (
        0.04 * CURRENT_U * (depth / 1000)
        - 0.03 * CURRENT_V * (depth / 1000)
        + 0.015 * WIND_U * (depth / 1000)
        - 0.012 * WIND_V * (depth / 1000)
    )

    Y[:, i] = (
        base_temperature
        - thermocline_effect
        + forcing_effect
    )

# ===================================================
# 5. Small measurement-like noise
# ===================================================

noise = rng.normal(0, 0.05, Y.shape)
Y = Y + noise

# ===================================================
# 6. Save
# ===================================================

np.save("data/synthetic_realistic/X.npy", X)
np.save("data/synthetic_realistic/Y.npy", Y)
np.save("data/synthetic_realistic/depths.npy", depths)

print("Realistic synthetic dataset created successfully!")
print("X shape:", X.shape)
print("Y shape:", Y.shape)
print("Depths:", depths)

print("\nTemperature range:")
print("Minimum:", Y.min())
print("Maximum:", Y.max())

print("\nExample profile:")
print(Y[0])
