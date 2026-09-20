import xarray as xr
import numpy as np
import glob
import os

print("Starting real dataset preparation...")

# ---------------------------------------------------
# 1. Find the datasets
# ---------------------------------------------------

glorys_file = glob.glob("data/real_glorys_test_1100/*.nc")[0]
sst_file = "data/real_sst_test/sst_celsius.nc"
sss_file = glob.glob("data/real_sss_test/*.nc")[0]

sla_file = "data/real_sealevel_region/sla_025.nc"
current_u_file = "data/real_sealevel_region/current_u_025.nc"
current_v_file = "data/real_sealevel_region/current_v_025.nc"

wind_u_file = "data/real_wind_region/wind_u_025.nc"
wind_v_file = "data/real_wind_region/wind_v_025.nc"

# ---------------------------------------------------
# 2. Load datasets
# ---------------------------------------------------

print("Loading datasets...")

glorys = xr.open_dataset(glorys_file)
sst = xr.open_dataset(sst_file)
sss = xr.open_dataset(sss_file)

sla = xr.open_dataset(sla_file)
current_u = xr.open_dataset(current_u_file)
current_v = xr.open_dataset(current_v_file)

wind_u = xr.open_dataset(wind_u_file)
wind_v = xr.open_dataset(wind_v_file)

print("All datasets loaded.")

# ---------------------------------------------------
# 3. Extract variables
# ---------------------------------------------------

thetao = glorys["thetao"]

sst_var = sst["analysed_sst"]

sss_var = sss["sos"].isel(depth=0)

sla_var = sla["sla"]
current_u_var = current_u["ugosa"]
current_v_var = current_v["vgosa"]

wind_u_var = wind_u["eastward_wind"]
wind_v_var = wind_v["northward_wind"]

# ---------------------------------------------------
# 4. Convert SST to Celsius if necessary
# ---------------------------------------------------

if float(sst_var.mean()) > 100:
    print("Converting SST from Kelvin to Celsius...")
    sst_var = sst_var - 273.15

# ---------------------------------------------------
# 5. Create common 0.25° grid
# ---------------------------------------------------

target_latitudes = np.arange(15.0, 20.0 + 0.001, 0.25)
target_longitudes = np.arange(60.0, 65.0 + 0.001, 0.25)

print("Target grid:")
print("Latitude:", len(target_latitudes))
print("Longitude:", len(target_longitudes))

# ---------------------------------------------------
# 6. Match all surface variables to common grid
# ---------------------------------------------------

print("Matching surface variables to common grid...")

sst_grid = sst_var.interp(
    latitude=target_latitudes,
    longitude=target_longitudes,
    method="linear"
)

sss_grid = sss_var.interp(
    latitude=target_latitudes,
    longitude=target_longitudes,
    method="linear"
)

sla_grid = sla_var.interp(
    latitude=target_latitudes,
    longitude=target_longitudes,
    method="linear"
)

current_u_grid = current_u_var.interp(
    latitude=target_latitudes,
    longitude=target_longitudes,
    method="linear"
)

current_v_grid = current_v_var.interp(
    latitude=target_latitudes,
    longitude=target_longitudes,
    method="linear"
)

wind_u_grid = wind_u_var.interp(
    latitude=target_latitudes,
    longitude=target_longitudes,
    method="linear"
)

wind_v_grid = wind_v_var.interp(
    latitude=target_latitudes,
    longitude=target_longitudes,
    method="linear"
)

# GLORYS is already close to the required grid.
# Match it to our target grid as well.
thetao_grid = thetao.interp(
    latitude=target_latitudes,
    longitude=target_longitudes,
    method="linear"
)

# ---------------------------------------------------
# 7. Find common dates
# ---------------------------------------------------

print("Finding common dates...")

def date_strings(values):
    return np.array([
        str(t)[:10]
        for t in values
    ])

