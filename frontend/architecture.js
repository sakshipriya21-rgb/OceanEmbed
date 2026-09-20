// --------------------------------------------------
// OceanEmbed - System Architecture
// --------------------------------------------------

document.addEventListener("DOMContentLoaded", function () {

    const architectureBoxes =
        document.querySelectorAll(".architecture-box");

    architectureBoxes.forEach(function (box) {

        box.addEventListener("click", function () {

            box.classList.toggle("selected");

        });

    });

});