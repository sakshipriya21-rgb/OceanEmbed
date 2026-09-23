import numpy as np
import os

# Create output directory
os.makedirs("data/spatial_demo", exist_ok=True)

# Load real demonstration data
X = np.load("data/real_model_ready/X.npy")
Y = np.load("data/real_model_ready/Y.npy")
locations = np.load(
    "data/real_model_ready/locations.npy",
    allow_pickle=True
)
depths = np.load("data/real_model_ready/depths.npy")

print("Input shape:", X.shape)
print("Target shape:", Y.shape)
print("Locations shape:", locations.shape)
print("Depths:", depths)

# Extract latitude and longitude
latitudes = np.array([float(row[1]) for row in locations])
longitudes = np.array([float(row[2]) for row in locations])

# Get unique grid coordinates
unique_lats = np.sort(np.unique(latitudes))
unique_lons = np.sort(np.unique(longitudes))

print("\nUnique latitudes:", unique_lats)
print("Unique longitudes:", unique_lons)

# Load the already generated realistic-model predictions
predictions = np.load(
    "data/real_model_ready/realistic_predictions.npy"
)

print("\nPrediction shape:", predictions.shape)

# Create spatial arrays
# Dimensions:
# depth × latitude × longitude
real_grid = np.full(
    (len(depths), len(unique_lats), len(unique_lons)),
    np.nan
)

prediction_grid = np.full(
    (len(depths), len(unique_lats), len(unique_lons)),
    np.nan
)

# Put every profile at its corresponding grid location
for i in range(len(locations)):

    lat = float(locations[i][1])
    lon = float(locations[i][2])

    lat_index = np.where(unique_lats == lat)[0][0]
    lon_index = np.where(unique_lons == lon)[0][0]

    real_grid[:, lat_index, lon_index] = Y[i]
    prediction_grid[:, lat_index, lon_index] = predictions[i]

# Save the spatial demonstration data
np.save(
    "data/spatial_demo/real_temperature_grid.npy",
    real_grid
)

np.save(
    "data/spatial_demo/predicted_temperature_grid.npy",
    prediction_grid
)

np.save(
    "data/spatial_demo/latitudes.npy",
    unique_lats
)

np.save(
    "data/spatial_demo/longitudes.npy",
    unique_lons
)

np.save(
    "data/spatial_demo/depths.npy",
    depths
)

print("\nSpatial demonstration created successfully.")

print("\nFinal grid shape:")
print("Temperature grid:", prediction_grid.shape)

print("\nGrid dimensions:")
print("Depth levels:", len(depths))
print("Latitude points:", len(unique_lats))
print("Longitude points:", len(unique_lons))

print("\nSaved files:")
print("data/spatial_demo/real_temperature_grid.npy")
print("data/spatial_demo/predicted_temperature_grid.npy")
print("data/spatial_demo/latitudes.npy")
print("data/spatial_demo/longitudes.npy")
print("data/spatial_demo/depths.npy")