# Pedigree difficulty and construction

This page owns procedural workload presets and family construction. The production order and bank
lifecycle are in [PEDIGREE_PIPELINE.md](PEDIGREE_PIPELINE.md); biological and teaching filters are
in [PEDIGREE_BIOLOGY.md](PEDIGREE_BIOLOGY.md).

## Workload presets

Choose `-E` / `--easy` (default), `-M` / `--medium`, or `-R` / `--rigorous` for any command.
`write_pedigree_to_pattern.py` also accepts `-b` / `--bonus` for one large identification pedigree;
bonus is unsupported in five-diagram selection and matching.

| Preset | MC generations / people | Matching generations / people |
| --- | --- | --- |
| Easy | 3 / 12-15 | 3 / 10-11 |
| Medium | 4-5 / 16-22 | 3 / 12-15 |
| Rigorous | 5 / 23-26 | 3-4 / 16-18 |
| Bonus | 6-7 / 60-100, identification only | Not supported |

These are practical reading-workload bands, not calibrated student-difficulty measurements. More
people increase scanning, couples and founders increase branching, and generations increase
tracing depth. Bands can overlap. All presets retain the same biology, visible-evidence, sex-balance,
carrier-hiding, and layout checks. Rigorous adds more structure to inspect, not weaker evidence.
Review examples and student response data when tuning them.

The editable `DIFFICULTY_SETTINGS` and `MATCHING_SETTINGS` in
[difficulty.py](pedigree_lib/difficulty.py) also constrain construction. Counts are inclusive and
sampled jointly within feasible bounds; some combinations are impossible.

| Preset | MC seed / total couples | Matching seed / total couples | Later children per couple |
| --- | --- | --- | --- |
| Easy | 1 / 3-4 | 1 / 2-3 | 1-3 |
| Medium | 1-2 / 4-6 | 1-2 / 3-4 | 1-4 |
| Rigorous | 2-3 / 6-8 | 2-3 / 4-5 | MC 1-4; matching 1-3 |
| Bonus | 3-4 / 18-26 | Not supported | 1-5 |

| Preset | MC root children | Matching root children |
| --- | --- | --- |
| Easy | 2-4 | 2-5 |
| Medium | 2-5 | 2-6 |
| Rigorous | 2-4 | 2-4 |
| Bonus | 2-5 | Not supported |

Total couples includes seed couples, unions joining descendants of founding families, and marrying-in
unions. For easy, medium, and rigorous, seed sibship counts use the bounds in the table; medium MC
allows two to five, and medium matching two to six. Bonus uses its separate two-to-five root bound.
Selection and matching share seed-couple count across their assembled diagrams. Counts are
resampled after rejection within the same preset.

## Family construction

Procedural families plan unions and reserved child slots before instantiating people. A constrained
search selects branches within people and sibship budgets; remaining child slots fill the requested
population band. One or more seed couples begin in generation I. When several founding families
are requested, different generation-II children from adjacent families can marry to join them.
Further descendants may marry unrelated people. A generated student case is connected and has no
consanguinity. Authored fixtures may include separate families and cousin unions.

Sex roles are assigned before simulation. Founder genotypes are seeded by the requested mode rules;
phenotypes then follow Mendelian transmission. Whole candidates are rejected and resampled under
the acceptance filters, so accepted outputs are conditioned on those filters. See
[PEDIGREE_BIOLOGY.md](PEDIGREE_BIOLOGY.md) for the mode rules and teaching gates.

Library callers can pass the same bounds to `procedural_family`, `simulate_case`, and
`generate_case`:

```python
case = questions.generate_case('autosomal recessive', rng,
    min_people=23, max_people=26, generations=5,
    seed_couples=2, couples=(6, 8), children=(1, 4), root_children=(2, 4))
```

Equal bounds request exact counts, such as `couples=(6, 6)`. Impossible settings raise an explicit
error. To change existing flags, edit the preset tables rather than adding a parallel configuration.

## Construction limits

The constructor does not use fixed teaching cores or complete-tree templates. Arbitrary clinical
family generation, half-sibships, and multiple partners are outside scope. Homework selects one
connected family and hides carrier status; see [PEDIGREE_BIOLOGY.md](PEDIGREE_BIOLOGY.md).
