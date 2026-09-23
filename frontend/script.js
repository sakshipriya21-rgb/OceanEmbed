// Get the Generate Temperature Profile button
const predictButton = document.getElementById("predict-button");


// Keep track of the chart
let temperatureChart = null;


// Run this code when the button is clicked
predictButton.addEventListener("click", async function () {

    // Read the values entered in the form
    const latitude = parseFloat(document.getElementById("latitude").value);
    const longitude = parseFloat(document.getElementById("longitude").value);

    const sst = parseFloat(document.getElementById("sst").value);
    const sss = parseFloat(document.getElementById("sss").value);
    const ssh = parseFloat(document.getElementById("ssh").value);

    const currentU = parseFloat(document.getElementById("current-u").value);
    const currentV = parseFloat(document.getElementById("current-v").value);

    const windU = parseFloat(document.getElementById("wind-u").value);
    const windV = parseFloat(document.getElementById("wind-v").value);

    // Check that all values are valid numbers
const values = [
    latitude,
    longitude,
    sst,
    sss,
    ssh,
    currentU,
    currentV,
    windU,
    windV
];

if (values.some(function(value) {
    return !Number.isFinite(value);
})) {

    document.getElementById("prediction-status").innerText =
        "Please enter valid values for all observations.";

    return;
}


// Check the intended North Indian Ocean study region
if (latitude < 5 || latitude > 30) {

    document.getElementById("prediction-status").innerText =
        "Latitude should be between 5°N and 30°N.";

    return;
}


if (longitude < 45 || longitude > 105) {

    document.getElementById("prediction-status").innerText =
        "Longitude should be between 45°E and 105°E.";

    return;
}


// Basic physical sanity checks
if (sst < 0 || sst > 40) {

    document.getElementById("prediction-status").innerText =
        "Please enter a reasonable SST value.";

    return;
}


if (sss < 0 || sss > 40) {

    document.getElementById("prediction-status").innerText =
        "Please enter a reasonable SSS value.";

    return;
}
    // Show status message
    document.getElementById("prediction-status").innerText =
        "Generating temperature profile...";
    predictButton.disabled = true;

predictButton.innerText = "Generating...";

    try {

        // Send observations to the FastAPI backend
        const response = await fetch("http://127.0.0.1:8000/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                latitude: latitude,
                longitude: longitude,

                sst: sst,
                sss: sss,
                ssh: ssh,

                current_u: currentU,
                current_v: currentV,

                wind_u: windU,
                wind_v: windV
            })
        });


        // Check whether the backend returned an error
        if (!response.ok) {
            throw new Error("Backend returned an error.");
        }


        // Convert backend response into JavaScript data
        const result = await response.json();


        // Show success message
        document.getElementById("prediction-status").innerText =
            result.message;
        predictButton.disabled = false;

predictButton.innerText = "Generate Temperature Profile";

        // Draw the temperature-depth graph
        drawTemperatureProfile(
            result.depths,
            result.temperatures
        );
        drawPredictionTable(
        result.depths,
        result.temperatures
        );

        // Print the prediction in the browser console
        console.log("Depths:", result.depths);
        console.log("Temperatures:", result.temperatures);

    }


    catch (error) {

        console.error("Error:", error);

        document.getElementById("prediction-status").innerText =
            "Unable to generate temperature profile.";
        predictButton.disabled = false;

predictButton.innerText = "Generate Temperature Profile";
    }

});


// --------------------------------------------------
// Draw temperature-depth profile
// --------------------------------------------------

function drawTemperatureProfile(depths, temperatures) {

    // Get the canvas where the graph will be drawn
    const canvas = document.getElementById(
        "temperature-profile-chart"
    );


    // If a previous chart exists, remove it
    if (temperatureChart !== null) {
        temperatureChart.destroy();
    }


    // Create coordinate pairs:
    // x = temperature
    // y = depth
    const profileData = depths.map(function (depth, index) {

        return {
            x: temperatures[index],
            y: depth
        };

    });


    // Create the temperature-depth profile
    temperatureChart = new Chart(canvas, {

        type: "scatter",

        data: {

            datasets: [
                {
                    label: "Predicted Temperature (°C)",

                    data: profileData,

                    showLine: true,

                    borderWidth: 2,

                    pointRadius: 4,

                    pointHoverRadius: 6,

                    tension: 0.1
                }
            ]
        },


        options: {

            responsive: true,

            maintainAspectRatio: false,


            scales: {

                // Temperature is now the horizontal axis
                x: {

                    title: {
                        display: true,
                        text: "Temperature (°C)"
                    }
                },


                // Depth is now the vertical axis
                y: {

                    title: {
                        display: true,
                        text: "Depth (m)"
                    },

                    // Ocean depth increases downward
                    reverse: true,

                    min: 0,

                    max: 1000
                }

            }

        }

    });
}
// --------------------------------------------------
// Display numerical prediction table
// --------------------------------------------------

function drawPredictionTable(depths, temperatures) {

    // Find the table body
    const tableBody = document.getElementById(
        "prediction-table-body"
    );


    // Clear any previous results
    tableBody.innerHTML = "";


    // Add one row for every depth
    depths.forEach(function (depth, index) {

        const row = document.createElement("tr");


        // Depth column
        const depthCell = document.createElement("td");

        depthCell.innerText = depth;

        row.appendChild(depthCell);


        // Temperature column
        const temperatureCell = document.createElement("td");

        temperatureCell.innerText =
            temperatures[index].toFixed(2);

        row.appendChild(temperatureCell);


        // Add row to table
        tableBody.appendChild(row);

    });

}
// --------------------------------------------------
// Spatial temperature map controls
// --------------------------------------------------

function updateSpatialMaps(depth) {

    const realMap = document.getElementById("real-spatial-map");
    const predictionMap = document.getElementById("prediction-spatial-map");
    const errorMap = document.getElementById("spatial-error-map");
    const rmseText = document.getElementById("spatial-rmse");

    const spatialRMSE = {
        0: 0.2580,
        100: 0.4585,
        200: 1.4982,
        500: 0.2575,
        1000: 0.5686
    };

    if (realMap) {
        realMap.src =
            "images/spatial_demo/real_glorys_" +
            depth +
            "m.png?v=" +
            Date.now();
    }

    if (predictionMap) {
        predictionMap.src =
            "images/spatial_demo/oceanembed_" +
            depth +
            "m.png?v=" +
            Date.now();
    }

    if (errorMap) {
        errorMap.src =
            "images/spatial_demo/error_" +
            depth +
            "m.png?v=" +
            Date.now();
    }

    if (rmseText) {
        rmseText.innerText =
            "Spatial RMSE: " +
            spatialRMSE[depth].toFixed(4) +
            " °C";
    }
}
document.addEventListener("DOMContentLoaded", function () {

    const spatialDepth = document.getElementById("spatial-depth");

    if (spatialDepth) {
        spatialDepth.addEventListener("change", function () {

            updateSpatialMaps(this.value);

        });
    }

});