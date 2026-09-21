# OceanEmbed

### AI-Based Subsurface Ocean Temperature Reconstruction

OceanEmbed is a prototype deep-learning framework that reconstructs
subsurface ocean temperature profiles from seven surface ocean observations.

The project is developed as a prototype implementation for the
**Smart India Hackathon problem statement SIH26066**.

### What OceanEmbed Does

OceanEmbed takes the following surface ocean variables as input:

| Surface Variable | Description |
|---|---|
| SST | Sea Surface Temperature |
| SSS | Sea Surface Salinity |
| SSH / SLA | Sea Surface Height / Sea Level Anomaly |
| Current U | Eastward surface current |
| Current V | Northward surface current |
| Wind U | Eastward surface wind |
| Wind V | Northward surface wind |

The model encodes these seven variables into a compact
**16-dimensional representation** and decodes the representation into
a temperature profile at **15 standard depth levels**, from the surface
to 1000 m.

The web interface additionally accepts latitude and longitude to identify
the requested location.

### Prototype Status

> **Current status: Prototype / Proof of Concept**
>
> The present reconstruction model is trained on a controlled realistic
> synthetic dataset and demonstrated against a small real GLORYS12V1 subset.
> Large-scale training using synchronized real satellite-GLORYS observations
> and independent ARGO validation remain future development stages.

### Demonstration

The project includes a working web interface built with **FastAPI,
JavaScript and Chart.js** for generating and visualizing subsurface
temperature profiles.

![OceanEmbed real GLORYS demonstration](frontend/images/realistic_real_vs_prediction.png)

*Example comparison between real GLORYS12V1 temperature profiles and
OceanEmbed prototype predictions.*

### Key Output

OceanEmbed predicts temperature at:

```text
0 m, 5 m, 10 m, 20 m, 30 m,
50 m, 75 m, 100 m, 125 m, 150 m,
200 m, 300 m, 500 m, 700 m, 1000 m

## 1. Problem Statement

Direct observations of subsurface ocean temperature are spatially and
temporally limited. However, several surface ocean variables are available
from satellite and ocean observation products.

OceanEmbed explores whether these surface observations can be used to
reconstruct a depth-wise subsurface temperature profile using a compact
deep-learning model.

The intended application is reconstruction over the North Indian Ocean,
with the long-term target of producing daily temperature profiles on a
0.25° spatial grid.

---

## 2. Project Objective

The main objectives of OceanEmbed are:

1. Harmonize different ocean observation products.
2. Convert the observations into a common model-ready format.
3. Represent seven surface variables using a low-dimensional latent
   embedding.
4. Decode the embedding into a subsurface temperature profile.
5. Provide an interactive web interface for generating and visualizing
   temperature profiles.
6. Establish a pipeline that can later be extended to large-scale real
   satellite-GLORYS training and independent ARGO validation.

---

## 3. Input and Output

### Input

The current model accepts seven surface variables:

| Variable | Description |
|---|---|
| SST | Sea Surface Temperature |
| SSS | Sea Surface Salinity |
| SSH/SLA | Sea Surface Height / Sea Level Anomaly |
| Current U | Eastward surface current |
| Current V | Northward surface current |
| Wind U | Eastward surface wind |
| Wind V | Northward surface wind |

The web interface additionally accepts:

- Latitude
- Longitude

Latitude and longitude are currently used to describe the requested
location and are returned with the generated result. The current neural
network prediction itself uses the seven surface variables.

### Output

The model predicts temperature at the following 15 depth levels:

```text
0 m
5 m
10 m
20 m
30 m
50 m
75 m
100 m
125 m
150 m
200 m
300 m
500 m
700 m
1000 m

---

## 4. System Architecture

The current prototype follows this workflow:

```text
Surface Ocean Observations
            |
            v
+-----------------------------+
| Data Preprocessing          |
|                             |
| - Unit conversion           |
| - Temporal matching         |
| - Spatial matching         |
| - Interpolation             |
| - Standardization           |
+-------------+---------------+
              |
              v
+-----------------------------+
| OceanEmbed Encoder          |
|                             |
| 7 input variables           |
|       |                     |
|       v                     |
| 32-dimensional layer        |
|       |                     |
|       v                     |
| 16-dimensional embedding    |
+-------------+---------------+
              |
              v
+-----------------------------+
| OceanEmbed Decoder          |
|                             |
| 16-D embedding              |
|       |                     |
|       v                     |
| 15 temperature values       |
+-------------+---------------+
              |
              v
+-----------------------------+
| Subsurface Temperature      |
| Profile                     |
|                             |
| 0 m - 1000 m                |
+-------------+---------------+
              |
              v
+-----------------------------+
| Web Visualization           |
|                             |
| FastAPI + JavaScript        |
| Chart.js + Prediction Table |
+-----------------------------+

---

## 5. OceanEmbed Model

The current neural network uses an encoder-decoder architecture.

### Encoder

```text
7 inputs
   |
   v
Linear(7 -> 32)
   |
 ReLU
   |
   v
Linear(32 -> 16)
   |
   v
16-dimensional embedding

---

## 9. Model Performance

### 9.1 Held-Out Synthetic Test

The current OceanEmbed model achieved:

| Metric | Result |
|---|---:|
| MAE | 0.112 °C |
| RMSE | 0.149 °C |
| Bias | +0.003 °C |

These values represent performance on held-out realistic synthetic data.

They should not be interpreted as final real-ocean prediction accuracy.

### 9.2 Real GLORYS Demonstration

The trained model was additionally evaluated against four complete real
GLORYS demonstration samples.

| Metric | Result |
|---|---:|
| MAE | 0.967 °C |
| RMSE | 1.147 °C |
| Bias | -0.238 °C |

This evaluation is only a small demonstration and is not a statistically
representative real-world validation.

---

## 10. Real GLORYS Demonstration

The project includes real GLORYS12V1 temperature profiles processed through
the data pipeline.

The prototype also compares the real GLORYS profiles with predictions from
the current OceanEmbed model.

These figures are available in:

```text
frontend/images/real_glorys_profiles.png
frontend/images/realistic_real_vs_prediction.png

---

## 13. Project Structure

```text
OceanEmbed/
│
├── backend.py
├── embedding_model.py
├── README.md
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   │
│   └── images/
│       ├── real_glorys_profiles.png
│       └── realistic_real_vs_prediction.png
│
├── models/
│   └── oceanembed_realistic.pth
│
├── data/
│   ├── synthetic/
│   ├── synthetic_realistic/
│   ├── realistic_processed/
│   └── real_model_ready/
│
└── ...

---

## 14. Installation

The project uses a dedicated Python environment for its machine-learning
and ocean-data processing components.

Activate the project environment:

```powershell
conda activate copernicus_env