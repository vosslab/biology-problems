# Matching Set Authoring Guide

This folder contains YAML "matching set" banks and small helper scripts that turn those banks into Blackboard-format questions.

## Start Here (30 seconds to first bank)

1. Copy `problems/matching_sets/TEMPLATE.yml` to a new file (pick a clear name like `enzyme_classes.yml`).
   - Suggested naming convention: use a clear topic prefix so sets map to chapters, like `enzymes_*`, `macromolecules_*`, `membranes_*`, `genetics_*`, `cell_biology_*`, `metabolism_*`.
2. Edit the four description lines: `key description`, `keys description`, `value description`, `values description`.
3. Add 8 to 20 keys under `matching pairs:` (your left column concepts).
4. For each key, add 2 to 4 phrasing variants (your right column definitions/functions).
5. Test-generate a small sample (see `Quick Test Commands` below).

## File Naming Convention (descriptive, jargon-free)

Use filenames that are readable to instructors and students, and that map naturally to chapters.

- Prefer a chapter/topic prefix + plain-English descriptor, for example `senses_receptor_types.yml` or `senses_pathway_components.yml`.
- Avoid deep jargon in filenames (keep jargon inside the YAML content, not the filename).
- Keep names short but specific; future-you should know what the bank covers without opening the file.

## What You Can Generate

- Matching questions (Blackboard `MAT`): use `problems/matching_sets/yaml_make_match_sets.py`
- Multiple-choice questions (Blackboard `MC`): use `problems/matching_sets/yaml_make_which_one_multiple_choice.py`

Both scripts read the same YAML structure (see `problems/matching_sets/TEMPLATE.yml`).

## When To Use Matching Sets (vs MC Statements)

This format is best when you want students to pair terms/components with a single best match.

Good fits for matching sets:

- Vocabulary: term -> definition
- Parts to function: pathway component -> role (enzyme/channel/protein -> function)
- Category mapping: receptor type -> modality, macromolecule -> monomer/bond type

If your goal is to test conceptual claims, misconception discrimination, or "which statement is TRUE/FALSE?" logic, consider the MC-statements format instead: `problems/multiple_choice_statements/MC_STATEMENTS_AUTHORING_GUIDE.md`.

## YAML File Structure

Each YAML file defines:

- A set of **keys** (the left column of the match list)
- A set of **values** (the right column; one value per key per question)
- Optional rules that control wording, formatting, and "do not place these together" exclusions

### Required Top-Level Keys

- `matching pairs`: a mapping of `key -> list of values`
- `key description` and `keys description`: singular and plural phrases for the key side
- `value description` and `values description`: singular and plural phrases for the value side

## qti_package_maker Terminology (MATCH items)

Internally, a matching question is represented as:

- `prompts_list`: the left-column headings (your YAML keys)
- `choices_list`: the right-column options (your YAML values)

In other words: keys become prompts, and values become choices.

## Deterministic Prompt Colors (default behavior)

For MATCH questions, this repo will automatically color the `prompts_list` (left-column headings) using a deterministic color wheel, to make matching tables easier to scan.

- Colors are assigned deterministically by sorting prompts alphabetically, so the same prompt set gets the same colors run-to-run.
- If any prompt already contains HTML color markup (for example `<span style="color: ...">`), automatic prompt coloring is disabled for the entire question (so author-chosen colors are preserved).

### Common Optional Top-Level Keys

- `items to match per question`: how many key/value pairs appear in each matching question (default is `5` in the scripts)
- `question override`: HTML/text that replaces the default question prompt
- `replacement_rules`: a mapping of literal substring replacements (often used for coloring or consistent formatting)
- `exclude pairs`: a list of 2-item lists like `[key_a, key_b]` to prevent those two keys from appearing in the same question

### Optional (Recommended) Metadata Keys

The generators ignore unknown top-level keys, so you can add author-facing metadata to help long-term maintenance:

