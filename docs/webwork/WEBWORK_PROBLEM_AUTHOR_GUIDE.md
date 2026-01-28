# WeBWorK Problem Author Guide (PGML-First, Corpus-Compatible)

This guide is prescriptive. Follow it when creating new `.pg` problems intended for long-term reuse, searchability, automated analysis, and inclusion in a PGML-first corpus.

This document focuses on **problem authoring** (PGML usage, structure, randomization, answer checking), and assumes you already follow the separate **header and tagging** guide for `DESCRIPTION`, `KEYWORDS`, `DBsubject`, etc.

---

## Goals

1. **PGML-first**: problem text and blanks live in PGML blocks.
2. **Inline grading**: each visible blank should have an attached evaluator at the blank site.
3. **Robust randomization**: avoid degenerate cases and fragile edge conditions.
4. **Portable**: no course-local dependencies unless explicitly optional.
5. **Auditable**: a reader can understand intent and constraints from comments and structure.

---

## Canonical file skeleton (required)

Use this layout unless you have a strong reason not to.

```perl
## (Tagging header block goes here)

DOCUMENT();

loadMacros(
  "PGstandard.pl",
  "MathObjects.pl",
  "PGML.pl",
  "PGcourse.pl",
);

TEXT(beginproblem());

$showPartialCorrectAnswers = 1;

# ----------------------------
# 1) Context and configuration
# ----------------------------

# ----------------------------
# 2) Randomization and setup
# ----------------------------

# ----------------------------
# 3) Define correct answers
# ----------------------------

# ----------------------------
# 4) Problem text (PGML)
# ----------------------------
BEGIN_PGML
...
END_PGML

# ----------------------------
# 5) Solutions, hints (optional)
# ----------------------------

ENDDOCUMENT();
```

Rules:

- Always include `DOCUMENT();` and `ENDDOCUMENT();`.
- Put all macro loads in one `loadMacros(...)` block.
- Keep setup, answers, and PGML text in distinct sections with headings.

---

## Macro requirements

### Minimum recommended macro set (default)

Use only what you need. Start with:

- `PGstandard.pl` (required in practice)
- `MathObjects.pl` (recommended for modern evaluators)
- `PGML.pl` (required for PGML authoring)
- `PGcourse.pl` (commonly expected; keep unless you have a reason to drop it)

### Add macros intentionally

If you add a specialized macro, add a short comment explaining why.

Example:

```perl
loadMacros(
  "PGstandard.pl",
  "MathObjects.pl",
  "PGML.pl",
  "parserPopUp.pl",  # dropdown widget
  "PGcourse.pl",
);
```

---

## PGML requirements (PGML-first)

### Use PGML for student-facing text (required)

New problems should put the statement, formatting, and blanks inside `BEGIN_PGML ... END_PGML`.

### Use PGML blanks, not legacy answer rules (strongly preferred)

Prefer:

```perl
BEGIN_PGML
Compute [`[$a]+[$b]`]. Answer: [__________]{$ans}
END_PGML
```

Avoid relying on a blank in PGML while grading is done later elsewhere.

---

## HTML whitelist and sanitizers (required awareness)

PGML output is filtered by an HTML whitelist in this install. Tags like `table`, `tr`, and `td` are blocked and will warn or render badly.

Rules:

- Do not use HTML tables in PGML. Use flexbox `div` layouts, a TeX `array`, or `niceTables.pl` if that macro is available.
- Keep TeX wrapper slots present in `MODES(...)` wrappers (or PGML tag wrappers) even for web-only problems.
- For styling, use `span` and `MODES(HTML => '<span ...>', TeX => $text)`. If a sanitizer strips `<style>` blocks (for example in Blackboard), prefer inline styles or `<font color="...">` as a fallback.
- PGML parses once. Do not build PGML tag wrapper syntax inside Perl variables and expect a second parse.
- If you need to inject HTML stored in a Perl variable, render it with `[$var]*` so PGML does not escape the tags.
- Only wrap strings in `MODES(...)` when you truly need mode-specific output (for example HTML tags). If a value is plain text with no HTML tags or mode differences, use a plain string instead. When `MODES(...)` is used in this repo, keep the TeX value empty.

---

## Emphasis for critical words (recommended)

Use concise visual emphasis for key terms like ABOVE/BELOW, NOT, or the target
concept. Keep TeX output empty for these spans in this repo to avoid renderer
and ADAPT mismatches. Prefer HTML `span` styles over MathJax color macros.

Example:

