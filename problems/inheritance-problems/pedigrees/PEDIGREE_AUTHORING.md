# Author pedigree families

Author relationships and visible observations in YAML. Both authored and procedural families pass
the acceptance rules in [PEDIGREE_PIPELINE.md](PEDIGREE_PIPELINE.md). Edit
[authored_cases.yml](authored_cases.yml) for library demonstrations and regression fixtures.
Homework commands use randomly generated families exclusively.

## Small example

This minimal autosomal-recessive teaching example has unaffected parents and affected offspring of
both sexes. It works for MC; matching additionally requires comparable three- or four-generation examples
for all five modes.

```yaml
cases:
- metadata:
    expected_mode: autosomal recessive
    note: Unaffected parents have affected offspring of both sexes.
  people:
  - {id: father, sex: male, affected: false}
  - {id: mother, sex: female, affected: false}
  - {id: daughter, sex: female, affected: true, label: II-1}
  - {id: son, sex: male, affected: true, label: II-2}
  unions:
  - father: father
    mother: mother
    children: [daughter, son]
    sibling_order: [daughter, son]
```

## People and unions

- `people` is a list, with a unique string `id`, `sex` (`male` or `female`), and boolean `affected`.
- Optional `carrier: true` means a known unaffected heterozygote. Absence does not mean noncarrier.
  This is a library demonstration feature: student commands hide carrier status and re-evaluate
  the answer. They exclude disconnected families and cases unclear without carrier disclosure.
- Optional `label` is plain text, up to 12 characters, attached permanently to the person ID.
- `unions` contains `father`, `mother`, and a list of child IDs. An empty child list is permitted
  for diagrams, but cannot supply transmission evidence.
- A person occurs in one parental child list and at most one reproductive union.
- A spouse with no recorded parents is a founder biologically, even when marrying into a later layer.
- Generation numbers are derived from parentage and partner relationships.
- Cousin unions reference the original cousin IDs. Never duplicate a person for drawing convenience.
- Multiple founding families use distinct IDs and ordinary unions in the same case.
- `sibling_order`, when present, must contain each child exactly once. It preserves an authored
  left-to-right order before optional whole-diagram mirroring. Without it, homework presentation
  may shuffle siblings.
- `metadata` is optional instructor information. `expected_mode`, if supplied, must agree with
  the independently evaluated answer. Metadata is not embedded in student drawings.

The inheritance engine accepts `affected: null` for an unknown phenotype and renderers show `?`.
The current homework profiles require complete phenotype observations and reject such cases.
No genotype, generation, grid character, or drawing coordinate belongs in the YAML format.

## Library fixtures only

Homework generators now use random families exclusively. Authored YAML remains available
for library tests and demonstrations through `questions.authored_cases(path)`; there is no
authored-bank command or source-selection flag. Render accepted library cases with
`svg_output.render_svg(case.diagram, case.case.observations)` for editable review.

Loading validates every authored case, including ones not randomly selected for that run. A malformed,
weak, tied, biologically unsupported, or unreadable case fails explicitly with its metadata and reasons.
Use the JSON rationale to inspect the inferred answer and compatible alternatives; open the SVG
in Inkscape to inspect editable shapes and labels. Keep the JSON instructor review files separate
from student distribution.

A typical prompt is "Which inheritance pattern is most likely demonstrated by this pedigree?"
Its five choices are autosomal dominant, autosomal recessive, X-linked dominant, X-linked recessive,
and Y-linked. The standard bptools anti-cheat settings and export options apply unchanged.
