import numpy as np
import matplotlib.pyplot as plt


# Load data
Y = np.load(
    "data/real_glorys_test_1100/Y_real.npy"
)

depths = np.load(
    "data/real_glorys_test_1100/target_depths.npy"
)


# Create figure
plt.figure(figsize=(7, 8))


# Plot first 10 profiles
number_of_profiles = min(10, len(Y))

for i in range(number_of_profiles):

    plt.plot(
        Y[i],
        depths,
        marker="o",
        label=f"Profile {i + 1}"
    )


# Depth increases downward
plt.gca().invert_yaxis()


plt.xlabel("Temperature (°C)")
plt.ylabel("Depth (m)")

plt.title(
    "Real GLORYS Subsurface Temperature Profiles"
)

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.show()