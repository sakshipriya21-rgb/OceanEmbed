import xarray as xr
import numpy as np
import glob

# ---------------------------------------------------
# 1. Find the GLORYS file
# ---------------------------------------------------

files = glob.glob("data/real_glorys_test_1100/*.nc")
file = files[0]

ds = xr.open_dataset(file)

# ---------------------------------------------------
# 2. SIH26066 standard depths
# ---------------------------------------------------

target_depths = np.array([
    0, 5, 10, 20, 30, 50, 75, 100,
    125, 150, 200, 300, 500, 700, 1000
])

# ---------------------------------------------------
# 3. Get dimensions
# ---------------------------------------------------

times = ds.time.values
latitudes = ds.latitude.values
longitudes = ds.longitude.values

print("Number of time steps:", len(times))
print("Number of latitudes:", len(latitudes))
print("Number of longitudes:", len(longitudes))

# ---------------------------------------------------
# 4. Prepare output
# ---------------------------------------------------

number_of_samples = (
    len(times)
    * len(latitudes)
    * len(longitudes)
)

Y = np.zeros(
    (number_of_samples, len(target_depths))
)

# ---------------------------------------------------
# 5. Store location information
# ---------------------------------------------------

locations = []

sample_index = 0

# ---------------------------------------------------
# 6. Interpolate every profile
# ---------------------------------------------------

for t in range(len(times)):

    for lat in range(len(latitudes)):

        for lon in range(len(longitudes)):

            profile = ds.thetao.isel(
                time=t,
                latitude=lat,
                longitude=lon
            ).values

            # Check for missing values
            if np.all(np.isnan(profile)):
                continue

            # Find valid values
            valid = ~np.isnan(profile)

            native_depths = ds.depth.values[valid]
            native_temperature = profile[valid]

            # Interpolate
            interpolated = np.interp(
                target_depths,
                native_depths,
                native_temperature
            )

            Y[sample_index] = interpolated

            locations.append([
                times[t],
                latitudes[lat],
                longitudes[lon]
            ])

            sample_index += 1

# ---------------------------------------------------
# 7. Remove unused rows
# ---------------------------------------------------

Y = Y[:sample_index]

locations = np.array(
    locations,
    dtype=object
)

# ---------------------------------------------------
# 8. Save the dataset
# ---------------------------------------------------

np.save(
    "data/real_glorys_test_1100/Y_real.npy",
    Y
)

np.save(
    "data/real_glorys_test_1100/locations.npy",
    locations
)

np.save(
    "data/real_glorys_test_1100/target_depths.npy",
    target_depths
)

# ---------------------------------------------------
# 9. Print results
# ---------------------------------------------------

print("\nReal GLORYS target dataset created!")

print("Y shape:", Y.shape)

print("Locations shape:", locations.shape)

print("Target depths:", target_depths)

print("\nFirst profile:")

for depth, temperature in zip(
    target_depths,
    Y[0]
):
    print(
        f"Depth = {depth:4d} m   "
        f"Temperature = {temperature:.2f} °C"
    )