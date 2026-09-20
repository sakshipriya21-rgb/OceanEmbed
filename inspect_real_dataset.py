import numpy as np


# Load dataset
X = np.load(
    "data/real_glorys_test_1100/X_real.npy"
)

Y = np.load(
    "data/real_glorys_test_1100/Y_real.npy"
)

locations = np.load(
    "data/real_glorys_test_1100/locations_real.npy"
)

depths = np.load(
    "data/real_glorys_test_1100/target_depths.npy"
)


print("======================================")
print("REAL DATASET INSPECTION")
print("======================================")


# Shapes
print("\nShapes:")
print("X:", X.shape)
print("Y:", Y.shape)
print("Locations:", locations.shape)


# Input statistics
names = [
    "SST",
    "SSS",
    "SLA",
    "Current U",
    "Current V",
    "Wind U",
    "Wind V"
]


print("\nInput statistics:")

for i, name in enumerate(names):

    print("\n" + name)

    print(
        "Minimum:",
        X[:, i].min()
    )

    print(
        "Maximum:",
        X[:, i].max()
    )

    print(
        "Mean:",
        X[:, i].mean()
    )

    print(
        "Standard deviation:",
        X[:, i].std()
    )


# Target statistics
print("\nTarget temperature statistics:")

print(
    "Minimum:",
    Y.min(),
    "°C"
)

print(
    "Maximum:",
    Y.max(),
    "°C"
)

print(
    "Mean:",
    Y.mean(),
    "°C"
)

print(
    "Standard deviation:",
    Y.std(),
    "°C"
)


# Missing values
print("\nMissing values:")

print(
    "X NaNs:",
    np.isnan(X).sum()
)

print(
    "Y NaNs:",
    np.isnan(Y).sum()
)


# Depth-wise mean temperature
print("\nMean temperature at each depth:")

for depth, mean_temperature in zip(
    depths,
    Y.mean(axis=0)
):

    print(
        f"{depth:4d} m : "
        f"{mean_temperature:.2f} °C"
    )