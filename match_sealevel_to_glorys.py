import xarray as xr
import glob

# Load GLORYS data
glorys_file = glob.glob("data/real_glorys_test_1100/*.nc")[0]
glorys = xr.open_dataset(glorys_file)

# Load sea-level data
sealevel_file = glob.glob("data/real_sealevel_test/*.nc")[0]
sealevel = xr.open_dataset(sealevel_file)

# Select January 2
sla = sealevel["sla"].isel(time=1)
u_current = sealevel["ugosa"].isel(time=1)
v_current = sealevel["vgosa"].isel(time=1)

# Interpolate onto GLORYS grid
sla_on_glorys = sla.interp(
    latitude=glorys.latitude,
    longitude=glorys.longitude,
    method="linear"
)

u_current_on_glorys = u_current.interp(
    latitude=glorys.latitude,
    longitude=glorys.longitude,
    method="linear"
)

v_current_on_glorys = v_current.interp(
    latitude=glorys.latitude,
    longitude=glorys.longitude,
    method="linear"
)

print("Original sea-level grid:")
print("Latitude:", len(sealevel.latitude))
print("Longitude:", len(sealevel.longitude))

print("\nGLORYS grid:")
print("Latitude:", len(glorys.latitude))
print("Longitude:", len(glorys.longitude))

print("\nSLA after matching:")
print(sla_on_glorys.shape)

print("Current U after matching:")
print(u_current_on_glorys.shape)

print("Current V after matching:")
print(v_current_on_glorys.shape)

print("\nExample SLA:",
      float(sla_on_glorys.values[6, 6]), "m")

print("Example Current U:",
      float(u_current_on_glorys.values[6, 6]), "m/s")

print("Example Current V:",
      float(v_current_on_glorys.values[6, 6]), "m/s")