from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import numpy as np
import torch
import joblib

from embedding_model import OceanEmbed


# --------------------------------------------------
# Create FastAPI application
# --------------------------------------------------

app = FastAPI()


# --------------------------------------------------
# Allow frontend to communicate with backend
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Load the trained OceanEmbed model
# --------------------------------------------------

model = OceanEmbed()

model.load_state_dict(
    torch.load(
        "models/oceanembed_realistic.pth",
        map_location="cpu"
    )
)

model.eval()


# --------------------------------------------------
# Load the data scalers
# --------------------------------------------------

X_scaler = joblib.load(
    "data/realistic_processed/X_scaler.pkl"
)

Y_scaler = joblib.load(
    "data/realistic_processed/Y_scaler.pkl"
)


# --------------------------------------------------
# Define the input data structure
# --------------------------------------------------

class OceanInput(BaseModel):

    latitude: float
    longitude: float

    sst: float
    sss: float
    ssh: float

    current_u: float
    current_v: float

    wind_u: float
    wind_v: float


# --------------------------------------------------
# Home route
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "OceanEmbed backend is running"
    }


# --------------------------------------------------
# Prediction route
# --------------------------------------------------

@app.post("/predict")
def predict(data: OceanInput):

    # Create input array in the same order
    # used during model training

    X = np.array([[
        data.sst,
        data.sss,
        data.ssh,
        data.current_u,
        data.current_v,
        data.wind_u,
        data.wind_v
    ]])


    # Apply the same normalization used during training

    X_scaled = X_scaler.transform(X)


    # Convert NumPy array to PyTorch tensor

    X_tensor = torch.tensor(
        X_scaled,
        dtype=torch.float32
    )


    # Generate prediction

    with torch.no_grad():

        prediction_scaled = model(X_tensor)


    # Convert PyTorch tensor to NumPy

    prediction_scaled = prediction_scaled.numpy()


    # Convert prediction back to temperature units

    prediction = Y_scaler.inverse_transform(
        prediction_scaled
    )


    # Standard depth levels

    depths = [
        0,
        5,
        10,
        20,
        30,
        50,
        75,
        100,
        125,
        150,
        200,
        300,
        500,
        700,
        1000
    ]


    # Convert prediction into a normal Python list

    temperatures = prediction[0].tolist()


    # Return the result to JavaScript

    return {
        "message": "Temperature profile generated successfully",
        "latitude": data.latitude,
        "longitude": data.longitude,
        "depths": depths,
        "temperatures": temperatures
    }
