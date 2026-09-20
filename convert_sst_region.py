import xarray as xr
import glob

files = glob.glob("data/real_sst_region/*.nc")

file = files[0]
ds = xr.open_dataset(file)

# Convert Kelvin to Celsius
sst_celsius = ds["analysed_sst"] - 273.15

print("SST shape:", sst_celsius.shape)

print("\nTemperature range:")
print("Minimum:", float(sst_celsius.min()), "°C")
print("Maximum:", float(sst_celsius.max()), "°C")

print("\nFirst value:")
print(float(sst_celsius.values.flat[0]), "°C")

# Save converted SST
sst_celsius.to_netcdf(
    "data/real_sst_region/sst_celsius.nc"
)

print("\nSaved:")
print("data/real_sst_region/sst_celsius.nc")