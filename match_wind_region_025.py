import xarray as xr
import glob
import numpy as np

# Find the downloaded wind file
file = glob.glob("data/real_wind_region/*.nc")[0]

ds = xr.open_dataset(file)

# Create the target 0.25° grid
target_latitudes = np.arange(15.0, 20.0 + 0.001, 0.25)
target_longitudes = np.arange(60.0, 65.0 + 0.001, 0.25)

# Interpolate wind components to the target grid
wind_u_025 = ds["eastward_wind"].interp(
    latitude=target_latitudes,
    longitude=target_longitudes,
    method="linear"
)

wind_v_025 = ds["northward_wind"].interp(
    latitude=target_latitudes,
    longitude=target_longitudes,
    method="linear"
)

print("Original wind grid:")
print("Latitude:", len(ds.latitude))
print("Longitude:", len(ds.longitude))

print("\nWind after matching to 0.25° grid:")
print("Wind U shape:", wind_u_025.shape)
print("Wind V shape:", wind_v_025.shape)

print("\nWind U:")
print("Minimum:", float(wind_u_025.min()))
print("Maximum:", float(wind_u_025.max()))
print("NaN count:", int(wind_u_025.isnull().sum()))

print("\nWind V:")
print("Minimum:", float(wind_v_025.min()))
print("Maximum:", float(wind_v_025.max()))
print("NaN count:", int(wind_v_025.isnull().sum()))

# Save processed wind data
wind_u_025.to_netcdf(
    "data/real_wind_region/wind_u_025.nc"
)

wind_v_025.to_netcdf(
    "data/real_wind_region/wind_v_025.nc"
)

print("\nSaved:")
print("data/real_wind_region/wind_u_025.nc")
print("data/real_wind_region/wind_v_025.nc")