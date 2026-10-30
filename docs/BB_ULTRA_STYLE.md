# Blackboard Ultra style

Author Blackboard question HTML with **CSS declarations directly in each element's
`style="..."` attribute**. This is what "inline CSS" means in this repository.

These rules apply to question stems, choices, hints, tables, diagrams, and shared renderers
used by Blackboard generators and YAML banks.

## Element-local styling only

- Put CSS declarations in the styled element's `style` attribute.
- Do not emit `class` attributes, including empty classes or unused test markers.
- Do not emit `<style>` blocks or stylesheet `<link>` elements.
- A stylesheet written inside a Python string or HTML fragment is still a stylesheet.
- An element with both `class` and `style` still violates the no-classes rule.
- Use existing semantic attributes or necessary `data-*` metadata for test selectors.
  Metadata does not replace inline styling.

Allowed:

```html
<span style="color: #076DAD; font-weight: bold;">Gene A</span>
```

Forbidden, even if a matching stylesheet exists elsewhere:

```html
<span class="gene-a">Gene A</span>
<span class="gene-a" style="color: #076DAD;">Gene A</span>
<style>.gene-a { color: #076DAD; }</style>
<link rel="stylesheet" href="questions.css"/>
```

In Python HTML/SVG builders, assigning `node.set('class', ...)` is also forbidden.
SVG presentation attributes such as `fill`, `stroke`, and `font-size` remain valid;
they define appearance directly on the element without a stylesheet.

## Compact, readable tables

- Let ordinary tables size from their content. Avoid forced full width and fixed heights.
- Keep intentional dimensions when scientific geometry or aligned allele columns require them.
- Use modest cell padding. Extra padding repeated across many columns makes tables needlessly wide.
- Group related values with clear boundaries and compact spacing; use nested tables when they
  preserve a meaningful group, such as the alleles within one spore.
- Define text and background colors together for self-contained diagrams and tables.
- Keep gene colors consistent across labels, genotypes, and artwork. Pair color with text or
  symbols so the distinction does not depend on color alone.
- Use monospace for genotypes and sequences. Keep their alignment and readable text sizes.
- Preserve labels, counts, totals, and blank working cells when refining appearance.

Use the existing shared renderer when possible. Keep style strings local to that renderer;
do not introduce stylesheet machinery to avoid repeating a few declarations.

## PGML and local previews

PGML permits CSS classes, though they are discouraged. Its rules are separate from Blackboard
HTML; see [QUESTION_VOICE_GUIDE.md](QUESTION_VOICE_GUIDE.md).

Standalone galleries and local review pages may use stylesheets. Their exemption does not extend
to shared artwork or renderers that also produce Blackboard question content.

## Source check

[test_blackboard_inline_styles.py](../tests/test_blackboard_inline_styles.py) checks tracked
Python generators and YAML banks under `problems/`. It detects class attributes in markup,
ElementTree class assignments, style blocks, and stylesheet links. PGML converters and identified
standalone previews are excluded.

```bash
source source_me.sh && python3 -m pytest tests/test_blackboard_inline_styles.py -q
```

A failure identifies the source file and line. Move styling into `style="..."`, remove unused
classes, and update affected test selectors. Exempt a file only when it genuinely produces PGML
or a standalone preview, not to silence a Blackboard generator failure.

This is a static source check. It does not execute every generator or detect every possible
runtime construction. Inspect the changed generator's actual output as part of its focused checks.

Question wording and pedagogy remain covered by [QUESTION_VOICE_GUIDE.md](QUESTION_VOICE_GUIDE.md)
and [QUESTION_PEDAGOGY_GUIDE.md](QUESTION_PEDAGOGY_GUIDE.md).
