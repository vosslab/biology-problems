# Design decisions

<!-- VENDORED HEADER: START -->
Record each durable decision about how this code and repository are shaped, once it is settled, with
the reasoning a later reader needs. Guidance Neil Voss states belongs in
[HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md), dated history in `docs/CHANGELOG.md`, open discussion in
`docs/active_plans/decisions/`. [PROPAGATED HEADER - ENTRIES BELOW ARE YOURS]
<!-- VENDORED HEADER: END -->

Write each decision as a level-three heading with these four fields. `Owner` names the
authoritative code or contract document, rather than a person.

```markdown
### <decision title>

**Decision.** <the durable direction>

**Why.** <the reason it was chosen>

**Consequence.** <the constraint a future change preserves>

**Owner.** <the authoritative code or contract doc>
```

## Software design

### Restriction-digest cut placement

**Decision.** Restriction-digest questions keep one map-and-gel format.
Placement proposes mixed, readable maps. Evaluation checks validity, then
the mode's required answer shape. At most half of the correct distinct
bands may also appear in the distractor digest
(`shared_correct_fraction <= 0.5`). Difficulty is the fragment list and
distinct-band set. Full rules live in
[CUT_PLACEMENT.md](../problems/molecular_biology-problems/restriction_enzymes/CUT_PLACEMENT.md).

**Why.** Two circular cuts produce only complementary sizes `{d, L-d}`, so
raising length with two sites per enzyme leaves the reasoning unchanged.
The key comes from the named enzyme alone. Rigorous items use co-migrating
equal fragments as one band.

**Consequence.** Update
[CUT_PLACEMENT.md](../problems/molecular_biology-problems/restriction_enzymes/CUT_PLACEMENT.md)
first, then the generators.

**Owner.** [CUT_PLACEMENT.md](../problems/molecular_biology-problems/restriction_enzymes/CUT_PLACEMENT.md)



## Dependencies

## Generated artifacts