```perl
my $above_emph = MODES(
  TeX => '',
  HTML => "<span style='color:#d96500;font-weight:700;'>ABOVE</span>",
);
my $below_emph = MODES(
  TeX => '',
  HTML => "<span style='color:#1f7a1f;font-weight:700;'>BELOW</span>",
);

BEGIN_PGML
When the pH is two units [$above_emph]* the pKa, what form is present?
END_PGML
```

Guidelines:

- Keep emphasis short (1 to 3 words).
- Use high-contrast colors and bold weight for readability.
- Do not rely on MathJax macros for color or emphasis.

---

## Question order (recommended)

Use this ordering in PGML to keep questions consistent and scannable:

1) Background (context or scenario)
2) Statement (what is being asked)
3) Data/table (if any)
4) Directions (how to respond, constraints, formatting)

Keep directions concise and place them after the data or statement rather than
before the prompt.

---

## HTML in PGML (PG 2.17)

For PG 2.17, raw HTML layouts are reliable when you keep TeX output empty.
This is the recommended pattern for two-column matching layouts.

Rules:

- Emit raw HTML only in `MODES(TeX => '', HTML => '...')` so TeX output is empty.
- Use `HEADER_TEXT(MODES(TeX => '', HTML => <<'END_STYLE'))` for CSS blocks.
- If a Perl variable contains HTML (`<span>`, `<div>`), output it as `[$var]*`.
- Avoid PGML tag wrapper syntax (`[< ... >]{...}`) for complex layouts; it is
  fragile in PG 2.17.
- Do not use blocked tags like `table`, `tr`, `td`.

Example (HTML-only wrapper):

```perl
[@ MODES(TeX => '', HTML => '<div class="two-column"><div>') @]*
... left column ...
[@ MODES(TeX => '', HTML => '</div><div class="right-col">') @]*
... right column ...
[@ MODES(TeX => '', HTML => '</div></div>') @]*
```

---

## Inline grading requirements (required)

### Principle

If the student sees a blank, the grader should be attached at that blank in the PGML.

This is a corpus requirement because it makes extraction and refactoring reliable.

### Required patterns

1) Direct evaluator attached to blank

```perl
my $ans = Compute("$a + $b");

BEGIN_PGML
Answer: [__________]{$ans}
END_PGML
```

2) Star specifications (allowed, but document)

Star specifications are allowed if you need a non-default evaluator shape. Keep it simple and add a one-line comment about why.

```perl
# Star spec used to apply a custom evaluator behavior.
BEGIN_PGML
Answer: [__________]*{$ans}
END_PGML
```

### Avoid these patterns (strongly discouraged)

- PGML blank with no payload plus later `ANS(...)` wiring.
- Variable-based wiring where a blank is created but the evaluator is attached in a different section with no clear linkage.

These are difficult to analyze and will tend to fall into "unknown" buckets in tooling.

---

## Context and configuration (required)

### Choose an explicit context

Always set a context appropriate for the expected answer type.

Examples:

- `Context("Numeric");`
- `Context("Real");`
- `Context("Vector");`
- `Context("Matrix");`
- `Context("Complex");`

### Set tolerances and flags intentionally

If you change defaults, do it in one place and comment why.

Example:

```perl
Context("Numeric");
Context()->flags->set(
  tolerance => 0.001,
  tolType   => "absolute",
);
```

Rules:

- Prefer absolute tolerance for most numeric-entry problems unless relative tolerance is clearly better.
- Do not silently rely on default tolerances if the statement requires rounding or precision.

---

## Randomization rules (required)

Randomization must be stable, readable, and avoid edge cases.

Requirements:

1. No custom seeding. Use WeBWorK's built-in seeding.
2. Deterministic for a fixed seed. Do not rely on Perl hash key order; sort keys before randomized selection.
3. Avoid degeneracy.
   - No division by zero.
   - No invalid domains (log of nonpositive, sqrt of negative) unless the context supports it.
4. Bound magnitudes to reasonable ranges for readability.
5. Guard interacting random choices when needed.

### Guard patterns

Avoid zero denominators:

```perl
my $b;
do { $b = random(-5, 5, 1); } while ($b == 0);
```

Avoid repeated or conflicting values:

```perl
my $a = random(2, 9, 1);
my $b;
do { $b = random(2, 9, 1); } while ($b == $a);
```

Avoid invalid domain for log:

```perl
my $x0;
do { $x0 = random(-5, 5, 1); } while ($x0 <= 0);
```

Document non-obvious constraints:

- If a guard exists, add a short comment explaining what it prevents.

---

## Answer definitions and evaluators (required)

### Use MathObjects evaluators (recommended)

Prefer `Compute(...)` and related constructors.

Examples:

