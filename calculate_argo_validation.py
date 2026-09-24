import numpy as np
import matplotlib.pyplot as plt

# Standard depths
depths = np.array([
    0, 5, 10, 20, 30, 50, 75, 100,
    125, 150, 200, 300, 500, 700, 1000
])

# ARGO observations
argo = np.array([
    28.532000,
    28.531500,
    28.533000,
    28.538000,
    28.702000,
    27.673000,
    22.343381,
    20.345000,
    18.030500,
    17.303000,
    14.865000,
    12.781524,
    11.688000,
    10.184000,
    7.952000
])

# OceanEmbed prediction
prediction = np.array([
    28.213,
    27.827,
    27.517,
    26.819,
    26.325,
    25.116,
    23.536,
    22.459,
    21.372,
    20.538,
    19.139,
    16.459,
    12.782,
    10.699,
    9.113
])

# Errors
error = prediction - argo

mae = np.mean(np.abs(error))
rmse = np.sqrt(np.mean(error ** 2))
bias = np.mean(error)

print()
print("======================================")
print("ARGO VALIDATION - ONE PROFILE")
print("======================================")
print(f"MAE  : {mae:.4f} C")
print(f"RMSE : {rmse:.4f} C")
print(f"Bias : {bias:.4f} C")

print()
print("Depth (m)   ARGO (C)   Prediction (C)   Error (C)")
print("---------------------------------------------------")

for d, a, p, e in zip(depths, argo, prediction, error):
    print(f"{d:>5}      {a:>7.3f}       {p:>7.3f}       {e:>7.3f}")

# Save numerical results
results = np.column_stack([
    depths,
    argo,
    prediction,
    error
])

np.savetxt(
    "data/argo_validation/argo_comparison.csv",
    results,
    delimiter=",",
    header="depth_m,argo_temp_C,predicted_temp_C,error_C",
    comments=""
)

# Plot
plt.figure(figsize=(7, 8))

plt.plot(
    argo,
    depths,
    marker="o",
    label="ARGO observation"
)

plt.plot(
    prediction,
    depths,
    marker="s",
    label="OceanEmbed prediction"
)

plt.gca().invert_yaxis()

plt.xlabel("Temperature (C)")
plt.ylabel("Depth (m)")
plt.title("OceanEmbed vs Independent ARGO Profile")

plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()

plt.savefig(
    "frontend/images/argo_validation_profile.png",
    dpi=200
)

plt.show()

print()
print("Saved:")
print("data/argo_validation/argo_comparison.csv")
print("frontend/images/argo_validation_profile.png")
