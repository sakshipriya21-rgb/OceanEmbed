import xarray as xr
import glob

files = glob.glob("data/real_glorys_region/*.nc")

print("Number of files:", len(files))

file = files[0]

ds = xr.open_dataset(file)

print("\nDataset:")
print(ds)

print("\nDimensions:")
print(ds.dims)

print("\nCoordinates:")
print("Time:", len(ds.time))
print("Depth:", len(ds.depth))
print("Latitude:", len(ds.latitude))
print("Longitude:", len(ds.longitude))

print("\nRanges:")
print("Latitude:", float(ds.latitude.min()), "to", float(ds.latitude.max()))
print("Longitude:", float(ds.longitude.min()), "to", float(ds.longitude.max()))
print("Depth:", float(ds.depth.min()), "to", float(ds.depth.max()))
print("Temperature:", float(ds.thetao.min()), "to", float(ds.thetao.max()))