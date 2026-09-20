import xarray as xr
import glob
import numpy as np


# ---------------------------------------------------
# 1. Load all datasets
# ---------------------------------------------------

glorys_file = glob.glob(
    "data/real_glorys_test_1100/*.nc"
)[0]

sst_file = "data/real_sst_test/sst_celsius.nc"

sss_file = glob.glob(
    "data/real_sss_test/*.nc"
)[0]

sealevel_file = glob.glob(
    "data/real_sealevel_test/*.nc"
)[0]

wind_file = glob.glob(
    "data/real_wind_test/*.nc"
)[0]


glorys = xr.open_dataset(glorys_file)
sst = xr.open_dataset(sst_file)
sss = xr.open_dataset(sss_file)
sealevel = xr.open_dataset(sealevel_file)
wind = xr.open_dataset(wind_file)


# ---------------------------------------------------
# 2. Use January 2
# ---------------------------------------------------

time_index = 1


# ---------------------------------------------------
# 3. Match all surface variables to GLORYS grid
# ---------------------------------------------------

sst_day = sst["analysed_sst"].isel(
    time=time_index
)

sst_on_glorys = sst_day.interp(
    latitude=glorys.latitude,
    longitude=glorys.longitude,
    method="linear"
)


sss_day = sss["sos"].isel(
    time=time_index,
    depth=0
)

sss_on_glorys = sss_day.interp(
    latitude=glorys.latitude,
    longitude=glorys.longitude,
    method="linear"
)


sla = sealevel["sla"].isel(
    time=time_index
)

current_u = sealevel["ugosa"].isel(
    time=time_index
)

current_v = sealevel["vgosa"].isel(
    time=time_index
)

sla_on_glorys = sla.interp(
    latitude=glorys.latitude,
    longitude=glorys.longitude,
    method="linear"
)

current_u_on_glorys = current_u.interp(
    latitude=glorys.latitude,
    longitude=glorys.longitude,
    method="linear"
)

current_v_on_glorys = current_v.interp(
    latitude=glorys.latitude,
    longitude=glorys.longitude,
    method="linear"
)


wind_u = wind["eastward_wind"].isel(
    time=time_index
)

wind_v = wind["northward_wind"].isel(
    time=time_index
)

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


# ---------------------------------------------------
# 4. Count NaNs in each variable
# ---------------------------------------------------

variables = {
    "SST": sst_on_glorys.values,
    "SSS": sss_on_glorys.values,
    "SLA": sla_on_glorys.values,
    "Current U": current_u_on_glorys.values,
    "Current V": current_v_on_glorys.values,
    "Wind U": wind_u_on_glorys.values,
    "Wind V": wind_v_on_glorys.values
}


print("======================================")
print("REAL DATA QUALITY CHECK")
print("======================================")

for name, values in variables.items():

    total = values.size
    nan_count = int(np.isnan(values).sum())
    valid_count = total - nan_count

    print("\n" + name)
    print("Total values :", total)
    print("Valid values :", valid_count)
    print("NaN values   :", nan_count)


# ---------------------------------------------------
# 5. Check complete samples
# ---------------------------------------------------

all_variables = np.stack([
    sst_on_glorys.values,
    sss_on_glorys.values,
    sla_on_glorys.values,
    current_u_on_glorys.values,
    current_v_on_glorys.values,
    wind_u_on_glorys.values,
    wind_v_on_glorys.values
], axis=-1)


complete_samples = np.all(
    np.isfinite(all_variables),
    axis=-1
)


print("\n======================================")
print("COMPLETE SAMPLE CHECK")
print("======================================")

print("Grid shape:", complete_samples.shape)

print(
    "Complete samples:",
    int(complete_samples.sum())
)

print(
    "Incomplete samples:",
    int((~complete_samples).sum())
)

print(
    "Total samples:",
    complete_samples.size
)