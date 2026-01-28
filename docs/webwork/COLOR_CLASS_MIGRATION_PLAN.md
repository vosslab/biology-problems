# Color Class Migration Plan (PGML Matching Sets)

## Goals
- Use CSS classes (not MathJax color) for matching-label coloring in PGML output.
- Preserve existing YAML replacement rules without a risky bulk refactor.
- Keep PGML output compatible with this install's HTML whitelist.

## Constraints (current install)
- MathJax/TeX color injected in PGML does not render reliably.
- PGML tag wrappers with span + CSS do render reliably.
- HTML tables (`table`, `tr`, `td`, `th`) are blocked and must be avoided.

## Current state
- YAML replacement_rules often wrap terms with `<span style="color: ...">`.
- Some replacement rules also expand content (entities, subscripts, bold).
- `yaml_match_to_pgml.py` strips HTML and converts sub/sup to Unicode.

## Plan

### 1) Keep YAML stable (no bulk edits)
- Do not rewrite existing YAML files now.
- Treat replacement_rules as the semantic content layer (expansions and fixes).

### 2) Add an explicit class-based color path (opt-in)
- Add an optional YAML block (tentative name: `color_rules`) that maps tokens
  to CSS class names.
- Only use class-based coloring when this block is present.
- This avoids "smart" guessing and preserves legacy behavior.

### 3) Optional strict conversion mode (future)
- Add a generator flag (tentative: `--color-mode class`) that will only convert
  replacement rules matching a very strict pattern:
  - A single span with a `color:` style and no other HTML tags.
  - Optional `<strong>` wrapper is allowed (translate to font-weight).
- If the rule does not match the strict pattern, keep inline output or leave it
  untouched, and log a warning.

### 4) Use HTML spans + `*` for variable content
- PGML parses once; tag wrappers built inside Perl variables are not re-parsed.
- Emit HTML spans (class or inline) and pass them through with `[$var]*` when
  the content lives in Perl arrays or variables.
- Prefer CSS classes; allow inline styles only as a fallback.

### 5) Sub/sup handling
- Convert `<sub>` and `<sup>` to Unicode digits and common signs.
- Map common letter subscripts where Unicode exists.
- Leave Greek letters on baseline (for example, `C<sub>&alpha;</sub>` -> `Calpha`).

### 6) Table guard
- If any text contains `<table`, `<tr`, `<td`, or `<th>`, skip class conversion for that
  string and route it to the niceTables conversion path instead of stripping it.
- Log a warning when the table shape is unsupported so these entries can be cleaned up.

### 7) Incremental migration
- When touching a YAML file, optionally add `color_rules` and remove redundant
  inline color spans in its replacement_rules.
- Keep changes small and local to reduce risk.

## Validation
- Use the color probe file to confirm CSS rendering in the target install:
  `problems/matching_sets/color_render_test.pg`.
- Spot-check at least one matching set with sub/sup and one with table content.

## Implemented flags (current)
- Generators default to inline color spans.
- `--no-color` disables coloring.
- `--use-colors` is an explicit enable (same as default).

## Open questions
- Final name of the new YAML key (`color_rules` vs `color_classes`).
- Class naming convention (palette-based vs meaning-based).
- Where to store shared CSS if we want a reusable palette across problems.
