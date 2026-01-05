/* global initRDKitModule, RDKitModule, setupGame */

document.addEventListener("DOMContentLoaded", function () {
    var messageEl = document.getElementById("message");

    // Help button scrolls to instructions
    var helpButton = document.getElementById("help-button");
    var details = document.getElementById("instructions-details");
    if (helpButton && details) {
        helpButton.addEventListener("click", function () {
            details.open = true;
            details.scrollIntoView({ behavior: "smooth" });
        });
    }

    if (typeof initRDKitModule !== "function") {
        messageEl.textContent = "Error: initRDKitModule is not available.";
        return;
    }

    initRDKitModule().then(function (instance) {
        window.RDKitModule = instance;
        console.log("RDKit " + RDKitModule.version());
        if (typeof setupGame === "function") {
            setupGame();
        } else {
            messageEl.textContent = "Error: setupGame is not defined in peptidyle_game.js.";
        }
    }).catch(function (e) {
        console.error("RDKit init failed", e);
        messageEl.textContent = "Error: RDKit could not be loaded.";
    });
});