glorys_dates = date_strings(glorys.time.values)
sst_dates = date_strings(sst.time.values)
sss_dates = date_strings(sss.time.values)
sla_dates = date_strings(sla.time.values)
wind_dates = date_strings(wind_u.time.values)

common_dates = np.intersect1d(
    glorys_dates,
    sst_dates
)

common_dates = np.intersect1d(
    common_dates,
    sss_dates
)

common_dates = np.intersect1d(
    common_dates,
    sla_dates
)

common_dates = np.intersect1d(
    common_dates,
    wind_dates
)

print("Common dates:", common_dates)

# ---------------------------------------------------
# 8. Standard depths
# ---------------------------------------------------

target_depths = np.array([
    0, 5, 10, 20, 30,
    50, 75, 100, 125,
    150, 200, 300, 500,
    700, 1000
])

# ---------------------------------------------------
# 9. Build X and Y
# ---------------------------------------------------

X_list = []
Y_list = []
locations = []

print("Building ML dataset...")

for date in common_dates:

    print("Processing:", date)

    # Find time indices
    t_glorys = np.where(glorys_dates == date)[0][0]
    t_sst = np.where(sst_dates == date)[0][0]
    t_sss = np.where(sss_dates == date)[0][0]
    t_sla = np.where(sla_dates == date)[0][0]
    t_wind = np.where(wind_dates == date)[0][0]

    # Extract one day
    day_sst = sst_grid.isel(time=t_sst).values
    day_sss = sss_grid.isel(time=t_sss).values
    day_sla = sla_grid.isel(time=t_sla).values
    day_current_u = current_u_grid.isel(time=t_sla).values
    day_current_v = current_v_grid.isel(time=t_sla).values

    day_wind_u = wind_u_grid.isel(time=t_wind).values
    day_wind_v = wind_v_grid.isel(time=t_wind).values

    day_thetao = thetao_grid.isel(time=t_glorys)

    # ------------------------------------------------
    # Loop through every grid cell
    # ------------------------------------------------

    for i in range(len(target_latitudes)):

        for j in range(len(target_longitudes)):

            surface_values = np.array([
                day_sst[i, j],
                day_sss[i, j],
                day_sla[i, j],
                day_current_u[i, j],
                day_current_v[i, j],
                day_wind_u[i, j],
                day_wind_v[i, j]
            ])

            # Skip cells with missing surface data
            if np.any(np.isnan(surface_values)):
                continue

            # Extract GLORYS temperature profile
            profile = day_thetao.isel(
                latitude=i,
                longitude=j
            ).values

            native_depths = glorys.depth.values

            valid = ~np.isnan(profile)

            if np.sum(valid) < 2:
                continue

            native_depths_valid = native_depths[valid]
            profile_valid = profile[valid]

            # Interpolate to standard depths
            temperature_profile = np.interp(
                target_depths,
                native_depths_valid,
                profile_valid
            )

            # Store sample
            X_list.append(surface_values)
            Y_list.append(temperature_profile)

            locations.append([
                date,
                target_latitudes[i],
                target_longitudes[j]
            ])

# ---------------------------------------------------
# 10. Convert to NumPy arrays
# ---------------------------------------------------

X = np.array(X_list)
Y = np.array(Y_list)
locations = np.array(locations, dtype=object)

print("\nDataset construction complete.")

print("X shape:", X.shape)
print("Y shape:", Y.shape)
print("Locations shape:", locations.shape)

# ---------------------------------------------------
# 11. Save dataset
# ---------------------------------------------------

output_directory = "data/real_model_ready"

os.makedirs(output_directory, exist_ok=True)

np.save(
    output_directory + "/X.npy",
    X
)

np.save(
    output_directory + "/Y.npy",
    Y
)

np.save(
    output_directory + "/locations.npy",
    locations
)

np.save(
    output_directory + "/depths.npy",
    target_depths
)

print("\nSaved files:")
print(output_directory + "/X.npy")
print(output_directory + "/Y.npy")
print(output_directory + "/locations.npy")
print(output_directory + "/depths.npy")