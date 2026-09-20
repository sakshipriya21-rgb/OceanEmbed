import xarray as xr
import glob

files = glob.glob("data/real_sealevel_region/*.nc")

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

print("\nSLA:")
print("Minimum:", float(ds.sla.min()))
print("Maximum:", float(ds.sla.max()))
print("Units:", ds.sla.attrs.get("units"))

print("\nCurrent U:")
print("Minimum:", float(ds.ugosa.min()))
print("Maximum:", float(ds.ugosa.max()))
print("Units:", ds.ugosa.attrs.get("units"))

print("\nCurrent V:")
print("Minimum:", float(ds.vgosa.min()))
print("Maximum:", float(ds.vgosa.max()))
print("Units:", ds.vgosa.attrs.get("units"))