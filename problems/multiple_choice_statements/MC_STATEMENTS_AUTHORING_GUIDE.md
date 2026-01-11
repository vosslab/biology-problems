# Multiple Choice Statements Authoring Guide

This folder contains YAML "statement banks" and a generator that turns them into multiple-choice questions of the form: "Which one statement is TRUE?" or "Which one statement is FALSE?"

## Start Here (30 seconds to first bank)

1. Copy `problems/multiple_choice_statements/TEMPLATE.yml` to a new file (pick a clear name like `membrane_diffusion.yml`).
2. Set `topic:` to the concept you want in the question stem.
3. Add 8 to 20 items under `true_statements:` and `false_statements:`.
4. For key concepts that have multiple equivalent phrasings, make 2 to 4 variants (see the ID naming rule below).
5. Test-generate a small sample:

```bash
source source_me.sh
/opt/homebrew/opt/python@3.12/bin/python3.12 problems/multiple_choice_statements/yaml_multiple_choice_statements.py -y problems/multiple_choice_statements/your_set.yml -x 20
```

## File Naming Recommendation

Do not end filenames with `*_mc_statements.yml` in this folder; it is redundant.

Use descriptive, jargon-free names that map to chapters, for example `senses_coding_principles.yml` (prefix + plain-English topic).

Prefer short, chapter-friendly names like:

- `senses_chemosensation.yml`
- `senses_coding_principles.yml`
- `enzymes_inhibitors.yml`

## Picking A Good Topic (3-step rule)

1. Start low-jargon and one-learning-objective: diffusion, macromolecules, enzyme basics, noncovalent forces.
2. Make sure the topic has crisp true/false claims (not "it depends" interpretation).
3. Save pathway-heavy topics for later (phototransduction, signaling cascades) after the authoring pattern feels routine.

## What Gets Generated

- The generator writes a `bbq-TFMS-<yaml_stem>-questions.txt` file in the current directory.
- By default it generates both:
  - "Which statement is TRUE ... ?" questions
  - "Which statement is FALSE ... ?" questions
- You can disable either form at runtime:
  - `--no-true` to skip TRUE questions
  - `--no-false` to skip FALSE questions

## When To Use MC Statements (vs Matching Sets)

This format is best when you want students to evaluate ideas (truth/falsehood), not just map terms to definitions.

Good fits for MC statements:

- "Which statement is TRUE/FALSE?" conceptual checks
- Misconception diagnostics (wrong molecule, wrong direction, wrong location, sign flips, etc.)
- "Why" and "what changes" logic that is hard to make one-to-one

If your goal is to map terms/components to their matching definitions/functions (especially pathways and part-to-function), consider a matching set instead: `problems/matching_sets/MATCHING_SET_AUTHORING_GUIDE.md`.

## YAML File Structure

Each YAML file defines:

- A `topic` used in the question stem.
- A pool of `true_statements` (correct statements).
- A pool of `false_statements` (incorrect statements).
- Optional style rules (replacement rules and custom stems).

### Required Top-Level Keys

- `topic`: short phrase used in the stem (for example `DNA structure`).
- `true_statements`: mapping of `id -> statement text`
- `false_statements`: mapping of `id -> statement text`

### Common Optional Top-Level Keys

- `connection_words`: a YAML list of stem connectors (defaults to built-in words like `concerning`, `about`, `regarding`).
- `replacement_rules`: a mapping of literal substring replacements (often used for coloring or consistent formatting).
- `override_question_true`: replace the TRUE stem with your own HTML/text, or set to `~` to disable TRUE questions.
- `override_question_false`: replace the FALSE stem with your own HTML/text, or set to `~` to disable FALSE questions.

#### What `~` Means (YAML null)

Many banks use `~`. In YAML, `~` means "null" (like Python `None`).

In practice, this generator treats `~` differently depending on the key:

- `connection_words: ~` means "use the built-in defaults".
- `override_question_true: ~` means "disable the TRUE-question form".
- `override_question_false: ~` means "disable the FALSE-question form".
- `conflict_rules: ~` is fine; the generator auto-builds conflict rules from your statement IDs.

### Optional (Recommended) Metadata Keys

The generator ignores unknown top-level keys, so you can add author-facing metadata to help long-term maintenance:

- `topic_tag`: short label (for example `replication`)
- `learning_objective`: one sentence (for example `Distinguish leading vs lagging strand synthesis`)
- `source`: textbook/chapter or your course code

## Statement IDs and Conflict Groups (important)

Named rule: "Same concept, different phrasing."

- Put equivalent phrasings for the same concept as multiple statements that share the same number, like `truth4a`, `truth4b`.
- Do the same for false variants, like `false4a`, `false4b`.

