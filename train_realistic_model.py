import numpy as np
import torch
import torch.nn as nn
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from embedding_model import OceanEmbed

# Create output folders
os.makedirs("data/realistic_processed", exist_ok=True)
os.makedirs("models", exist_ok=True)

# Load realistic synthetic dataset
X = np.load("data/synthetic_realistic/X.npy")
Y = np.load("data/synthetic_realistic/Y.npy")
depths = np.load("data/synthetic_realistic/depths.npy")

# Split 70/15/15
X_train, X_temp, Y_train, Y_temp = train_test_split(
    X, Y, test_size=0.30, random_state=42
)

X_val, X_test, Y_val, Y_test = train_test_split(
    X_temp, Y_temp, test_size=0.50, random_state=42
)

# Scale using training data only
X_scaler = StandardScaler()
Y_scaler = StandardScaler()

X_train_s = X_scaler.fit_transform(X_train)
X_val_s = X_scaler.transform(X_val)
X_test_s = X_scaler.transform(X_test)

Y_train_s = Y_scaler.fit_transform(Y_train)
Y_val_s = Y_scaler.transform(Y_val)
Y_test_s = Y_scaler.transform(Y_test)

# Convert to tensors
Xtr = torch.tensor(X_train_s, dtype=torch.float32)
Ytr = torch.tensor(Y_train_s, dtype=torch.float32)

Xv = torch.tensor(X_val_s, dtype=torch.float32)
Yv = torch.tensor(Y_val_s, dtype=torch.float32)

# Model
model = OceanEmbed()

criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Training
for epoch in range(1, 201):

    model.train()

    optimizer.zero_grad()

    output = model(Xtr)

    loss = criterion(output, Ytr)

    loss.backward()

    optimizer.step()

    if epoch == 1 or epoch % 25 == 0:

        model.eval()

        with torch.no_grad():
            val_output = model(Xv)
            val_loss = criterion(val_output, Yv)

        print(
            f"Epoch {epoch:3d} | "
            f"Train Loss: {loss.item():.6f} | "
            f"Val Loss: {val_loss.item():.6f}"
        )

# Save model and scalers
torch.save(
    model.state_dict(),
    "models/oceanembed_realistic.pth"
)

joblib.dump(
    X_scaler,
    "data/realistic_processed/X_scaler.pkl"
)

joblib.dump(
    Y_scaler,
    "data/realistic_processed/Y_scaler.pkl"
)

np.save(
    "data/realistic_processed/X_test.npy",
    X_test_s
)

np.save(
    "data/realistic_processed/Y_test.npy",
    Y_test_s
)

np.save(
    "data/realistic_processed/depths.npy",
    depths
)

# Test evaluation
model.eval()

with torch.no_grad():
    pred_scaled = model(
        torch.tensor(X_test_s, dtype=torch.float32)
    ).numpy()

pred = Y_scaler.inverse_transform(pred_scaled)

mae = np.mean(np.abs(pred - Y_test))
rmse = np.sqrt(np.mean((pred - Y_test) ** 2))
bias = np.mean(pred - Y_test)

print("\n======================================")
print("REALISTIC MODEL TEST RESULTS")
print("======================================")
print(f"MAE  : {mae:.4f} C")
print(f"RMSE : {rmse:.4f} C")
print(f"Bias : {bias:.4f} C")

print("\nModel saved:")
print("models/oceanembed_realistic.pth")

print("\nScalers saved:")
print("data/realistic_processed/")
