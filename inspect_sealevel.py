import xarray as xr
import glob

files = glob.glob("data/real_sealevel_test/*.nc")

file = files[0]

ds = xr.open_dataset(file)

print(ds)