/* global initRDKitModule, RDKitModule, setupGame */

document.addEventListener("DOMContentLoaded", function () {
    var messageEl = document.getElementById("message");

    // Optional override via URL: ?seq=ACRID
    try {
        var params = new URLSearchParams(window.location.search);
        var overrideSeq = params.get("seq");
        if (overrideSeq) {
            window.WORDLE_OVERRIDE = overrideSeq.toUpperCase();
        }
    } catch (e) {
        console.error("URL parameter parse error", e);
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
            messageEl.textContent = "Error: setupGame is not defined in wordle_game.js.";
        }
    }).catch(function (e) {
        console.error("RDKit init failed", e);
        messageEl.textContent = "Error: RDKit could not be loaded.";
    });
});
