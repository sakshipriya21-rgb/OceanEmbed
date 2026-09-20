import xarray as xr
import glob

# Open GLORYS
glorys_file = glob.glob(
    "data/real_glorys_test_1100/*.nc"
)[0]

glorys = xr.open_dataset(glorys_file)

# Open SST
sst = xr.open_dataset(
    "data/real_sst_test/sst_celsius.nc"
)

print("GLORYS dates:")
print(glorys.time.values)

print("\nSST dates:")
print(sst.time.values)