Why: the generator automatically prevents multiple variants of the same idea from appearing together in one question, based on these ID patterns.

Practical authoring pattern:

- Use `truth<N>a`, `truth<N>b`, `truth<N>c` for true variants.
- Use `false<N>a`, `false<N>b`, `false<N>c` for false variants.

Mini-example (visual):

```yml
true_statements:
  truth3a: Enzymes lower activation energy.
  truth3b: Enzymes speed reactions by lowering activation energy.
```

These are the same concept with different phrasing, so they share the `3` and will not appear together as separate choices in the same question.

## Replacement Rules (Formatting, Color, Consistency)

`replacement_rules` is a simple "search and replace" table applied to question text and choices.
It is commonly used for:

- Highlighting phrases with HTML `<span style="color: ...">...`
- Consistent symbols/typography (for example `&Delta;G`, `&nbsp;`)

Tip: `problems/multiple_choice_statements/recommended_colors.csv` contains a suggested palette used in existing banks.

## What Statements Should Look Like (for biology)

- One main idea per statement (avoid "and also..." bundles that introduce extra claims).
- Enforcement rule: if you can underline two separate facts, split the statement.
- Biology-first wording: concrete verbs (binds, phosphorylates, opens, inhibits).
- Avoid double negatives.
- Define abbreviations on first use inside the statement (for example `Protein kinase A (PKA)`).
- Keep statements similar in length and grammar to avoid test-taking cues.

## What Makes A Good False Statement (biology patterns)

Aim for "plausible but wrong" in a way that diagnoses a misconception. Good patterns:

- Wrong substrate or reactant (ATP vs GTP, NADH vs NADPH).
- Wrong directionality (influx vs efflux, synthesis vs degradation).
- Wrong cellular location (nucleus vs cytosol vs mitochondrion).
- Swapped cofactors or ions (Mg2+ vs Ca2+).
- Wrong sign/relationship for thermodynamics (use `&Delta;G` / equilibrium logic).

Practical trick: write the true statement first, then create the false statement by changing exactly one detail.

## How To Avoid Accidental Cues

Three quick checks that prevent "test-taking" answers:

- Keep statement length similar across choices (do not let one be twice as long).
- Keep grammar parallel (all noun phrases, or all full sentences).
- Avoid unique keywords that appear only in one choice (they give away the answer).

## Difficulty Control (quick slider)

- Easier:
  - Use direct definitions and unique vocabulary.
  - Keep false statements clearly wrong (one obvious error).
- Harder:
  - Make false statements "plausible but wrong" (common misconceptions).
  - Use more similar terms (then rely on the conflict grouping rule to avoid near-duplicates in the same question).

## Copy/Paste Example (biology)

Example: second messenger signaling.

```yml
---
topic: second messenger signaling
learning_objective: Distinguish cAMP vs cGMP roles and enzymes that regulate them.

replacement_rules:
  cAMP: "<strong>cAMP</strong>"
  cGMP: "<strong>cGMP</strong>"

true_statements:
  truth1a: cAMP is a second messenger made from ATP
  truth1b: cyclic AMP (cAMP) is produced from ATP by adenylyl cyclase
  truth2: phosphodiesterase breaks down cyclic nucleotides to terminate a signal
  truth3: Protein kinase A (PKA) is activated by cAMP

false_statements:
  false1a: cAMP is a second messenger made from glucose
  false1b: cyclic AMP (cAMP) is produced from ADP by phosphodiesterase
  false2: phosphodiesterase makes cAMP from ATP
  false3: Protein kinase A (PKA) is activated by cGMP
```

## Troubleshooting Common YAML Mistakes

- Tabs vs spaces: YAML does not allow tab indentation.
- Colons: if a string contains `:` (or starts with `{`, `[`, `#`, `*`, `&`), put it in quotes.
- Smart quotes: if you pasted from Word/Docs, replace curly quotes with plain ASCII quotes.
- Lists: `connection_words` must be a YAML list (each item starts with `- `).

## Quick Lint Checklist (bank hygiene)

Before using a bank in an assessment, do a quick pass for:

- Misfiled statements: confirm all `truth*` entries are under `true_statements` and all `false*` entries are under `false_statements`.
- ID collisions: avoid reusing the same ID for two different meanings (for example two unrelated `truth5a` ideas).
- Duplicate statement text: the generator fails if the exact same sentence appears twice (even across true/false).
- Replacement rule overlap: prefer specific, non-overlapping phrases to avoid nested spans or partial matches (for example avoid having `cells`, `Cells`, and `' cell'` all at once unless you really need it).
- One-pass grammar scan: fix obvious typos and subject/verb agreement; it improves student trust even when the biology is correct.
