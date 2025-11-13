// peptidyle_stats.js

const STATS_KEY = "peptidyle_stats_v1";

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

    // If we already recorded a result for this day, do not double count
    if (stats.lastDayKey === dayKey && stats.lastResult !== null) {
        return;
    }

    // New result for this day
    stats.gamesPlayed += 1;

    if (win) {
        // Streak logic: consecutive winning days
        if (stats.lastDayKey === previousDayKey(dayKey) && stats.lastResult === "win") {
            stats.currentStreak += 1;
        } else {
            stats.currentStreak = 1;
        }
        stats.wins += 1;
        stats.lastResult = "win";
    } else {
        stats.currentStreak = 0;
        stats.lastResult = "loss";
    }

    if (stats.currentStreak > stats.maxStreak) {
        stats.maxStreak = stats.currentStreak;
    }

    stats.lastDayKey = dayKey;
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
