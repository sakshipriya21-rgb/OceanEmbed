import xarray as xr
import glob

# -------------------------------
# 1. Open GLORYS
# -------------------------------

glorys_file = glob.glob(
    "data/real_glorys_test_1100/*.nc"
)[0]

glorys = xr.open_dataset(glorys_file)

# -------------------------------
# 2. Open SSS
# -------------------------------

sss_file = glob.glob(
    "data/real_sss_test/*.nc"
)[0]

sss = xr.open_dataset(sss_file)

# -------------------------------
# 3. Select first day and surface
# -------------------------------

sss_day = sss["sos"].isel(
    time=0,
    depth=0
)

# -------------------------------
# 4. Interpolate SSS onto
#    GLORYS grid
# -------------------------------

sss_on_glorys_grid = sss_day.interp(
    latitude=glorys.latitude,
    longitude=glorys.longitude,
    method="linear"
)

# -------------------------------
# 5. Print information
# -------------------------------

print("Original SSS grid:")
print("Latitude:", len(sss.latitude))
print("Longitude:", len(sss.longitude))

print("\nGLORYS grid:")
print("Latitude:", len(glorys.latitude))
print("Longitude:", len(glorys.longitude))

print("\nSSS after matching to GLORYS:")
print(sss_on_glorys_grid.shape)

print(
    "\nExample SSS value:",
    float(sss_on_glorys_grid.values[6, 6]),
    "PSU"
)