import xarray as xr
import glob
import numpy as np

wind_file = glob.glob("data/real_wind_test/*.nc")[0]

wind = xr.open_dataset(wind_file)
print("Checking:", wind.time.values[1])
wind_u = wind["eastward_wind"].isel(time=1)
wind_v = wind["northward_wind"].isel(time=1)

print("Wind U:")
print("Total values:", wind_u.size)
print("NaN values:", int(np.isnan(wind_u.values).sum()))

print("\nWind V:")
print("Total values:", wind_v.size)
print("NaN values:", int(np.isnan(wind_v.values).sum()))

print("\nWind U values:")
print(wind_u.values)

print("\nWind V values:")
print(wind_v.values)