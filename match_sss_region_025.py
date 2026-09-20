import xarray as xr
import numpy as np
import glob

# Load SSS
sss_file = glob.glob("data/real_sss_region/*.nc")[0]
sss = xr.open_dataset(sss_file)

# Remove the single depth dimension
sss_surface = sss["sos"].isel(depth=0)

# Common SIH-style 0.25° grid
target_latitudes = np.arange(15.0, 20.0 + 0.001, 0.25)
target_longitudes = np.arange(60.0, 65.0 + 0.001, 0.25)

# Interpolate SSS onto the common grid
sss_025 = sss_surface.interp(
    latitude=target_latitudes,
    longitude=target_longitudes,
    method="linear"
)

print("Original SSS shape:")
print(sss_surface.shape)

print("\nSSS after 0.25° interpolation:")
print(sss_025.shape)

print("\nSSS range after interpolation:")
print(
    float(sss_025.min()),
    "to",
    float(sss_025.max())
)

print("\nExample SSS value:")
print(
    float(
        sss_025.isel(
            time=0,
            latitude=2,
            longitude=2
        ).values
    )
)

# Save
sss_025.to_netcdf(
    "data/real_sss_region/sss_025.nc"
)

print("\nSaved:")
print("data/real_sss_region/sss_025.nc")