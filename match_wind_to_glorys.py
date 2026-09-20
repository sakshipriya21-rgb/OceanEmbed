import xarray as xr
import glob

# Load GLORYS data
glorys_file = glob.glob("data/real_glorys_test_1100/*.nc")[0]
glorys = xr.open_dataset(glorys_file)

# Load wind data
wind_file = glob.glob("data/real_wind_test/*.nc")[0]
wind = xr.open_dataset(wind_file)

# Select the first day
wind_u = wind["eastward_wind"].isel(time=1)
wind_v = wind["northward_wind"].isel(time=1)

# Interpolate wind onto GLORYS grid
wind_u_on_glorys = wind_u.interp(
    latitude=glorys.latitude,
    longitude=glorys.longitude,
    method="linear"
)

wind_v_on_glorys = wind_v.interp(
    latitude=glorys.latitude,
    longitude=glorys.longitude,
    method="linear"
)

print("Original wind grid:")
print("Latitude:", len(wind.latitude))
print("Longitude:", len(wind.longitude))

print("\nGLORYS grid:")
print("Latitude:", len(glorys.latitude))
print("Longitude:", len(glorys.longitude))

print("\nWind U after matching:")
print(wind_u_on_glorys.shape)

print("\nWind V after matching:")
print(wind_v_on_glorys.shape)

print("\nExample Wind U:", float(
    wind_u_on_glorys.values[6, 6]
), "m/s")

print("Example Wind V:", float(
    wind_v_on_glorys.values[6, 6]
), "m/s")