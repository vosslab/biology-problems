// wordle_stats.js

const STATS_KEY = "wordle_peptides_stats_v1";

function loadStats() {
    const raw = window.localStorage.getItem(STATS_KEY);
    if (!raw) {
        return {
            gamesPlayed: 0,
            wins: 0,
            currentStreak: 0,
            maxStreak: 0,
            lastDayKey: null,
            lastResult: null
        };
    }
    try {
        return JSON.parse(raw);
    } catch (_) {
        return {
            gamesPlayed: 0,
            wins: 0,
            currentStreak: 0,
            maxStreak: 0,
            lastDayKey: null,
            lastResult: null
        };
    }
}

function saveStats(stats) {
    window.localStorage.setItem(STATS_KEY, JSON.stringify(stats));
}

function previousDayKey(dayKey) {
    const d = new Date(dayKey + "T00:00:00Z");
    d.setUTCDate(d.getUTCDate() - 1);
    return d.toISOString().slice(0, 10);
}

function updateStatsOnGameEnd(win, dayKey) {
    const stats = loadStats();

    if (stats.lastDayKey !== dayKey) {
        stats.gamesPlayed += 1;
    }

    if (win) {
        if (stats.lastDayKey === previousDayKey(dayKey) && stats.lastResult === "win") {
            stats.currentStreak += 1;
        } else {
            stats.currentStreak = 1;
        }
        stats.wins += 1;
    } else {
        stats.currentStreak = 0;
    }

    if (stats.currentStreak > stats.maxStreak) {
        stats.maxStreak = stats.currentStreak;
    }

    stats.lastDayKey = dayKey;
    stats.lastResult = win ? "win" : "loss";
    saveStats(stats);
}

function renderStats() {
    const stats = loadStats();
    const el = document.getElementById("stats");
    if (!el) {
        return;
    }
    el.textContent =
    "Games: " + stats.gamesPlayed +
    "   Wins: " + stats.wins +
    "   Streak: " + stats.currentStreak +
    "   Max streak: " + stats.maxStreak;
}
