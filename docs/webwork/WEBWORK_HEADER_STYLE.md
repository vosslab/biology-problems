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

1. `TITLE('...')` line (required)
2. `DESCRIPTION` block (required)
3. `KEYWORDS(...)` (strongly recommended)
4. `DBsubject(...)`, `DBchapter(...)`, `DBsection(...)` (required for repo tagging)
5. `Level(...)` (required for this corpus)
6. Attribution and provenance fields (recommended, but valuable)
7. `Language(en)` (required for this corpus)

Order is not technically required, but the canonical order below is recommended for consistency.

---

## 1) TITLE('...') line (required)

### Purpose

Short, student-facing title that mirrors ADAPT's title field.

### Format

Use a single line:

```text
## TITLE('Short single-sentence title')
```

### Content requirements

- One sentence.
- 90 characters or fewer.
- Describe the task, not the story wrapper.
- Include the discipline or course context when the title appears in a large bank
  (for example, "Genetics: X-linked inheritance from fly offspring counts").
- Avoid filler words like "practice" in titles.
- Avoid commas if they make the title run long.

---

## 2) DESCRIPTION block (required)

### Purpose

Human-readable summary for instructors and reviewers.

### Format

Use `## DESCRIPTION` and `## ENDDESCRIPTION`. Put plain English in between.

### Content requirements

- 2 to 3 sentences.
- Describe the task, not the story wrapper.
- Include constraints that affect adoption (rounding requirement, unit expectations, domain restrictions).
- If adapted, say "Adapted from ..." or "Based on ...".
- Prefer a single paragraph line within the DESCRIPTION block rather than one
  sentence per line.

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

## 3) KEYWORDS(...) (strongly recommended)

### Purpose

Search terms for discoverability.

### Format

A single line:

```text
## KEYWORDS('keyword1','keyword2','keyword3')
```

### Rules

- Use 3 to 5 keywords (prefer 3 when possible).
- Use concepts and techniques, not character names or story nouns.
- Prefer lower-case unless capitalization matters.
- Prefer canonical spellings: integration by parts, chain rule, partial fraction, eigenvalues.
- Avoid duplicates already implied by DBsubject, but include key techniques.

### Example

```text
## KEYWORDS('derivative','polynomial','evaluate at a point','power rule')
```

---

## 4) Library classification: DBsubject / DBchapter / DBsection (required)

### Purpose

Primary browse and analysis hooks. These are the most useful tags for corpus statistics and discovery.

### Format

```text
## DBsubject('Calculus - single variable')
## DBchapter('Derivatives')
## DBsection('Basic differentiation rules')
```

### Rules

- Use one DBsubject, one DBchapter, one DBsection for every problem in this repo.
- The upstream OPL corpus is math-heavy, so use the local life science strings listed below.
- Match existing strings used elsewhere in this repo.
- Choose the most specific correct subject that still fits typical course organization.
- If uncertain, search for existing usage and copy the exact string.
- Do not leave empty strings. If you are unsure, pick the closest existing label and revise later.

### Local DBsubject values for biology-problems

Use these DBsubject values for life science content:

- Anatomy and Physiology
- Biochemistry
- Bioinformatics and Computational Biology
- Biomedical Sciences
- Biostatistics
- Cell Biology
- DNA Profiling
- Ecology
- Evolution
- Immunology
- Inheritance Genetics
- Laboratory Techniques
- Microbiology
- Molecular Biology
- Neuroscience
- Organismic Biology

If a new subject is needed, add it to this list so tags remain consistent.

### Common pitfalls

- Quoted duplicates like `'Algebra'` vs `Algebra`. Pick one style and stick to it.
- Empty subject strings. Do not leave empty strings; choose the closest existing label.

---

## 5) Problem level: Level(...) (required)

OPL uses a 1-6 scale aligned to Bloom's revised taxonomy order (Remember,
Understand, Apply, Analyze, Evaluate, Create). Use these life science oriented
meanings (calculations, when present, are typically lab-only).

- Level 1 (Remember): recall a term, definition, or basic fact.
  Verbs: recall, define, label, list, match, identify.
- Level 2 (Understand): describe or explain a concept, classify or interpret a
  simple representation (for example, identify a technique or classify a
  molecule). Verbs: explain, summarize, interpret, classify, compare.
- Level 3 (Apply): use rules or methods in a direct way, typically routine and
  low-stakes (for example, apply Mendelian rules or use a lab formula).
  Verbs: apply, use, determine, solve, choose.
- Level 4 (Analyze): interpret data or results and connect to a biological
  conclusion (for example, read a graph, compare treatments, or infer phenotype
  effects). Verbs: analyze, compare, contrast, categorize, infer.
- Level 5 (Evaluate): justify a choice, critique evidence, or defend a
  conclusion (for example, assess experimental design or argue between
  competing explanations). Verbs: evaluate, justify, critique, defend.
- Level 6 (Create): combine ideas to design or propose a new biological plan or
  model (for example, design a study or propose a pathway).
  Verbs: design, propose, formulate, develop, create.

Format:

```text
## Level(2)
```

### Level assessment examples (biochemistry and molecular biology)

These examples help calibrate level assignments for chemistry-heavy biology questions:

