import pandas as pd
import numpy as np

# File paths
input_file = "data/argo_validation/argo_2902174_cycle379.csv"
output_file = "data/argo_validation/argo_standard_depths.csv"

# OceanEmbed standard depths
target_depths = np.array([
    0, 5, 10, 20, 30,
    50, 75, 100, 125, 150,
    200, 300, 500, 700, 1000
])

# Read ARGO CSV
df = pd.read_csv(input_file, skiprows=[1])

# Convert pressure and temperature to numeric
df["PRES"] = pd.to_numeric(df["PRES"], errors="coerce")
df["TEMP"] = pd.to_numeric(df["TEMP"], errors="coerce")

# Keep only valid pressure-temperature measurements
df = df[["PRES", "TEMP"]].dropna()

# Sort by pressure
df = df.sort_values("PRES")

# Remove duplicate pressure values
df = df.drop_duplicates(subset="PRES")

# Interpolate temperature at OceanEmbed standard depths
argo_temperature = np.interp(
    target_depths,
    df["PRES"].values,
    df["TEMP"].values
)

# Create output table
result = pd.DataFrame({
    "depth_m": target_depths,
    "argo_temperature_C": argo_temperature
})

# Save
result.to_csv(output_file, index=False)

# Display
print("\nARGO temperature profile at OceanEmbed standard depths:\n")
print(result.to_string(index=False))

print("\nSaved to:")
print(output_file)