"use strict";

// Letters not allowed for amino acid guesses
const INVALID_LETTERS = {
    B: true,
    X: true,
    Z: true,
    J: true,
    O: true,
    U: true,
    P: true  // Proline excluded by design
};

// Simple letter state for keyboard colouring
const LETTER_STATE = {};
const MAX_GUESSES = 3;

(function initLetterState() {
    const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    for (let i = 0; i < letters.length; i += 1) {
        LETTER_STATE[letters[i]] = "unknown";
    }
}());

//=================================================
// Scoring and validation
//=================================================
function scoreGuess(guess, answer) {
    const len = answer.length;
    const result = new Array(len).fill("absent");
    const counts = {};

    // first pass: mark correct and count others
    for (let i = 0; i < len; i += 1) {
        const a = answer[i];
        const g = guess[i];
        if (g === a) {
            result[i] = "correct";
        } else {
            counts[a] = (counts[a] || 0) + 1;
        }
    }

    // second pass: present vs absent
    for (let i = 0; i < len; i += 1) {
        if (result[i] !== "absent") {
            continue;
        }
        const g = guess[i];
        if (counts[g] > 0) {
            result[i] = "present";
            counts[g] -= 1;
        }
    }

    return result; // array of "correct" | "present" | "absent"
}

// peptide specific validator: any valid amino acid sequence of length 5
function isValidPeptideGuess(guess) {
    if (guess.length !== 5) {
        return false;
    }
    if (!/^[A-Z]{5}$/.test(guess)) {
        return false;
    }
    for (let i = 0; i < guess.length; i += 1) {
        const ch = guess[i];
        if (INVALID_LETTERS[ch]) {
            return false;
        }
        if (!aminoAcidMapping[ch]) {
            return false;
        }
    }
    return true;
}

//=================================================
// Board rendering: show previous guesses + currentGuess + empty rows
//=================================================
function renderBoard(container, guesses, currentGuess, maxRows) {
    const rows = maxRows || 3;
    const wordLen = 5;

    container.innerHTML = "";

    for (let rowIndex = 0; rowIndex < rows; rowIndex += 1) {
        const row = document.createElement("div");
        row.className = "row";

        let text = "";
        let result = null;
        let state = "empty";

        if (rowIndex < guesses.length) {
            // past guess, already scored
            text = guesses[rowIndex].guess;
            result = guesses[rowIndex].result;
        } else if (rowIndex === guesses.length && currentGuess) {
            // active guess being typed
            text = currentGuess;
            state = "pending";
        }

        for (let col = 0; col < wordLen; col += 1) {
            const cell = document.createElement("span");
            let ch = text[col] || "";
            cell.textContent = ch;

            let cls = "cell";
            if (result) {
                cls += " " + result[col]; // correct | present | absent
            } else if (state === "pending" && ch) {
                cls += " pending";
            } else {
                cls += " empty";
            }
            cell.className = cls;
            row.appendChild(cell);
        }

        container.appendChild(row);
    }
}

//=================================================
// Keyboard state and rendering
//=================================================
function updateLetterState(guess, result, letterState) {
    for (let i = 0; i < guess.length; i += 1) {
        const ch = guess[i];
        const res = result[i];
        const current = letterState[ch] || "unknown";

        if (res === "correct") {
            letterState[ch] = "correct";
        } else if (res === "present") {
            if (current !== "correct") {
                letterState[ch] = "present";
            }
        } else if (res === "absent") {
            if (current === "unknown") {
                letterState[ch] = "absent";
            }
        }
    }
}

function renderKeyboard(letterState) {
    const container = document.getElementById("keyboard");
    if (!container) {
        return;
    }
    container.innerHTML = "";

    const rows = [
        "QWERTYUIOP",
        "ASDFGHJKL",
        "ZXCVBNM"
    ];

    function createRow(letters, isBottom) {
        const rowEl = document.createElement("div");
        rowEl.className = "kb-row";

        if (isBottom) {
            const enterKey = document.createElement("button");
            enterKey.type = "button";
            enterKey.className = "kb-key wide";
            enterKey.textContent = "Enter";
            enterKey.dataset.key = "ENTER";
            rowEl.appendChild(enterKey);
        }

        for (let i = 0; i < letters.length; i += 1) {
            const ch = letters[i];
            const key = document.createElement("button");
            key.type = "button";

            let cls = "kb-key";
            if (INVALID_LETTERS[ch]) {
                cls += " invalid";
                key.disabled = true;
            } else {
                const state = letterState[ch];
                if (state === "correct") {
                    cls += " correct";
                } else if (state === "present") {
                    cls += " present";
                } else if (state === "absent") {
                    cls += " absent";
                }
            }
            key.className = cls;
            key.textContent = ch;
            key.dataset.key = ch;
            rowEl.appendChild(key);
        }

        if (isBottom) {
            const backKey = document.createElement("button");
            backKey.type = "button";
            backKey.className = "kb-key wide";
            backKey.textContent = "DEL";
            backKey.dataset.key = "BACKSPACE";
            rowEl.appendChild(backKey);
        }

        return rowEl;
    }

    container.appendChild(createRow(rows[0], false));
    container.appendChild(createRow(rows[1], false));
    container.appendChild(createRow(rows[2], true));
}

