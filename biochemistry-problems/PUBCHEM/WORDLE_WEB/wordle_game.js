
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
    if (guess.length !== 5) return false;
    if (!/^[A-Z]{5}$/.test(guess)) return false;
    return wordList.indexOf(guess) !== -1;
}

function setupGame() {
    const dayKey = getUtcDayKey();
    const answer = getDailyWord(); // uppercase
    const maxGuesses = 6;

    renderSequence(answer, "peptide"); // from wordle_peptides.js
    renderStats();

    const form = document.getElementById("guess-form");
    const input = document.getElementById("guess");
    const message = document.getElementById("message");
    const board = document.getElementById("board");

    let guesses = [];
    let finished = false;

    form.addEventListener("submit", function (evt) {
        evt.preventDefault();
        if (finished) return;

                          let guess = input.value.trim().toUpperCase();
        if (!isValidGuess(guess, WORD_LIST)) {
            message.textContent = "Not a valid word.";
            return;
        }
        input.value = "";

        const result = scoreGuess(guess, answer);
        guesses.push({ guess: guess, result: result });
        renderBoard(board, guesses);

        if (result.every(function (x) { return x === "correct"; })) {
            message.textContent = "Correct.";
            updateStatsOnGameEnd(true, dayKey);
            renderStats();
            finished = true;
        } else if (guesses.length >= maxGuesses) {
            message.textContent = "Out of guesses. Answer was " + answer + ".";
            updateStatsOnGameEnd(false, dayKey);
            renderStats();
            finished = true;
        } else {
            message.textContent = "";
        }
    });
}

function renderBoard(container, guesses) {
    container.innerHTML = "";
    for (let i = 0; i < guesses.length; i += 1) {
        const row = document.createElement("div");
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

function updateLetterState(guess, result, letterState) {
    for (var i = 0; i < guess.length; i += 1) {
        var ch = guess[i];
        var res = result[i];
        var current = letterState[ch] || "unknown";

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
    var container = document.getElementById("keyboard");
    if (!container) {
        return;
    }
    container.innerHTML = "";

    var rows = [
        "QWERTYUIOP",
        "ASDFGHJKL",
        "ZXCVBNM"
    ];

    function createRow(letters, isBottom) {
        var rowEl = document.createElement("div");
        rowEl.className = "kb-row";

        if (isBottom) {
            var enterKey = document.createElement("button");
            enterKey.type = "button";
            enterKey.className = "kb-key wide";
            enterKey.textContent = "Enter";
            enterKey.dataset.key = "ENTER";
            rowEl.appendChild(enterKey);
        }

        for (var i = 0; i < letters.length; i += 1) {
            var ch = letters[i];
            var key = document.createElement("button");
            key.type = "button";

            var cls = "kb-key";
            if (INVALID_LETTERS[ch]) {
                cls += " invalid";
                key.disabled = true;
            } else {
                var state = letterState[ch];
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
            var backKey = document.createElement("button");
            backKey.type = "button";
            backKey.className = "kb-key wide";
            backKey.textContent = "?";
            backKey.dataset.key = "BACKSPACE";
            rowEl.appendChild(backKey);
        }

        return rowEl;
    }

    container.appendChild(createRow(rows[0], false));
    container.appendChild(createRow(rows[1], false));
    container.appendChild(createRow(rows[2], true));
}

