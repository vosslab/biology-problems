# Markdown style

> This file is vendored. Local changes can and will be overwritten by propagation.

Keep documentation concise, scannable, and consistent.

## Standard

- Follow the [GitHub Flavored Markdown specification](https://github.github.com/gfm/) for Markdown
  syntax.
- Use GitHub Flavored Markdown by default.
- Use extensions beyond GitHub Flavored Markdown only when the target explicitly supports them.
- Treat this guide as a short set of repository conventions, not a restatement of the specification.

## Content

- Use ASCII or ISO-8859-1 source characters.
- Escape other characters with HTML character references such as `&alpha;` and `&beta;`.

## Headings

- Use sentence case.
- Start at `#` for the document title, then `##`, `###` as needed.
- Keep headings short (3-6 words).

## Lists

- Prefer `-` for bullets.
- One idea per bullet.
- Keep bullet lines short; wrap at ~100 chars.

## Code

- Use fenced code blocks with language where practical.
- Use inline backticks for file paths, CLI flags, and identifiers.

## Tables and diagrams

- Use ASCII-only tables and diagrams. Do not use Unicode box-drawing or checkmark symbols.
- For boxed layouts, use `+`, `-`, and `|` inside fenced code blocks.
- Replace checkmarks with `OK`, `YES`, or `[x]` and crosses with `NO`, `FAIL`, or `[ ]`.
- For progress bars or fills, use `#` and `.` (or `-`) instead of block characters.
- Use tables for tabular data, not page layout.
- If the content is tabular, prefer GitHub Flavored Markdown pipe tables unless alignment in a
  fenced `text` block is required.
- Keep tables simple, with one clear header row.
- Introduce each table with a descriptive heading or sentence because GitHub Flavored Markdown has
  no caption syntax.
- Use semantic HTML or an appropriate publishing pipeline when a table needs a caption, row
  headers, multi-level headers, or explicit header associations. Follow the
  [W3C accessible tables guidance](https://www.w3.org/WAI/tutorials/tables/).

Simple table:

| Field | Description |
| --- | --- |
| input | Path to input file |
| output | Path to output file |

## Links

- Use relative links inside the repo.
- Prefer descriptive link text, not raw URLs.
- When referencing another doc, always link it (avoid bare filenames).
- Links must work when committed and browsed on github.com. GitHub resolves relative URLs against
  the file containing the link, so use a path relative to that file, not the repo root.
- When linking from the repo root into `docs/`, include `docs/` in both the link text and URL. For
  example, use `[docs/FORMAT.md](docs/FORMAT.md)`.
- When linking between files in the same folder, use the bare filename in both the link text and
  URL. For example, use `[PYTEST_STYLE.md](PYTEST_STYLE.md)`, not a redundant `docs/` prefix.
- Link text should match the URL filename so readers see the exact file being referenced.
- `tests/test_markdown_links.py` enforces local link existence, repo containment, traversal, and
  path-like link text.

## Examples

- Show a minimal example before a complex one.
- Label sample output explicitly if needed.

## Tone

- Write in the present tense.
- Prefer active voice.
- Avoid filler and speculation.