- `topic`: short label (for example `phototransduction`)
- `learning_objective`: one sentence (for example `Trace the cGMP pathway in rods`)
- `source`: textbook/chapter or your course code

These help with search, maintenance, and chapter mapping when the folder grows over time.

## `matching pairs` Format

The typical pattern is:

```yml
matching pairs:
  Key A:
    - value A1
    - value A2
  Key B:
    - value B1
```

Notes:

- Each key must map to a YAML list (even if you only have one value).
- For each generated question, the generator will pick **one** value per key (randomly from that key's list).
- Values may contain HTML (for example `<sub>`, `<strong>`, `<p>`) and/or HTML entities (for example `&Delta;`).

## Biology Pattern: One Concept Per Key (with phrasing variants)

Named rule: "Same concept, different phrasing."

- Put synonyms and equivalent statements under one key as multiple values.
- Do not split a single concept across multiple keys (that turns synonyms into trick questions).

This is the biggest quality lever: it makes banks feel fresh without changing what you are assessing.

Instructor-friendly way to think about it:

- If two answers mean the same thing (synonyms, paraphrases, or equally acceptable wording), put them under the same key as separate lines.
- Students will only see one wording per key in any single generated question, but across different generated questions the bank naturally rotates through the alternate wordings.

## Excluding Confusable Pairs

If two keys are too similar (or their values are too easy to mix up), use `exclude pairs` so they never appear together:

```yml
exclude pairs:
  - [Coenzyme, Cofactor]
```

This filters key combinations before questions are generated.

Misconception-first checklist for `exclude pairs`:

- Exclude when students can reasonably know both terms, yet still mix them up under time pressure.
- Do not exclude just because two terms are related; that can remove the learning objective.
- Use it sparingly, only for classic confusions.

Biology examples:

- `cAMP` vs `cGMP`
- `competitive inhibitor` vs `non-competitive inhibitor`
- `agonist` vs `antagonist`

## Replacement Rules (Formatting, Color, Consistency)

`replacement_rules` is a simple "search and replace" table applied after question text and choice lists are constructed.
It is commonly used for:

- Highlighting phrases with HTML `<span style="color: ...">...`
- Ensuring consistent typography (for example using `&nbsp;` in fixed phrases)

Example:

```yml
replacement_rules:
  releases&nbsp;energy: "<span style='color: #e60000;'>releases&nbsp;energy</span>"
```

Tip: `problems/matching_sets/recommended_colors.csv` contains a suggested palette used in existing sets.

## What Keys and Values Should Look Like (for biology)

- Keys: stable concepts (enzyme class, receptor type, molecule, organelle, process).
- Values: one function or definition (one main idea), written so there is only one reasonable matching key.

## Authoring Tips

- Prefer "same concept, different phrasing" within a single key:
  - Put multiple acceptable wordings for the *same* idea under one key (as a list of values).
  - The generator will pick one wording per question, which makes the bank feel fresh while still assessing the same learning objective.
- Keep values distinct across different keys: if multiple keys could plausibly match the same value text, students will be guessing.
- Watch the combinatorics: matching questions are generated from key combinations.
  - If you have `n` keys and `k = items to match per question`, you can get up to `n choose k` question "skeletons" before values are chosen.
  - Use `-x/--max-questions` when testing large banks.
- Write for intro readability:
  - Use the simplest correct term (then optionally add a parenthetical clarifier).
  - Keep each value to one main idea; avoid "and also..." definitions that introduce extra concepts.
- House style (ESL-friendly, exam-friendly):
  - Prefer concrete verbs: binds, phosphorylates, opens, inhibits.
  - Avoid double negatives.
  - Define abbreviations on first use inside the value (for example `Protein kinase A (PKA)`).
  - Keep each value under ~15 to 20 words when possible.
- YAML does not allow tab indentation; use spaces.
- Quote strings that contain `:` or start with special characters.

Use a low-jargon starter set (enzyme classes, macromolecules, or noncovalent interactions) for your first bank, then move to pathway-heavy topics once the authoring pattern feels routine.

## How To Avoid Accidental Cues

Three quick checks that prevent "test-taking" answers:

- Keep value length similar across keys (do not let one answer be twice as long).
- Keep grammar parallel (all noun phrases, or all full sentences).
- Avoid unique keywords that appear only in one value (they give away the match).

### Normalize Formatting So Values Do Not “Telegraph” The Match

A very common matching-bank failure mode is that the value repeats a key word from the prompt.
That makes the item solvable by scanning for the repeated word instead of understanding the biology.

Quick check:

- If a prompt contains a distinctive word (for example `adenylyl`, `rhodopsin`, `transducin`, `phosphodiesterase`), do not repeat that same word in its matching values.
- Prefer functional descriptions that avoid the prompt noun (for example "enzyme that produces cAMP from ATP" instead of "adenylyl cyclase that produces cAMP").

## Difficulty Control (quick slider)

- Easier:
  - Use direct definitions and unique vocabulary.
  - Use fewer items per question (`items to match per question: 3` or `4`).
- Harder:
  - Use mechanism/consequence phrasing instead of definitions.
  - Include more similar terms (then use `exclude pairs` for the worst confusions).

## Faculty-Friendly Quality Checks

Before you ship a new matching set, do a quick pass for:

- Single learning objective per key: each key should test one concept, not a bundle of related facts.
- Common misconceptions: include phrasing that forces students to distinguish confusable ideas (and use `exclude pairs` if two keys are too confusable to appear together).
- Parallel grammar: keep values in similar grammatical form (all noun phrases, or all full sentences) to reduce "test-taking cues".
- Appropriate specificity: if one value is much more detailed than the others, students can use length as a hint.
- Accessibility: avoid relying on color alone to convey meaning; use color as an accent, not the only signal.

## Copy/Paste Example (biology)

Example: enzyme classes matched to reaction type (a good first bank).

```yml
#YAML file for Matching Questions
topic: enzymes_basics
learning_objective: Match enzyme classes to what they do.

items to match per question: 5

key description: enzyme class
keys description: enzyme classes

value description: reaction type
values description: reaction types

matching pairs:
  Kinase:
    - Adds a phosphate group to a substrate (phosphorylation)
    - Transfers a phosphate group to a molecule
  Phosphatase:
    - Removes a phosphate group from a substrate (dephosphorylation)
    - Catalyzes phosphate removal from a molecule
  Protease:
    - Breaks peptide bonds in proteins
    - Hydrolyzes peptide bonds
  Ligase:
    - Joins two molecules by forming a new bond (often using ATP)
    - Catalyzes bond formation to link molecules
  Isomerase:
    - Rearranges atoms within a molecule to form an isomer
    - Converts a molecule into its isomer
```

Mini-example (optional) for `exclude pairs` when two keys are too confusable to appear together:

```yml
exclude pairs:
  - [aspartate, aspartic acid]
  - [glutamate, glutamic acid]
```

## Troubleshooting Common YAML Mistakes

- Tabs vs spaces: YAML does not allow tab indentation.
- Colons: if a string contains `:` (or starts with `{`, `[`, `#`, `*`, `&`), put it in quotes.
- Smart quotes: if you pasted from Word/Docs, replace curly quotes with plain ASCII quotes.
- Lists: each value line must start with `- ` and be indented under its key.

## Quick Test Commands

From repo root:

```bash
source source_me.sh
/opt/homebrew/opt/python@3.12/bin/python3.12 problems/matching_sets/yaml_make_match_sets.py -y problems/matching_sets/your_set.yml -x 20
```

For MC questions derived from the same set:

```bash
source source_me.sh
/opt/homebrew/opt/python@3.12/bin/python3.12 problems/matching_sets/yaml_make_which_one_multiple_choice.py -y problems/matching_sets/your_set.yml -x 20
```

The scripts write `bbq-*.txt` outputs in the current working directory.