//=================================================
// Toast messages
//=================================================
function showToast(text, durationMs) {
    const container = document.getElementById("toast-container");
    if (!container) {
        return;
    }
    const d = durationMs || 1500;

    const el = document.createElement("div");
    el.className = "toast";
    el.textContent = text;
    container.appendChild(el);

    void el.offsetWidth;
    el.classList.add("show");

    setTimeout(function () {
        el.classList.remove("show");
        setTimeout(function () {
            if (el.parentNode === container) {
                container.removeChild(el);
            }
        }, 200);
    }, d);
}

//=================================================
// Game setup and main loop
//=================================================
function setupGame() {
    const dayKey = getUtcDayKey();
    let answer = getDailyWord(); // uppercase

    // Optional override from URL: ?seq=ACRID
    if (window.PEPTIDYL_OVERRIDE) {
        answer = window.PEPTIDYL_OVERRIDE.toUpperCase();
    }

    const maxGuesses = MAX_GUESSES;

    renderSequence(answer, "peptide"); // from peptidyl_peptides.js
    renderStats();

    const form = document.getElementById("guess-form");
    const input = document.getElementById("guess");
    const message = document.getElementById("message");
    const board = document.getElementById("board");

    let guesses = [];
    let finished = false;
    let currentGuess = "";

    // keep hidden input in sync but it is not shown
    input.value = "";

    renderBoard(board, guesses, currentGuess, maxGuesses);
    renderKeyboard(LETTER_STATE);

    function submitGuess() {
        if (finished) {
            return;
        }
        const guess = currentGuess.toUpperCase();

        if (guess.length !== 5) {
            showToast("Guess must be 5 letters.");
            return;
        }
        if (!isValidPeptideGuess(guess)) {
            showToast("Not a valid peptide sequence.");
            return;
        }

        const result = scoreGuess(guess, answer);
        guesses.push({ guess: guess, result: result });
        currentGuess = "";
        input.value = "";
        renderBoard(board, guesses, currentGuess, maxGuesses);
        updateLetterState(guess, result, LETTER_STATE);
        renderKeyboard(LETTER_STATE);

        if (result.every(function (x) { return x === "correct"; })) {
            message.textContent = "Correct.";
            showToast("Correct.");
            updateStatsOnGameEnd(true, dayKey);
            renderStats();
            finished = true;
            return;
        }
        if (guesses.length >= maxGuesses) {
            message.textContent = "Out of guesses. Answer was " + answer + ".";
            showToast("Answer was " + answer + ".");
            updateStatsOnGameEnd(false, dayKey);
            renderStats();
            finished = true;
            return;
        }
        message.textContent = "";
    }

    // Hidden form, in case someone actually hits Enter in it
    form.addEventListener("submit", function (evt) {
        evt.preventDefault();
        submitGuess();
    });

    // On screen keyboard
    const keyboard = document.getElementById("keyboard");
    if (keyboard) {
        keyboard.addEventListener("click", function (evt) {
            const target = evt.target;
            if (!target.classList.contains("kb-key")) {
                return;
            }
            const k = target.dataset.key;
            if (!k) {
                return;
            }
            if (k === "ENTER") {
                submitGuess();
            } else if (k === "BACKSPACE") {
                currentGuess = currentGuess.slice(0, -1);
                input.value = currentGuess;
                renderBoard(board, guesses, currentGuess, maxGuesses);
            } else if (/^[A-Z]$/.test(k)) {
                if (INVALID_LETTERS[k]) {
                    return;
                }
                if (!finished && currentGuess.length < 5) {
                    currentGuess += k;
                    input.value = currentGuess;
                    renderBoard(board, guesses, currentGuess, maxGuesses);
                }
            }
        });
    }

    // Physical keyboard
    document.addEventListener("keydown", function (evt) {
        if (!input || finished) {
            return;
        }
        // do not eat browser shortcuts like Cmd+R, Ctrl+R
        if (evt.metaKey || evt.ctrlKey || evt.altKey) {
            return;
        }
        const key = evt.key;
        if (key === "Enter") {
            evt.preventDefault();
            submitGuess();
        } else if (key === "Backspace") {
            evt.preventDefault();
            currentGuess = currentGuess.slice(0, -1);
            input.value = currentGuess;
            renderBoard(board, guesses, currentGuess, maxGuesses);
        } else if (/^[a-zA-Z]$/.test(key)) {
            const ch = key.toUpperCase();
            if (INVALID_LETTERS[ch]) {
                evt.preventDefault();
                return;
            }
            if (currentGuess.length < 5) {
                currentGuess += ch;
                input.value = currentGuess;
                renderBoard(board, guesses, currentGuess, maxGuesses);
                evt.preventDefault();
            }
        }
    });
}
