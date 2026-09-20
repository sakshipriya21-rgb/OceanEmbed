import xarray as xr
import numpy as np
import glob

# ---------------------------------------------------
# 1. Load the GLORYS file
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
# 3. Select one profile
# ---------------------------------------------------

profile = ds.thetao.isel(
    time=0,
    latitude=6,
    longitude=6
)

native_depths = ds.depth.values
native_temperature = profile.values

# ---------------------------------------------------
# 4. Interpolate to SIH depths
# ---------------------------------------------------

interpolated_temperature = np.interp(
    target_depths,
    native_depths,
    native_temperature
)

# ---------------------------------------------------
# 5. Print results
# ---------------------------------------------------

print("Native GLORYS depths:")
print(native_depths)

print("\nSIH26066 target depths:")
print(target_depths)

print("\nInterpolated temperature profile:")
for depth, temperature in zip(
    target_depths,
    interpolated_temperature
):
    print(f"Depth = {depth:4d} m   Temperature = {temperature:.2f} °C")