- Numeric: `Compute("...")`
- Formula: `Formula("...")` or `Compute("...")` in an appropriate context
- Vector/list: `Compute("(1,2,3)")` or list contexts
- Units: use a units-aware strategy when units matter

### Keep evaluator objects near their use

Define answers in the "Define correct answers" section, then attach them inline in PGML.

---

## Multi-part problems (required practices)

### Structure multi-part answers explicitly

- Define a distinct evaluator variable per part.
- Attach each evaluator to its blank.
- Keep part labels in the PGML text.

Example:

```perl
my $ans_a = Compute("...");
my $ans_b = Compute("...");

BEGIN_PGML
(a) ... [__________]{$ans_a}

(b) ... [__________]{$ans_b}
END_PGML
```

### Avoid anonymous evaluator arrays

Do not rely on "implicit ordering" of `ANS(...)` calls to bind graders to blanks.

---

## Widgets (dropdown, radio, checkbox)

If you use interactive widgets, treat them as first-class and keep grading explicit.

### Popups

- Load `parserPopUp.pl`.
- Define the popup object clearly.
- Attach evaluator at the blank/widget site.

### Radio and checkbox lists

- Load the relevant parser macro (`parserRadioButtons.pl`, etc.).
- Keep options stable and avoid randomizing option wording unless you also randomize the answer mapping safely.

---

## Randomization and seeds

- Use a local `PGrandom` instance seeded with `problemSeed` when you need
  deterministic output for a fixed seed.
- Avoid `SRAND(seed)` unless you intend to reset the global RNG for the whole
  problem.
- When selecting from hash keys, sort keys before random selection so a fixed
  seed yields stable results across runs.
- Prefer non-deprecated helpers (for example `random_subset`) over wrappers like
  `NchooseK` when possible.
- See [RANDOMIZATION_REFERENCE.md](RANDOMIZATION_REFERENCE.md) for a list of
  common PG randomization entry points.

---

## Solutions and hints

### Use PGML solution/hint blocks when available

Prefer standard PGML solution/hint mechanisms if your environment supports them.

Rules:

- Keep solutions correct and concise.
- Do not include extraneous debugging prints.
- If the solution depends on a random parameter, show the parameter values clearly.
- ADAPT does not render HTML or numeric Unicode entities in solution blocks; keep solution text plain ASCII when exporting to ADAPT (for example, avoid `CH&#8322;CH&#8322;` in solutions).

---

## Units, rounding, and precision (required when relevant)

### Units

- State expected units in the problem text.
- Use a units-aware evaluator approach if you want unit flexibility.
- Do not silently assume units.

### Rounding

If rounding is required:

- Say so explicitly in the statement.
- Match grading tolerance or evaluator behavior to the stated rounding rule.

---

## Portability rules (recommended, often required)

1. Avoid course-local macros or files.
2. If you use images, include them with the problem and reference via a relative path.
3. Avoid applets unless necessary. If used, document constraints and provide a non-applet fallback.

---

## Documentation inside code (required)

Add short comments explaining:

- Mathematical intent (what is being tested).
- Randomization constraints and why they exist.
- Any non-default context flags or tolerances.
- Any specialized grader behavior.

Do not narrate Perl syntax. Explain the reason.

---

## Author checklist (required)

Before adding a problem to the corpus:

1. Render multiple versions to sample random cases.
2. Verify the displayed question matches the grader.
3. Verify correct answers are accepted and common incorrect forms are rejected.
4. Check edge cases produced by randomization.
5. Confirm the file runs without course-local dependencies.
6. Confirm every visible blank has an inline evaluator payload in PGML.

---

## Template you can copy (PGML-first)

```perl
## DESCRIPTION
## One to three sentences describing the task and any adoption-relevant constraints.
## ENDDESCRIPTION
## KEYWORDS('keyword1','keyword2','keyword3')
## DBsubject('Subject')
## DBchapter('Chapter')
## DBsection('Section')
## Date('YYYY-MM-DD')
## Author('Name')
## Institution('Institution')

DOCUMENT();

loadMacros(
  "PGstandard.pl",
  "MathObjects.pl",
  "PGML.pl",
  "PGcourse.pl",
);

TEXT(beginproblem());

$showPartialCorrectAnswers = 1;

# 1) Context and configuration
Context("Numeric");

# 2) Randomization and setup
my $a = random(2, 9, 1);
my $b;
do { $b = random(2, 9, 1); } while ($b == 0);

# 3) Define correct answers
my $ans = Compute("$a/$b");

# 4) Problem text (PGML)
BEGIN_PGML
Compute [`\\frac{[$a]}{[$b]}`].

Answer: [__________]{$ans}
END_PGML

ENDDOCUMENT();
```