**Level 1 (Remember):**
- "Which amino acid has a sulfur atom in its side chain?"
- "What is the name of this functional group?" (given a labeled structure)
- "List the three components of a nucleotide."

Direct recall, no inference or multi-step reasoning needed.

**Level 2 (Understand):**
- "Classify this molecule as a carbohydrate, lipid, protein, or nucleic acid." (given structure)
- "Explain why histidine acts as a buffer at physiological pH."
- "Which of these amino acids is hydrophobic?"

Requires understanding and classification, but pKa values or group assignments are given.

**Level 3 (Apply):**
- "Calculate the net charge on lysine at pH 7.4 given pKa values: 2.18 (COOH), 8.95 (NH3+), 10.53 (side chain)."
- "Determine the number of peptide bonds in a tetrapeptide."
- "Using the genetic code table, translate this mRNA sequence."

Direct application of rules or formulas with clear instructions and provided data.

**Level 4 (Analyze):**
- "Histidine has pKa values of 1.82, 6.00, and 9.17. Determine the protonation state at pH 7.4."
- "Compare the solubility of Arg-Asp-Glu at pH 3.0 vs pH 11.0."
- "Analyze this gel electrophoresis result to determine which protein is largest."

Student must infer relationships (which pKa → which group), analyze multiple factors, or
synthesize information from different knowledge domains.

**Level 5 (Evaluate):**
- "Justify why an Arg-Glu-Asp peptide would be more soluble than Leu-Val-Ile at pH 7.0."
- "Critique this proposed mechanism for enzyme inhibition based on the kinetic data."
- "Evaluate which buffer system (acetate vs phosphate) would be better for maintaining pH 6.5."

Requires defending a conclusion, evaluating competing explanations, or justifying choices
based on multiple criteria.

**Level 6 (Create):**
- "Design a peptide sequence that would be maximally soluble at pH 7.0 and explain your design."
- "Propose an experimental protocol to determine the pKa of an unknown amino acid."
- "Create a metabolic pathway diagram showing how glucose is converted to lactate."

Requires synthesizing knowledge to create novel solutions, designs, or models.

---

## 6) Attribution and provenance fields (recommended)

These fields are frequently present in OPL-style problems and are useful for credit, auditing, and licensing clarity.

### Minimal recommended set

```text
## Date('YYYY-MM-DD')
## Author('Full Name')
## Institution('Institution or group')
```

In this repo, use the author/institution listed in `docs/AUTHORS.md` unless a
different author is explicitly required for a specific problem. Current default:

```text
## Author('Dr. Neil R. Voss')
## Institution('Roosevelt University')
```

### Contact links (comments only, required)

Use plain comment lines (not tags) and avoid email. The GitHub link is required:

```text
# https://github.com/vosslab
# https://bsky.app/profile/neilvosslab.bsky.social
# https://www.youtube.com/neilvosslab
```

### Source and textbook provenance (use when adapted or mapped)

Use these when the problem is adapted from a textbook, worksheet, or other source.

```text
## TitleText1('Title of source')
## EditionText1('Edition')
## AuthorText1('Author(s)')
## Section1('Section identifier')
## Problem1('Problem identifier')
```

For this repo, the common textbook titles are:

- Upper-Level Introductory Biochemistry
- Advanced Genetics: Mechanisms of Inheritance and Analysis
- Writing Automated Questions using WeBWork in ADAPT

Use TitleText1/2/3 (and matching EditionText/AuthorText/Section/Problem tags) to
map to multiple texts when appropriate.

### Rules

- If adapted, also state that in DESCRIPTION.
- Empty strings are acceptable when you do not know the details, but do not invent information.
- Use a real date when known. Prefer ISO format: YYYY-MM-DD.

---

## 7) Language: Language(en) (required)

Use ISO 639-1 language codes. For English, use:

```text
## Language(en)
```

---

## 8) License comments (required, not an OPL tag)

OPL does not define a standard license tag. Use plain comment lines to state
licensing for the problem text and any included images or code. The required
license statement for this repo is CC BY 4.0 / LGPL v3.

Example:

```text
# This work is licensed under CC BY 4.0 (Creative Commons Attribution 4.0
# International License).
# https://creativecommons.org/licenses/by/4.0/
# Source code portions are licensed under LGPLv3.
```

If a problem includes a separate image license, add an extra comment line for
the image.

---

## 9) Optional header tags you may encounter

These vary by collection. Use them only if your corpus expects them.

- `## DBcourse(...)` or course tags: often local, not recommended for portability.
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
## TITLE('Short single-sentence title')
## DESCRIPTION
## Two to three sentences describing the task and any adoption-relevant constraints.
## ENDDESCRIPTION
## KEYWORDS('keyword1','keyword2','keyword3')
## DBsubject('Subject')
## DBchapter('Chapter')
## DBsection('Section')
## Level(2)
## Date('YYYY-MM-DD')
## Author('Dr. Neil R. Voss')
## Institution('Roosevelt University')
## Language(en)
```

Optional textbook mapping (use only when applicable):

```text
## TitleText1('Upper-Level Introductory Biochemistry')
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
- DBsubject uses an existing repo string from the local list above.
- DBchapter and DBsection are present (no empty strings).
- Level is set using the 1-6 scale.
- Author and date are present when known.
- Language(en) is present.
- No smart quotes or odd characters were introduced into header lines.
