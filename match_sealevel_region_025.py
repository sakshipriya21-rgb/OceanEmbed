import xarray as xr
import numpy as np
import glob

# Load sea-level dataset
file = glob.glob("data/real_sealevel_region/*.nc")[0]
ds = xr.open_dataset(file)

# Common 0.25° grid
target_latitudes = np.arange(15.0, 20.0 + 0.001, 0.25)
target_longitudes = np.arange(60.0, 65.0 + 0.001, 0.25)

# Interpolate each variable
sla_025 = ds["sla"].interp(
    latitude=target_latitudes,
    longitude=target_longitudes,
    method="linear"
)

current_u_025 = ds["ugosa"].interp(
    latitude=target_latitudes,
    longitude=target_longitudes,
    method="linear"
)

current_v_025 = ds["vgosa"].interp(
    latitude=target_latitudes,
    longitude=target_longitudes,
    method="linear"
)

print("Original shape:")
print(ds["sla"].shape)

print("\nAfter 0.25° interpolation:")
print("SLA:", sla_025.shape)
print("Current U:", current_u_025.shape)
print("Current V:", current_v_025.shape)

print("\nRanges after interpolation:")

print(
    "SLA:",
    float(sla_025.min()),
    "to",
    float(sla_025.max()),
    "m"
)

print(
    "Current U:",
    float(current_u_025.min()),
    "to",
    float(current_u_025.max()),
    "m/s"
)

print(
    "Current V:",
    float(current_v_025.min()),
    "to",
    float(current_v_025.max()),
    "m/s"
)

# Save
sla_025.to_netcdf(
    "data/real_sealevel_region/sla_025.nc"
)

current_u_025.to_netcdf(
    "data/real_sealevel_region/current_u_025.nc"
)

current_v_025.to_netcdf(
    "data/real_sealevel_region/current_v_025.nc"
)

print("\nSaved:")
print("sla_025.nc")
print("current_u_025.nc")
print("current_v_025.nc")