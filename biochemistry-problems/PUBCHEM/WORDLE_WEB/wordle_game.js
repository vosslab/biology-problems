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

(function initLetterState() {
    var letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    for (var i = 0; i < letters.length; i += 1) {
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

function isValidGuess(guess, wordList) {
    if (guess.length !== 5) {
        return false;
    }
    if (!/^[A-Z]{5}$/.test(guess)) {
        return false;
    }
    return wordList.indexOf(guess) !== -1;
}

function isValidPeptideGuess(guess) {
    if (guess.length !== 5) {
        return false;
    }
    if (!/^[A-Z]{5}$/.test(guess)) {
        return false;
    }
    for (let i = 0; i < guess.length; i += 1) {
        const ch = guess[i];
        // block letters you decided are not allowed in this model
        if (INVALID_LETTERS[ch]) {
            return false;
        }
        // require that there is an amino acid mapping
        if (!aminoAcidMapping[ch]) {
            return false;
        }
    }
    return true;
}

//=================================================
// Board rendering
//=================================================
function renderBoard(container, guesses) {
    container.innerHTML = "";
    for (let i = 0; i < guesses.length; i += 1) {
        const row = document.createElement("div");
        row.className = "row";
        const item = guesses[i];
        for (let j = 0; j < item.guess.length; j += 1) {
            const cell = document.createElement("span");
            cell.textContent = item.guess[j];
            const status = item.result[j]; // "correct" | "present" | "absent"
            cell.className = "cell " + status;
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

    // force layout so transition applies
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
    if (window.WORDLE_OVERRIDE) {
        answer = window.WORDLE_OVERRIDE.toUpperCase();
    }

    const maxGuesses = 6;

    renderSequence(answer, "peptide"); // from wordle_peptides.js
    renderStats();

    const form = document.getElementById("guess-form");
    const input = document.getElementById("guess");
    const message = document.getElementById("message");
    const board = document.getElementById("board");

    let guesses = [];
    let finished = false;

    renderBoard(board, guesses);
    renderKeyboard(LETTER_STATE);

    function submitGuessFromInput() {
        if (finished) {
            return;
        }
        let guess = input.value.trim().toUpperCase();

        if (guess.length !== 5) {
            showToast("Guess must be 5 letters.");
            return;
        }
        if (!isValidPeptideGuess(guess, WORD_LIST)) {
            showToast("Not a valid word.");
            return;
        }
        input.value = "";

        const result = scoreGuess(guess, answer);
        guesses.push({ guess: guess, result: result });
        renderBoard(board, guesses);
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

    // Hidden form still handles Enter
    form.addEventListener("submit", function (evt) {
        evt.preventDefault();
        submitGuessFromInput();
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
                submitGuessFromInput();
            } else if (k === "BACKSPACE") {
                input.value = input.value.slice(0, -1);
            } else if (/^[A-Z]$/.test(k)) {
                if (INVALID_LETTERS[k]) {
                    return;
                }
                if (!finished && input.value.length < 5) {
                    input.value += k;
                }
            }
        });
    }

    // Physical keyboard
    document.addEventListener("keydown", function (evt) {
        if (!input || finished) {
            return;
        }

        // ignore browser shortcuts: Cmd, Ctrl, Alt etc.
        if (evt.metaKey || evt.ctrlKey || evt.altKey) {
            return;
        }

        const key = evt.key;
        if (key === "Enter") {
            evt.preventDefault();
            submitGuessFromInput();
        } else if (key === "Backspace") {
            evt.preventDefault();
            input.value = input.value.slice(0, -1);
        } else if (/^[a-zA-Z]$/.test(key)) {
            const ch = key.toUpperCase();
            if (INVALID_LETTERS[ch]) {
                evt.preventDefault();
                return;
            }
            if (input.value.length < 5) {
                input.value += ch;
                evt.preventDefault();
            }
        }
    });
}
