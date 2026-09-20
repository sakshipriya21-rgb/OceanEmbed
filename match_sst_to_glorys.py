import xarray as xr
import glob

# -------------------------------
# 1. Open GLORYS data
# -------------------------------

glorys_file = glob.glob(
    "data/real_glorys_test_1100/*.nc"
)[0]

glorys = xr.open_dataset(glorys_file)

# -------------------------------
# 2. Open processed SST data
# -------------------------------

sst = xr.open_dataset(
    "data/real_sst_test/sst_celsius.nc"
)

# -------------------------------
# 3. Select the first day
# -------------------------------

sst_day = sst["analysed_sst"].isel(time=0)

# -------------------------------
# 4. Interpolate SST onto
#    GLORYS latitude/longitude
# -------------------------------

sst_on_glorys_grid = sst_day.interp(
    latitude=glorys.latitude,
    longitude=glorys.longitude,
    method="linear"
)

# -------------------------------
# 5. Print information
# -------------------------------

print("GLORYS grid:")
print("Latitude:", len(glorys.latitude))
print("Longitude:", len(glorys.longitude))

print("\nOriginal SST grid:")
print("Latitude:", len(sst.latitude))
print("Longitude:", len(sst.longitude))

print("\nSST after matching to GLORYS:")
print(sst_on_glorys_grid.shape)

print(
    "\nExample SST value:",
    float(sst_on_glorys_grid.values[6, 6]),
    "°C"
)