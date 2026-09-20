import xarray as xr
import glob

files = glob.glob("data/real_wind_region/*.nc")

print("Number of files:", len(files))

file = files[0]
ds = xr.open_dataset(file)

print("\nDataset:")
print(ds)

print("\nDimensions:")
print(ds.dims)

print("\nCoordinates:")
print("Time:", len(ds.time))
print("Latitude:", len(ds.latitude))
print("Longitude:", len(ds.longitude))

print("\nRanges:")
print("Latitude:", float(ds.latitude.min()), "to", float(ds.latitude.max()))
print("Longitude:", float(ds.longitude.min()), "to", float(ds.longitude.max()))

print("\nWind U:")
print("Minimum:", float(ds.eastward_wind.min(skipna=True)))
print("Maximum:", float(ds.eastward_wind.max(skipna=True)))
print("NaN count:", int(ds.eastward_wind.isnull().sum()))

print("\nWind V:")
print("Minimum:", float(ds.northward_wind.min(skipna=True)))
print("Maximum:", float(ds.northward_wind.max(skipna=True)))
print("NaN count:", int(ds.northward_wind.isnull().sum()))

print("\nUnits:")
print("Wind U:", ds.eastward_wind.attrs.get("units"))
print("Wind V:", ds.northward_wind.attrs.get("units"))