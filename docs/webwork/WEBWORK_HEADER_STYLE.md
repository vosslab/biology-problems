# WeBWorK PG Header and Tagging Guidelines (OPL Compatible)

This guide covers only the **header comment block** and related metadata comments that make a `.pg` problem searchable, classifiable, and maintainable in the Open Problem Library (OPL) ecosystem. It does not cover PG code, PGML, graders, or implementation.

The "tagging" header block is a standard OPL convention and is documented on the WeBWorK wiki and visible throughout OPL problems.

---

## Scope

Use this guidance for any `.pg` file intended for long-term reuse. The goal is that a tool can parse and index the header without running the problem.

**Rules in this document are prescriptive.**

---

## Placement and formatting rules

1. Put the metadata block near the top of the file, before substantial code.
2. Use comment lines that start with `##` (double hash).
3. Keep one tag per line.
4. Use consistent quoting. Prefer single quotes inside tag functions.
5. Avoid smart quotes or non-ASCII punctuation in headers. Use plain ASCII.

---

## Canonical header block

A well-formed header usually contains:

1. `DESCRIPTION` block (required)
2. `KEYWORDS(...)` (strongly recommended)
3. `DBsubject(...)`, `DBchapter(...)`, `DBsection(...)` (strongly recommended)
4. Attribution and provenance fields (recommended, but valuable)

Order is not technically required, but the canonical order below is recommended for consistency.

---

## 1) DESCRIPTION block (required)

### Purpose

Human-readable summary for instructors and reviewers.

### Format

Use `## DESCRIPTION` and `## ENDDESCRIPTION`. Put plain English in between.

### Content requirements

- 1 to 4 sentences.
- Describe the task, not the story wrapper.
- Include constraints that affect adoption (rounding requirement, unit expectations, domain restrictions).
- If adapted, say "Adapted from ..." or "Based on ...".

### Example

```text
## DESCRIPTION
## Compute the derivative of a polynomial and evaluate it at a specified point.
## ENDDESCRIPTION
```

### Do not do

- Do not paste full solutions.
- Do not include long pedagogical essays.
- Do not include code.

---

## 2) KEYWORDS(...) (strongly recommended)

### Purpose

Search terms for discoverability.

### Format

A single line:

```text
## KEYWORDS('keyword1','keyword2','keyword3')
```

### Rules

- Use 3 to 10 keywords.
- Use concepts and techniques, not character names or story nouns.
- Prefer lower-case unless capitalization matters.
- Prefer canonical spellings: integration by parts, chain rule, partial fraction, eigenvalues.
- Avoid duplicates already implied by DBsubject, but include key techniques.

### Example

```text
## KEYWORDS('derivative','polynomial','evaluate at a point','power rule')
```

---

## 3) Library classification: DBsubject / DBchapter / DBsection (strongly recommended)

### Purpose

Primary browse and analysis hooks. These are the most useful tags for corpus statistics and discovery.

### Format

```text
## DBsubject('Calculus - single variable')
## DBchapter('Derivatives')
## DBsection('Basic differentiation rules')
```

### Rules

- Use one DBsubject, one DBchapter, one DBsection when possible.
- Match existing strings used elsewhere in your library.
- Choose the most specific correct subject that still fits typical course organization.
- If uncertain, search for existing usage and copy the exact string.

### Allowed omissions

- If you cannot confidently assign DBchapter or DBsection, omit them.
- Prefer keeping DBsubject even if chapter and section are omitted.

### Common pitfalls

- Quoted duplicates like `'Algebra'` vs `Algebra`. Pick one style and stick to it.
- Empty subject strings. If truly unknown, omit the DBsubject line rather than writing an empty label.

---

## 4) Attribution and provenance fields (recommended)

These fields are frequently present in OPL-style problems and are useful for credit, auditing, and licensing clarity.

### Minimal recommended set

```text
## Date('YYYY-MM-DD')
## Author('Full Name')
## Institution('Institution or group')
```

### Source and textbook provenance (use when adapted)

Use these when the problem is adapted from a textbook, worksheet, or other source.

```text
## TitleText1('Title of source')
## EditionText1('Edition')
## AuthorText1('Author(s)')
## Section1('Section identifier')
## Problem1('Problem identifier')
```

### Rules

- If adapted, also state that in DESCRIPTION.
- Empty strings are acceptable when you do not know the details, but do not invent information.
- Use a real date when known. Prefer ISO format: YYYY-MM-DD.

---

## 5) Optional header tags you may encounter

These vary by collection. Use them only if your corpus expects them.

- `## DBcourse(...)` or course tags: often local, not recommended for portability.
- `## Level(...)` or difficulty tags: only if your workflow uses them.
- `## Language(...)`: if multilingual content is supported.
- `## Commentary(...)`: keep short. Prefer adding context to DESCRIPTION instead.

When adding optional tags, keep them consistent and avoid creating new tag dialects without a corpus-wide decision.

---

## Tagging quality rules

1. DBsubject reflects the discipline and course area, not the scenario.
2. KEYWORDS reflect methods and concepts, not superficial nouns.
3. Use consistent capitalization and spelling across the corpus.
4. Prefer stable, existing label strings over "better" new strings.
5. Avoid "meta noise" labels like WeBWorK or ZZZ-Inserted Text in new content.

---

## Guidance on "Grade level" and education-style tags

In the upstream OPL, many "grade level" subjects are K-12 tagging (for example Middle School, Elementary School). Those are not pedagogy categories.

For new problems:

- Use grade-level subjects only if the problem is genuinely K-12 targeted and your library uses those labels.
- Do not use grade-level tags as a substitute for a discipline tag.

---

## A copy-paste template

```text
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
## TitleText1('')
## EditionText1('')
## AuthorText1('')
## Section1('')
## Problem1('')
```

---

## Related PGML HTML whitelist note

This guide is about headers, but remember that PGML output is filtered by an HTML whitelist in this install. Tags like `table`, `tr`, `td`, and `th` are blocked and will warn or render badly. For safe layout patterns, see [MATCHING_PROBLEMS.md](MATCHING_PROBLEMS.md) and [WEBWORK_PROBLEM_AUTHOR_GUIDE.md](WEBWORK_PROBLEM_AUTHOR_GUIDE.md).

---

## Header review checklist

Before publishing:

- DESCRIPTION exists and is short, accurate, and code-free.
- KEYWORDS exist and are concept-focused.
- DBsubject uses an existing corpus string.
- DBchapter and DBsection are present when you can assign them confidently.
- Author and date are present when known.
- No smart quotes or odd characters were introduced into header lines.
