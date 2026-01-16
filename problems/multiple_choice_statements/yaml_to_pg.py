#!/usr/bin/env python3
import os, yaml, random, argparse, re
from typing import Dict, List, Tuple

_fam_re = re.compile(r'^(truth|false)\s*(\d+)[a-z]?$')

PG_HEADER_MULTI = r"""DOCUMENT();

loadMacros(
  "PGstandard.pl",
  "PGchoicemacros.pl",
  "parserRadioButtons.pl",
);

TEXT(beginproblem());
$showPartialCorrectAnswers = 1;

# Multiple independent MC parts inside one problem file.
"""

PG_HEADER_SINGLE = r"""DOCUMENT();

loadMacros(
  "PGstandard.pl",
  "PGchoicemacros.pl",
  "parserRadioButtons.pl",
);

TEXT(beginproblem());
$showPartialCorrectAnswers = 1;
"""

PG_FOOTER = r"""ENDDOCUMENT();
"""

def load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def norm(s: str) -> str:
    return " ".join(s.split()).strip().lower()

def uniq(seq: List[str]) -> List[str]:
    seen = set()
    out = []
    for s in seq:
        k = norm(s)
        if k in seen:
            continue
        seen.add(k)
        out.append(s)
    return out

def apply_replacements(text: str, rules: Dict[str, str]) -> str:
    if not rules:
        return text

    # 1) Sort keys longest-first to prefer multi-word terms
    keys = sorted(rules.keys(), key=len, reverse=True)

    # 2) Build a regex that matches any of the plain keys
    pattern = re.compile("|".join(re.escape(k) for k in keys))

    # 3) Replace with numbered placeholders to avoid re-replacing inside inserted HTML
    placeholder_map = {}
    counter = 0

    def sub_fn(m):
        nonlocal counter
        k = m.group(0)
        replacement = rules[k]
        token = f"@@PGTOKEN{counter}@@"
        placeholder_map[token] = replacement
        counter += 1
        return token

    # Use the sub function during substitution
    out = pattern.sub(sub_fn, text)

    # 4) Restore placeholders exactly once (no further scanning of inserted HTML)
    for token, html in placeholder_map.items():
        out = out.replace(token, html)

    return out

def family_id(key: str) -> int:
    m = _fam_re.match(key)
    return int(m.group(2)) if m else -1

def group_by_family(d: Dict[str, str]) -> Dict[int, List[Tuple[str, str]]]:
    """family -> list of (key, text)"""
    fam: Dict[int, List[Tuple[str, str]]] = {}
    for k, v in d.items():
        f = family_id(k)
        if f < 0:
            continue
        fam.setdefault(f, []).append((k, v))
    # de-dup per family on text
    for f, items in fam.items():
        dedup = []
        seen = set()
        for k, v in items:
            if norm(v) in seen:
                continue
            seen.add(norm(v))
            dedup.append((k, v))
        fam[f] = dedup
    return fam

def esc_pg_single(s: str) -> str:
    # In single-quoted Perl strings, only \' and \\ need escaping.
    return s.replace('\\', '\\\\').replace("'", "\\'")

def mc_part_block(idx, prompt, choices, correct_text):
    # de-dupe & cap at 5
    seen = set()
    def _norm(s): return " ".join(s.split()).strip().lower()
    uniq_choices = []
    for c in choices:
        k = _norm(c)
        if k in seen:
            continue
        seen.add(k)
        uniq_choices.append(c)
    if len(uniq_choices) > 5:
        uniq_choices = uniq_choices[:5]

    import random as _r
    _r.shuffle(uniq_choices)

    # Perl array literal with properly escaped strings
    def perl_str(s): return "'" + esc_pg_single(s) + "'"
    perl_array = ", ".join(perl_str(c) for c in uniq_choices)
    correct_esc = esc_pg_single(correct_text)
    prompt_esc  = esc_pg_single(prompt)

    lines = []
    lines.append(f"# --- PART {idx} ---")
    # Build a RadioButtons widget with spacing between answers
    lines.append(f"my @choices_{idx} = ({perl_array});")
    lines.append(f"$rb_{idx} = RadioButtons(")
    lines.append(f"  [@choices_{idx}],")
    lines.append(f"  '{correct_esc}',")
    lines.append( "  labels => 'ABC',")
    lines.append( "  displayLabels => 1,")
    lines.append( "  separator => '<div style=\"margin-bottom: 0.7em;\"></div>',")
    lines.append( "  uncheckable => 0,")
    lines.append( "  randomize => 0,")  # we already shuffled in Python
    lines.append( ");")
    lines.append("BEGIN_TEXT")
    lines.append(f"{prompt_esc}")
    lines.append('<div style="margin-top: 2em;"></div>')
    lines.append(f"\\{{ $rb_{idx}->buttons() \\}}")
    lines.append("END_TEXT\n")
    lines.append(f"ANS( $rb_{idx}->cmp() );")
    lines.append("")
    return "\n".join(lines)

def single_question_pg(prompt: str, choices: List[str], correct_text: str) -> str:
    return "\n".join([PG_HEADER_SINGLE, mc_part_block(1, prompt, choices, correct_text), PG_FOOTER])

def pick_distractors_from_opposite_pool(opposite_by_family: Dict[int, List[str]],
                                        avoid_family: int,
                                        k: int,
                                        rng: random.Random) -> List[str]:
    pool = []
    for fam, items in opposite_by_family.items():
        if fam == avoid_family:
            continue
        pool.extend(items)
    pool = uniq(pool)
    rng.shuffle(pool)
    return pool[:k]

