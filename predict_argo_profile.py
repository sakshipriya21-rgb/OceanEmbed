import torch
import numpy as np
import joblib
from embedding_model import OceanEmbed

# Load model
model = OceanEmbed()

model.load_state_dict(
    torch.load(
        "models/oceanembed_realistic.pth",
        map_location="cpu"
    )
)

model.eval()

# Load the SAME scalers used during training
X_scaler = joblib.load(
    "data/realistic_processed/X_scaler.pkl"
)

Y_scaler = joblib.load(
    "data/realistic_processed/Y_scaler.pkl"
)

# ARGO surface observations
X = np.array([[
    28.185993106276896,
    35.5871693984375,
    0.07584280320000024,
    -0.0661539679999999,
    -0.1261565599999994,
    8.053875200000014,
    3.9291404800000054
]], dtype=np.float32)

# Apply training input normalization
X_scaled = X_scaler.transform(X)

# OceanEmbed prediction
with torch.no_grad():

    prediction_scaled = model(
        torch.tensor(X_scaled, dtype=torch.float32)
    ).numpy()

# Convert back to Celsius
prediction = Y_scaler.inverse_transform(
    prediction_scaled
)

# Standard depths
depths = np.load(
    "data/realistic_processed/depths.npy"
)

print()
print("OceanEmbed prediction for ARGO location")
print("Latitude: 14.304 N")
print("Longitude: 72.761 E")
print("Date: 2020-08-02")

print()
print("Depth (m)   Predicted Temp (C)")
print("--------------------------------")

for depth, temp in zip(depths, prediction[0]):

    print(
        f"{depth:>5.0f}       {temp:.3f}"
    )
