import xarray as xr
import numpy as np
import glob

# Load the 0.25° GLORYS grid
glorys_file = glob.glob("data/real_glorys_region/*.nc")[0]
glorys = xr.open_dataset(glorys_file)

# Load converted SST
sst = xr.open_dataset("data/real_sst_region/sst_celsius.nc")

# Create the same 0.25° grid used for GLORYS
target_latitudes = np.arange(15.0, 20.0 + 0.001, 0.25)
target_longitudes = np.arange(60.0, 65.0 + 0.001, 0.25)

# Interpolate SST onto the common grid
sst_025 = sst["analysed_sst"].interp(
    latitude=target_latitudes,
    longitude=target_longitudes,
    method="linear"
)

print("Original SST shape:")
print(sst["analysed_sst"].shape)

print("\nSST after 0.25° interpolation:")
print(sst_025.shape)

print("\nSST range after interpolation:")
print(
    float(sst_025.min()),
    "to",
    float(sst_025.max()),
    "°C"
)

print("\nExample SST value:")
print(float(sst_025.isel(time=0, latitude=2, longitude=2).values), "°C")

# Save
sst_025.to_netcdf(
    "data/real_sst_region/sst_025.nc"
)

print("\nSaved:")
print("data/real_sst_region/sst_025.nc")