def build_every_statement_items(data: dict,
                                rng: random.Random,
                                choices_per_q: int = 5) -> List[Tuple[str, List[str], str]]:
    """
    Generate one question per statement:
      - every truth -> a TRUE question
      - every false -> a FALSE question
    Each question has exactly `choices_per_q` options (1 key + k-1 distractors).
    """
    topic = data.get("topic", "this topic")
    connection_words = (data.get("connection_words")
                    or data.get("connecting_words")
                    or ["about", "regarding", "concerning", "of"])
    replace_rules: Dict[str, str] = data.get("replacement_rules") or {}

    # 🧼 Clean up replacement rules - strip out any HTML or color styling
    clean_rules = {}
    for k, v in (data.get("replacement_rules") or {}).items():
        # Skip replacements that contain HTML tags (like <span>, <b>, etc.)
        if re.search(r'<.*?>', v, re.IGNORECASE):
            continue
        clean_rules[k] = v
    replace_rules = clean_rules

    truths_map: Dict[str, str] = data.get("true_statements") or {}
    falses_map: Dict[str, str] = data.get("false_statements") or {}

    truth_by_fam_pairs = group_by_family(truths_map)
    false_by_fam_pairs = group_by_family(falses_map)

    truth_by_fam_texts: Dict[int, List[str]] = {f: [t for _, t in pairs] for f, pairs in truth_by_fam_pairs.items()}
    false_by_fam_texts: Dict[int, List[str]] = {f: [t for _, t in pairs] for f, pairs in false_by_fam_pairs.items()}

    items: List[Tuple[str, List[str], str]] = []
    need_distractors = choices_per_q - 1

    # --- TRUE questions ---
    for t_key, t_text in truths_map.items():
        fam = family_id(t_key)
        distractors = pick_distractors_from_opposite_pool(false_by_fam_texts, fam, need_distractors, rng)
        if len(distractors) < need_distractors:
            continue
        conn = rng.choice(connection_words)

        # ✅ Bold, colored, and slightly larger TRUE text
        prompt = (
            f'<p style="margin-top: 15px;">'
            f'Which one of the following statements is '
            f'<span style="color: MediumSeaGreen; font-weight: bold; font-size: 110%;">TRUE</span> '
            f'{conn} {topic}?'
            f'</p>'
        )

        key_h = apply_replacements(t_text, replace_rules)
        distractors = uniq(distractors)[:4]
        choices_h = [apply_replacements(c, replace_rules) for c in distractors + [t_text]]
        rng.shuffle(choices_h)
        items.append((prompt, choices_h, key_h))

    # --- FALSE questions ---
    for f_key, f_text in falses_map.items():
        fam = family_id(f_key)
        distractors = pick_distractors_from_opposite_pool(truth_by_fam_texts, fam, need_distractors, rng)
        if len(distractors) < need_distractors:
            continue
        conn = rng.choice(connection_words)

        # ✅ Bold, colored, and slightly larger FALSE text
        prompt = (
            f'<p style="margin-top: 15px;">'
            f'Which one of the following statements is '
            f'<span style="color: DarkOrange; font-weight: bold; font-size: 110%;">FALSE</span> '
            f'{conn} {topic}?'
            f'</p>'
        )

        key_h = apply_replacements(f_text, replace_rules)
        distractors = uniq(distractors)[:4]
        choices_h = [apply_replacements(c, replace_rules) for c in distractors + [f_text]]
        rng.shuffle(choices_h)
        items.append((prompt, choices_h, key_h))

    return items

def write_pg_multi(out_path: str, items, limit=None) -> int:
    if limit is not None:
        items = items[:limit]
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(PG_HEADER_MULTI + "\n")
        for i, (prompt, choices, correct) in enumerate(items, start=1):
            f.write(mc_part_block(i, prompt, choices, correct) + "\n")

            # Add separator *inside* a TEXT block, but not after the last part
            if i < len(items):
                f.write("BEGIN_TEXT\n")
                f.write("<div style='margin: 2em 0; border-top: 1px solid #ddd;'></div>\n")
                f.write("END_TEXT\n")
        f.write(PG_FOOTER)
    return len(items)


def write_pg_one_per_file(base_out: str, items: List[Tuple[str, List[str], str]], limit: int = None) -> int:
    if limit is not None:
        items = items[:limit]
    count = 0
    for i, (prompt, choices, correct) in enumerate(items, start=1):
        pg_text = single_question_pg(prompt, choices, correct)
        out_path = f"{base_out}_q{i:03d}.pg"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(pg_text)
        count += 1
    return count

def parse_args():
    p = argparse.ArgumentParser(description="YAML -> WeBWorK PG (one question per statement, colored, 5 options)")
    p.add_argument("input_yaml", help="Input YAML file")
    p.add_argument("--limit", type=int, default=None, help="Limit number of questions (for quick testing)")
    p.add_argument("--one-per-file", action="store_true", help="Write one .pg per question instead of a single multi-part .pg")
    p.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    return p.parse_args()

def main():
    args = parse_args()
    rng = random.Random(args.seed)
    data = load_yaml(args.input_yaml)

    # ALWAYS 5 choices per question by design
    items = build_every_statement_items(data, rng, choices_per_q=5)

    base = os.path.splitext(args.input_yaml)[0]
    if args.one_per_file:
        written = write_pg_one_per_file(base, items, limit=args.limit)
        print(f"✅ Wrote {written} files like {base}_q001.pg, {base}_q002.pg, ...")
    else:
        out_path = base + ".pg"
        written = write_pg_multi(out_path, items, limit=args.limit)
        print(f"✅ Wrote {written} sub-questions to {out_path}")

if __name__ == "__main__":
    main()
