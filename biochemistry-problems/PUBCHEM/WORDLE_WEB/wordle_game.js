
// 5-letter valid "pentapeptide" words
const WORD_LIST = [
    // paste your 898 words here
    'ACRID', 'ADAGE', 'ADMIN', 'ADMIT', 'AFIRE', 'AFTER', 'AGAIN', 'AGATE', 'AGENT', 'AGILE',
'AGING', 'AGREE', 'AHEAD', 'AIDER', 'AISLE', 'ALARM', 'ALERT', 'ALGAE', 'ALIEN', 'ALIGN',
'ALIKE', 'ALIVE', 'ALLAY', 'ALLEY', 'ALTAR', 'ALTER', 'AMASS', 'AMEND', 'AMISS', 'AMITY',
'ANGEL', 'ANGER', 'ANGLE', 'ANGRY', 'ANGST', 'ANIME', 'ANKLE', 'ANTIC', 'ANVIL', 'ARENA',
'ARISE', 'ARRAY', 'ARTSY', 'ASHEN', 'ASIDE', 'ASKEW', 'ASSAY', 'ASSET', 'ATTIC', 'AVAIL',
'AVERT', 'AVIAN', 'AWAIT', 'AWAKE', 'AWARD', 'AWARE', 'AWASH', 'CACHE', 'CACTI', 'CADDY',
'CADET', 'CAGEY', 'CAIRN', 'CAMEL', 'CANAL', 'CANDY', 'CANNY', 'CARAT', 'CARRY', 'CARVE',
'CASTE', 'CATCH', 'CATER', 'CATTY', 'CAVIL', 'CEASE', 'CEDAR', 'CHAFE', 'CHAFF', 'CHAIN',
'CHAIR', 'CHALK', 'CHANT', 'CHARD', 'CHARM', 'CHART', 'CHASE', 'CHASM', 'CHEAT', 'CHECK',
'CHEEK', 'CHEER', 'CHESS', 'CHEST', 'CHICK', 'CHIDE', 'CHIEF', 'CHILD', 'CHILI', 'CHILL',
'CHIME', 'CHINA', 'CIDER', 'CIGAR', 'CINCH', 'CIRCA', 'CIVIC', 'CIVIL', 'CLACK', 'CLAIM',
'CLANG', 'CLANK', 'CLASH', 'CLASS', 'CLEAN', 'CLEAR', 'CLEAT', 'CLEFT', 'CLERK', 'CLICK',
'CLIFF', 'CLING', 'CLINK', 'CRACK', 'CRAFT', 'CRANE', 'CRANK', 'CRASH', 'CRASS', 'CRATE',
'CRAVE', 'CRAWL', 'CREAK', 'CREAM', 'CREED', 'CREEK', 'CREME', 'CRESS', 'CREST', 'CRICK',
'CRIED', 'CRIER', 'CRIME', 'CYCLE', 'CYNIC', 'DADDY', 'DAILY', 'DAIRY', 'DAISY', 'DALLY',
'DANCE', 'DANDY', 'DEALT', 'DEATH', 'DECAL', 'DECAY', 'DECRY', 'DEFER', 'DEIGN', 'DEITY',
'DELAY', 'DELTA', 'DELVE', 'DENIM', 'DENSE', 'DETER', 'DEVIL', 'DIARY', 'DICEY', 'DIGIT',
'DILLY', 'DIMLY', 'DINER', 'DINGY', 'DIRGE', 'DIRTY', 'DITCH', 'DITTY', 'DIVER', 'DRAFT',
'DRAIN', 'DRAKE', 'DRAMA', 'DRANK', 'DRAWL', 'DRAWN', 'DREAD', 'DREAM', 'DRESS', 'DRIED',
'DRIER', 'DRIFT', 'DRILL', 'DRINK', 'DRIVE', 'DRYER', 'DRYLY', 'DWARF', 'DWELL', 'DWELT',
'DYING', 'EAGER', 'EAGLE', 'EARLY', 'EARTH', 'EASEL', 'EATEN', 'EATER', 'ECLAT', 'EDICT',
'EDIFY', 'EERIE', 'EGRET', 'EIGHT', 'EKING', 'ELATE', 'ELDER', 'ELECT', 'ELEGY', 'ELFIN',
'ELIDE', 'ELITE', 'EMAIL', 'EMCEE', 'ENACT', 'ENEMA', 'ENEMY', 'ENTER', 'ENTRY', 'ERASE',
'ERECT', 'ESSAY', 'ESTER', 'ETHER', 'ETHIC', 'EVADE', 'EVENT', 'EVERY', 'EVICT', 'EYING',
'FACET', 'FAINT', 'FAIRY', 'FAITH', 'FALSE', 'FANCY', 'FANNY', 'FARCE', 'FATAL', 'FATTY',
'FEAST', 'FECAL', 'FEIGN', 'FELLA', 'FEMME', 'FENCE', 'FERAL', 'FERRY', 'FETAL', 'FETCH',
'FETID', 'FEVER', 'FEWER', 'FIELD', 'FIEND', 'FIERY', 'FIFTH', 'FIFTY', 'FIGHT', 'FILER',
'FILET', 'FILLY', 'FILMY', 'FILTH', 'FINAL', 'FINCH', 'FINER', 'FIRST', 'FISHY', 'FLACK',
'FLAIL', 'FLAIR', 'FLAKE', 'FLAKY', 'FLAME', 'FLANK', 'FLARE', 'FLASH', 'FLASK', 'FLECK',
'FLEET', 'FLESH', 'FLICK', 'FLIER', 'FLING', 'FLINT', 'FLIRT', 'FLYER', 'FRAIL', 'FRAME',
'FRANK', 'FREAK', 'FREED', 'FREER', 'FRESH', 'FRIAR', 'FRIED', 'FRILL', 'FRISK', 'GAFFE',
'GAILY', 'GAMER', 'GAMMA', 'GASSY', 'GAVEL', 'GAWKY', 'GAYER', 'GAYLY', 'GEEKY', 'GEESE',
'GENIE', 'GENRE', 'GIANT', 'GIDDY', 'GIRLY', 'GIRTH', 'GIVEN', 'GIVER', 'GLADE', 'GLAND',
'GLARE', 'GLASS', 'GLEAM', 'GLEAN', 'GLIDE', 'GLINT', 'GNASH', 'GRACE', 'GRADE', 'GRAFT',
'GRAIL', 'GRAIN', 'GRAND', 'GRANT', 'GRASS', 'GRATE', 'GRAVE', 'GRAVY', 'GREAT', 'GREED',
'GREEN', 'GREET', 'GRIEF', 'GRILL', 'GRIME', 'GRIMY', 'GRIND', 'HAIRY', 'HALVE', 'HANDY',
'HARDY', 'HAREM', 'HARRY', 'HARSH', 'HASTE', 'HASTY', 'HATCH', 'HATER', 'HAVEN', 'HEADY',
'HEARD', 'HEART', 'HEATH', 'HEAVE', 'HEAVY', 'HEDGE', 'HEFTY', 'HEIST', 'HENCE', 'HILLY',
'HINGE', 'HITCH', 'HYENA', 'HYMEN', 'ICILY', 'ICING', 'IDEAL', 'IDLER', 'IDYLL', 'ILIAC',
'IMAGE', 'INANE', 'INERT', 'INFER', 'INLAY', 'INLET', 'INNER', 'INTER', 'IRATE', 'ISLET',
'ITCHY', 'KARMA', 'KAYAK', 'KHAKI', 'KINKY', 'KITTY', 'KNACK', 'KNAVE', 'KNEAD', 'KNEED',
'KNEEL', 'KNELT', 'KNIFE', 'KRILL', 'LADEN', 'LADLE', 'LAGER', 'LANCE', 'LANKY', 'LARGE',
'LARVA', 'LATCH', 'LATER', 'LATHE', 'LATTE', 'LAYER', 'LEACH', 'LEAFY', 'LEAKY', 'LEANT',
'LEARN', 'LEASE', 'LEASH', 'LEAST', 'LEAVE', 'LEDGE', 'LEECH', 'LEERY', 'LEFTY', 'LEGAL',
'LEGGY', 'LEVEL', 'LEVER', 'LIEGE', 'LIGHT', 'LIKEN', 'LILAC', 'LIMIT', 'LINEN', 'LINER',
'LITHE', 'LIVER', 'LIVID', 'LLAMA', 'LYING', 'LYNCH', 'LYRIC', 'MACAW', 'MADAM', 'MADLY',
'MAFIA', 'MAGIC', 'MAGMA', 'MAKER', 'MAMMA', 'MAMMY', 'MANGA', 'MANGE', 'MANGY', 'MANIA',
'MANIC', 'MANLY', 'MARCH', 'MARRY', 'MARSH', 'MASSE', 'MATCH', 'MATEY', 'MEALY', 'MEANT',
'MEATY', 'MECCA', 'MEDAL', 'MEDIA', 'MEDIC', 'MELEE', 'MERCY', 'MERGE', 'MERIT', 'MERRY',
'METAL', 'METER', 'MIDGE', 'MIDST', 'MIGHT', 'MILKY', 'MIMIC', 'MINCE', 'MINER', 'MINIM',
'MINTY', 'MIRTH', 'MISER', 'MISSY', 'MYRRH', 'NADIR', 'NAIVE', 'NANNY', 'NASAL', 'NASTY',
'NATAL', 'NAVAL', 'NAVEL', 'NEEDY', 'NEIGH', 'NERDY', 'NERVE', 'NEVER', 'NEWER', 'NEWLY',
'NICER', 'NICHE', 'NIECE', 'NIGHT', 'NINNY', 'NINTH', 'RACER', 'RADAR', 'RADII', 'RAINY',
'RAISE', 'RALLY', 'RAMEN', 'RANCH', 'RANDY', 'RANGE', 'RARER', 'RATTY', 'RAVEN', 'REACH',
'REACT', 'READY', 'REALM', 'REARM', 'REEDY', 'REFER', 'REFIT', 'REGAL', 'REIGN', 'RELAY',
'RELIC', 'REMIT', 'RENAL', 'RENEW', 'RESET', 'RESIN', 'RETCH', 'RETRY', 'REVEL', 'RHYME',
'RIDER', 'RIDGE', 'RIFLE', 'RIGHT', 'RIGID', 'RINSE', 'RISEN', 'RISER', 'RISKY', 'RIVAL',
'RIVER', 'RIVET', 'SADLY', 'SAFER', 'SAINT', 'SALAD', 'SALLY', 'SALSA', 'SALTY', 'SALVE',
'SANDY', 'SANER', 'SASSY', 'SATIN', 'SATYR', 'SAVVY', 'SCALD', 'SCALE', 'SCALY', 'SCANT',
'SCARE', 'SCARF', 'SCARY', 'SCENE', 'SCENT', 'SCRAM', 'SCREE', 'SCREW', 'SEDAN', 'SEEDY',
'SEMEN', 'SENSE', 'SERIF', 'SERVE', 'SEVEN', 'SEVER', 'SEWER', 'SHACK', 'SHADE', 'SHADY',
'SHAFT', 'SHAKE', 'SHAKY', 'SHALE', 'SHALL', 'SHALT', 'SHAME', 'SHANK', 'SHARD', 'SHARE',
'SHARK', 'SHAVE', 'SHAWL', 'SHEAR', 'SHEEN', 'SHEER', 'SHEET', 'SHEIK', 'SHELF', 'SHELL',
'SHIED', 'SHIFT', 'SHINE', 'SHINY', 'SHIRE', 'SHIRK', 'SHIRT', 'SHREW', 'SHYLY', 'SIEGE',
'SIEVE', 'SIGHT', 'SIGMA', 'SILKY', 'SILLY', 'SINCE', 'SINEW', 'SINGE', 'SIREN', 'SISSY',
'SKATE', 'SKIER', 'SKIFF', 'SKILL', 'SKIRT', 'SLACK', 'SLAIN', 'SLANG', 'SLANT', 'SLASH',
'SLATE', 'SLAVE', 'SLEEK', 'SLEET', 'SLICE', 'SLICK', 'SLIDE', 'SLIME', 'SLIMY', 'SLING',
'SLINK', 'SLYLY', 'SMACK', 'SMALL', 'SMART', 'SMASH', 'SMEAR', 'SMELL', 'SMELT', 'SMILE',
'SMIRK', 'SMITE', 'SMITH', 'SNACK', 'SNAIL', 'SNAKE', 'SNAKY', 'SNARE', 'SNARL', 'SNEAK',
'SNEER', 'SNIDE', 'SNIFF', 'STACK', 'STAFF', 'STAGE', 'STAID', 'STAIN', 'STAIR', 'STAKE',
'STALE', 'STALK', 'STALL', 'STAND', 'STANK', 'STARE', 'STARK', 'START', 'STASH', 'STATE',
'STAVE', 'STEAD', 'STEAK', 'STEAL', 'STEAM', 'STEED', 'STEEL', 'STEER', 'STEIN', 'STERN',
'STICK', 'STIFF', 'STILL', 'STILT', 'STING', 'STINK', 'STINT', 'STRAW', 'STRAY', 'STYLE',
'SWAMI', 'SWARM', 'SWASH', 'SWATH', 'SWEAR', 'SWEAT', 'SWEET', 'SWELL', 'SWIFT', 'SWILL',
'SWINE', 'SWING', 'SWIRL', 'SWISH', 'TACIT', 'TACKY', 'TAFFY', 'TAINT', 'TAKEN', 'TAKER',
'TALLY', 'TAMER', 'TANGY', 'TARDY', 'TASTE', 'TASTY', 'TATTY', 'TAWNY', 'TEACH', 'TEARY',
'TEASE', 'TEDDY', 'TEETH', 'TENET', 'TENSE', 'TENTH', 'TERRA', 'TERSE', 'TESTY', 'THANK',
'THEFT', 'THEIR', 'THEME', 'THERE', 'THESE', 'THETA', 'THICK', 'THIEF', 'THIGH', 'THING',
'THINK', 'THIRD', 'THREE', 'THREW', 'THYME', 'TIARA', 'TIDAL', 'TIGER', 'TIGHT', 'TILDE',
'TIMER', 'TIMID', 'TITAN', 'TITHE', 'TITLE', 'TRACE', 'TRACK', 'TRACT', 'TRADE', 'TRAIL',
'TRAIN', 'TRAIT', 'TRASH', 'TRAWL', 'TREAD', 'TREAT', 'TREND', 'TRIAD', 'TRIAL', 'TRICE',
'TRICK', 'TRIED', 'TRITE', 'TRYST', 'TWANG', 'TWEAK', 'TWEED', 'TWEET', 'TWICE', 'TWINE',
'TWIRL', 'TWIST', 'TYING', 'VALET', 'VALID', 'VALVE', 'VEGAN', 'VERGE', 'VERSE', 'VERVE',
'VICAR', 'VIGIL', 'VILLA', 'VINYL', 'VIRAL', 'VISIT', 'VISTA', 'VITAL', 'VIVID', 'VYING',
'WACKY', 'WAFER', 'WAGER', 'WAIST', 'WAIVE', 'WARTY', 'WASTE', 'WATCH', 'WATER', 'WAVER',
'WEARY', 'WEAVE', 'WEDGE', 'WEEDY', 'WEIGH', 'WEIRD', 'WELCH', 'WELSH', 'WENCH', 'WHACK',
'WHALE', 'WHARF', 'WHEAT', 'WHEEL', 'WHERE', 'WHICH', 'WHIFF', 'WHILE', 'WHINE', 'WHINY',
'WHIRL', 'WHISK', 'WHITE', 'WIDEN', 'WIDER', 'WIDTH', 'WIELD', 'WIGHT', 'WILLY', 'WINCE',
'WINCH', 'WINDY', 'WISER', 'WITCH', 'WITTY', 'WRACK', 'WRATH', 'WREAK', 'WRECK', 'WREST',
'WRING', 'WRIST', 'WRITE', 'WRYLY', 'YACHT', 'YEARN', 'YEAST', 'YIELD'
];

function getUtcDayKey(date = new Date()) {
    // "2025-11-09T12:34:56.789Z" -> "2025-11-09"
    return date.toISOString().slice(0, 10);
}

function hashString32(str) {
    let h = 2166136261 >>> 0; // FNV like offset
    for (let i = 0; i < str.length; i += 1) {
        h ^= str.charCodeAt(i);
        h = Math.imul(h, 16777619); // keep in 32 bits
    }
    return h >>> 0;
}

// WORD_LIST is your 898 word array, all uppercase

function getDailyIndex(date = new Date()) {
    const key = getUtcDayKey(date);      // for example "2025-11-09"
    const h = hashString32(key);         // deterministic 32 bit integer
    const n = WORD_LIST.length;
    return h % n;                        // 0 to n-1
}

function getDailyWord(date = new Date()) {
    return WORD_LIST[getDailyIndex(date)];
}

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
    } catch (e) {
        console.warn("stats parse error", e);
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

    // count game once per day
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
    el.textContent =
    "Games: " + stats.gamesPlayed +
    "   Wins: " + stats.wins +
    "   Streak: " + stats.currentStreak +
    "   Max streak: " + stats.maxStreak;
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
