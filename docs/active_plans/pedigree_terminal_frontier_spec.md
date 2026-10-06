# Pedigree final-generation plan

## Status

This is a proposed design. It does not describe the current generator. It does not change a
preset, replace the current constructor, or remove the current repair step.

The current constructor starts with generation-I couples and works downward. It can create a
valid deep family with too few people in the last generation. The current system can then try to
improve the empty lower part of the diagram after layout.

This design adds a planned set of people in the last generation before the middle of the family is
built. The aim is to make a broad last row part of the family structure, rather than something the
system tries to fix later.

This document is a working decision record. Move settled parts into the focused pedigree documents
only after the code is built and measured.

## Goal

Build one connected, biologically valid pedigree that:

- Starts with the required generation-I foundation couples.
- Has a chosen number of planned people in the last generation.
- Puts each planned person in a different sibship.
- Lets those sibships have any legal number of children, including one.
- Uses the existing family and layout code rather than fixed drawing positions.
- Keeps sex, genotype, phenotype, and question scoring separate from this layout plan.

The system should make the last row wide through normal family relationships. It must not add
people only because a layout check found a large empty area at the bottom of the diagram.

## Plain terms

### Planned final-generation person

A planned final-generation person is a child slot that the planner chooses before it creates people.
After the family is built, that slot becomes one normal person in the pedigree.

The label is used only while planning. It does not mean the person is:

- An only child.
- Affected or unaffected.
- Male or female.
- A carrier or a non-carrier.
- Marked, highlighted, or treated differently in the student-facing question.

Every person in the finished pedigree has equal standing. The planner removes or ignores this
planning label before normal output, caching, rendering, and scoring.

### Sibship

A sibship is the ordered list of children from one union. A planned person belongs to the sibship
that contains that person's child slot.

A sibship may contain one child or several children, subject to the preset's normal child-count
limits. The planner does not prefer singleton sibships. It also does not require siblings.

### Main rule

Each planned final-generation person belongs to a different sibship.

This is the only special family rule for these people. It does not require:

- A planned person to be an only child.
- A sibship to contain only one planned person because it has only one child.
- Every last-generation sibship to contain a planned person.
- Planned people to share parents, grandparents, or one foundation couple.
- One terminal family per foundation couple.

If there are `N` planned people, there are at least `N` different last-generation sibships that
contain them. This makes `N` count separate family endpoints, not children from one large family.

### Foundation couple

A foundation couple is a generation-I union selected by the current difficulty preset. The new
planner keeps the current number of foundation couples and uses the current genotype simulation
later.

### Child slot

A child slot is a temporary record such as `(union_plan_id, child_index)`. It helps the planner
connect families before it creates `Person` objects. A child slot has no sex, genotype, phenotype,
or visible symbol while the plan is being made.

### Last-generation union

A last-generation union has one or more children in the deepest generation. It may contain one
planned child and other children. It is not the same thing as a planned person.

## What this design does not do

This design does not:

- Add an unknown-sex pedigree symbol. The current model has male and female people only.
- Pick sex, phenotype, genotype, carrier status, or answer evidence while choosing the last-row
  plan.
- Promise that all people in the last generation are planned people.
- Use fixed x/y coordinates to place people.
- Replace the current `Family` model.
- Change child-count limits merely to make the first experiment succeed.
- Claim that every generated diagram will look better before measurements support that claim.
- Make the current repair step create the planned last row. Repair may remain as a fallback while
  experiments show whether it is still needed.

## Inputs

The planner uses the current difficulty settings plus a small new policy for the last generation.

### Current settings

The current settings include:

- Number of generations.
- Total-person range.
- Number of foundation couples.
- Total-union range.
- Child-count range for non-foundation unions.
- Child-count range for foundation unions.
- Seeded random number generator.

`pedigree_lib/difficulty.py` remains the source of these settings. The new planner must not copy
or redefine their meaning.

### New policy

The new policy needs:

- `planned_final_count`: the number `N` of planned people in the last generation.
- `different_sibships`: true for the first version of this design.
- A rule for spreading the selected last-generation sibships across the family.
- A rule for preserving their left-to-right relationship order without using coordinates.

The first experiment should sample `N` randomly within a tested range. It must not cycle through
values based on question number.

Possible first ranges:

| Workload | Planned people in last generation | Status |
| --- | --- | --- |
| Easy identification | 2-3 | Test first |
| Bonus identification | More than 8 | Test first |
| Medium | Not set | Measure first |
| Rigorous | Not set | Measure first |
| Matching | Not set | Separate decision |

These are experiment settings, not present difficulty settings. They do not become production
constants until a measured test shows that they fit the preset's people, unions, and generation
limits.

## Required family rules

The planner may create a family only when all of these rules are true.

### Basic family rules

1. The family is connected.
2. The family has the requested number of generations.
3. Every union has one father role and one mother role.
4. Every non-founder person has exactly one parental union.
5. A person is a partner in no more than one union, matching the current model.
6. A child is exactly one generation below that child's parents.
7. The family has no ancestry loop or conflicting generation assignment.
8. The people, union, and child counts fit the selected preset.

### Planned-person rules

1. There are exactly `N` planned child slots.
2. Every planned slot is in the deepest generation.
3. No two planned slots are in the same child list.
4. Every planned slot becomes exactly one person in the final `Family`.
5. Each planned person's parents form a last-generation union.
6. Every sibship that contains a planned person stays within the ordinary preset child limits.
7. The planner does not favor one-child sibships and does not require extra siblings.
8. At least two planned people are required when the layout goal includes both outer ends of the
   final row.

## Ordering rules

The planner controls relationship order, not drawing coordinates. The current layout reads child
order from `Union.children`, so that order is part of the family data.

The planner must:

1. Produce an ordered list of planned last-generation sibships.
2. Keep that order when it creates each `Union.children` tuple.
3. Put a planned child on the outside edge of the leftmost planned sibship.
4. Put a planned child on the outside edge of the rightmost planned sibship.
5. Put the remaining planned sibships between those two.
6. Run the real layout after the family is built.
7. Check that the leftmost and rightmost displayed people in the deepest generation are planned
   people.

A planned order is not enough. Spouses, related branches, and the layout solver can change the final
positions. If the real layout does not place planned people at both ends of the deepest row, reject
that family plan and try another one. Do not move symbols by hand or add fixed coordinate overrides.

## Keep biology separate

The last-generation plan is about relationships and order. It must not change biology or question
quality checks.

After the family shape is built, the existing process still does this work:

1. Assign sexes to people whose sex was not already needed for a parent role.
2. Assign founder genotypes with the existing inheritance-mode rules.
3. Pass genotypes to children with the existing Mendelian functions.
4. Derive visible observations.
5. Run the current biology, teaching, rarity, difficulty, and layout checks.
6. Reject the whole candidate when a required check fails.

A planned person may be male or female, affected or unaffected, and a carrier when that inheritance
mode shows carriers. The planner must not use that later information to choose planned people.

If a complete candidate fails a biology or teaching rule, discard it through the normal retry path.
Do not redraw a planned person's sex or genotype until the result looks better.

## How to build the family

The planner fixes important top and bottom constraints before it fills in the middle. It does not
build `N` isolated ancestry trees from the bottom upward. It also does not build an unrestricted
family from the top downward and hope the last row will work out.

### Step 1: Choose a legal size

1. Select the current difficulty preset.
2. Sample its foundation-couple count, total-union count, total-person target, and generation
   depth using the current random rules.
3. Sample `N` from the tested range for this workload.
4. Stop early and choose another legal size if the budget cannot contain `N` different
   last-generation sibships.
5. Reserve enough unions and child slots for foundation couples, middle connections, and the
   selected last-generation sibships.

This early count check prevents a nearly complete family from running out of room for the planned
last-generation people.

### Step 2: Reserve the last generation

1. Create a plan for each generation-I foundation union.
2. Create `N` different union plans whose children will be in the deepest generation.
3. Mark one child slot in each of those unions as planned.
4. Give each of those unions its normal allowed child-count range. Do not set its child count to one
   because it contains a planned person.
5. Put the last-generation union plans in a left-to-right order.
6. Reserve the outside child order for the first and last planned sibships.

At this point, the planner knows how many distinct last-generation sibships it needs. It does not
yet know the full set of parents and ancestors between them and the foundation couples.

### Step 3: Connect the middle

Build the intervening generations so every selected last-generation union has a path back to the
foundation couples.

1. Work through the middle generations while keeping a possible connection for each selected
   last-generation union.
2. When a union needs a related parent, use an available child from an earlier union.
3. When a union needs an unrelated spouse, use the current model's normal later-spouse rule.
4. Let different last-generation branches share ancestors when a normal connected family needs it.
5. Use the current valid method, or an equally valid replacement, to join foundation lines.
6. Spread selected last-generation unions across available descendant branches. Do not attach them
   all to one early family branch when other branches are available.
7. Keep enough unused child capacity to meet every union's minimum child count and the selected
   total-person target.
8. Backtrack or discard the plan as soon as the remaining generations, partner roles, child slots,
   union count, or person count cannot connect all selected last-generation unions.

The direction is driven by constraints. The top foundation couples and the bottom planned people are
both known before the middle is complete.

### Step 4: Fill child lists

After the necessary connections exist:

1. Give every union its preset minimum number of children.
2. Keep the planned child in each selected last-generation sibship.
3. Distribute remaining people across child lists using the current bounded allocation rule.
4. Allow a selected last-generation sibship to receive more children when allocation chooses it.
5. Do not require or forbid those extra children.
6. Give sex roles only to children that must become parents in later unions.
7. Leave other child sexes open until normal person creation.
8. Check final people, unions, generation depth, and every child bound before creating people.

A planned person can therefore have no siblings or several siblings. The only special rule is that
another planned person cannot be in the same sibship.

### Step 5: Create and lay out the family

1. Create people from the completed child slots in stable ID order.
2. Assign sex to uncommitted people with the current unbiased rule.
3. Create unions in stable construction order.
4. Preserve the planned child order in every `Union.children` tuple.
5. Create a `Family` and run `Family.generations()`.
6. Run the existing layout code.
7. Require no layout errors.
8. Check the two outer people in the deepest displayed row.

If the last check fails, discard the topology and choose another one. Do not adjust coordinates after
biology has been simulated.

### Step 6: Simulate and evaluate

Reuse the current simulation and question evaluation after the new family shape is complete. Those
parts of the system must not know which people were planned when they choose genotypes,
transmissions, observations, or answers.

A candidate can meet the planned-person rules and still fail biology, teaching, rarity, or layout
checks. That is normal. Discard the complete candidate and try again through the existing retry
policy.

## What the layout should show

For `N >= 2`, planned people should reach both ends of the final row.

```text
last generation
P ... P ... P ... P
^                 ^
left end          right end
```

`P` means a planned person. The dots can be people or horizontal space. They do not require extra
siblings, affected people, or evenly spaced symbols.

### The plan guarantees

- Planned people are in different last-generation sibships.
- The planner supplies a left-to-right order for those sibships.
- The first and last planned sibships place their planned children toward the outside.

### The layout must prove

- The leftmost displayed person in the deepest generation is planned.
- The rightmost displayed person in the deepest generation is planned.
- The diagram has no layout errors.
- The selected design meets the measured final-row coverage goal for its experiment without direct
  coordinate changes.

### The plan does not guarantee

- Equal gaps between planned people.
- A fixed empty-space score for every candidate.
- A narrower or wider diagram overall.
- A better visual result until review data supports that claim.
- A final row containing only planned people.

The design is a testable idea: planning wide endpoints early may reduce large blank space at the
bottom. Measurements, not the design document, decide whether it helps.

## Difficulty settings

`N` depends on the workload. It is not decoration that should be applied everywhere.

### Easy

A first easy experiment can choose two or three planned people in different sibships. Easy has a
small family, so the experiment must check whether two, three, or a mix is still readable.

### Medium and rigorous

This specification does not set values for medium or rigorous. Those presets have their own people,
unions, generations, and teaching requirements. Measure them before enabling this feature.

### Bonus

A first bonus experiment can require more than eight planned people in different sibships. The
current bonus settings already allow a large family with many unions and generations. This design
does not require raising the child limit just because `N` is above eight: the breadth comes from
several last-generation families, while each family still follows its normal child limits.

That does not decide whether the current bonus child limit is ideal. Change that limit only after a
separate test of readability, biological plausibility, and student workload.

### Matching and selection

Matching and selection use different bounds. They must not inherit an identification setting by
accident. The first implementation can target identification only and measure other formats later.

## Code boundaries

The expected responsibilities are:

| Location | Responsibility |
| --- | --- |
| `pedigree_lib/difficulty.py` | Current bounds and, after validation, planned-person settings |
| `pedigree_lib/sources.py` | Plan unions and child slots, then create the family |
| `pedigree_lib/family.py` | People, unions, and family validation; no planned-person behavior |
| `pedigree_lib/layout.py` | Current layout and geometry checks; no fixed planned-person coordinates |
| `pedigree_lib/inheritance.py` | Current genotype simulation; no preference for planned people |
| `pedigree_lib/questions.py` | Current biology and teaching checks |
| `pedigree_lib/downward_repair.py` | Current fallback until evidence supports changing its role |
| `pedigree_lib/polishing.py` | Current bounded additions until separately reviewed |
| `tests/libs/pedigrees/` | Last-generation planning and behavior tests |

The planner may keep a private record of child slot IDs while constructing a family. Do not add this
record to `Family`, put it in the compact cache, or pass it to renderers. If an experiment needs to
inspect it, keep a temporary report keyed by candidate seed and generated person ID.

## Cache rules

The compact cache stores finished family data, not untested planning notes.

- A cached case does not need to prove it came from this new planner.
- Do not apply a new planned-person rule to old cache entries unless the cache contains enough data
  to verify it.
- Cached and fresh cases must still pass the same current biology, teaching, difficulty, and layout
  checks.
- If this design becomes required for production cases, make an explicit decision to version,
  expire, or bypass older cache entries.

## Failure handling

| Problem | Required response |
| --- | --- |
| `N` cannot fit in different last-generation sibships | Choose another legal size before creating people |
| Middle generations cannot connect all selected unions | Backtrack or discard the family plan |
| Child limits cannot meet the total-person target | Discard the plan before biology simulation |
| Parent sex roles conflict | Discard the plan before creating the family |
| `Family.generations()` rejects the family | Treat it as a construction bug and add a regression test |
| Layout fails or outer last-row people are not planned | Discard the topology; never move symbols directly |
| Biology or teaching check fails | Discard the complete candidate through the normal retry path |
| Final-row measurement is weak | Keep or reject only through normal acceptance and ranking rules; analyze the experiment separately |

No failure path may select or redraw genotypes to improve last-row shape.

## Tests

Permanent tests should check stable rules. Large sample measurements should stay outside the normal
test suite until the project has a measured production threshold.

### Small topology tests

Use small, readable fixtures to check:

1. The planner creates exactly `N` planned child slots.
2. Every planned slot is in the deepest generation.
3. Each planned slot has different parents from every other planned slot.
4. A planned person's sibship can have one, two, or more children within current limits.
5. No test treats a planned person as an only child by default.
6. The completed family is connected and has valid generation ranks.
7. No person becomes a partner in two unions.
8. The planner rejects impossible size budgets before creating `Person` objects.

### Ordering and layout tests

Use fixed, hand-checked family plans to check:

1. Planned child order survives creation of `Union.children`.
2. The layout has no collisions or unclear connectors.
3. The leftmost and rightmost deepest-row symbols are planned people.
4. A mirrored family keeps the same planned endpoints while swapping visual left and right.
5. A family whose normal layout fails the endpoint check is rejected rather than coordinate-edited.
6. Extra siblings in planned sibships remain allowed.

### Biology-separation tests

With the same family shape and seed rules, check:

1. Genotype transmission does not read planned-person labels.
2. Planned people can be affected or unaffected when the inheritance model allows both.
3. Planned people can be male or female when no parent role fixes their sex.
4. Existing inheritance and transmission checks still pass.
5. Teaching evaluation has no planned-person preference.

Use the real inheritance functions. Do not create a second simplified Mendelian implementation for
these tests.

### Sample measurements

For every targeted preset and inheritance mode, run a seeded sample large enough to report:

- Attempts and accepted cases.
- Rejections by topology, biology, teaching, difficulty, and layout reason.
- People, unions, last-generation unions, and final-generation people.
- Planned-person count and different-sibship compliance.
- Sibling count for each planned person.
- Whether planned people appear at both displayed ends of the final row.
- Bottom empty space before any downward repair.
- How often later repair or polishing changes the family.
- Runtime and retry cost.

Compare the current constructor and the new constructor with the same preset, inheritance mode,
sample size, and seed rules. Do not compare only selected attractive examples.

### Visual review

A low empty-space number is useful but does not prove that a pedigree is better. Use the current
pedigree review rubric on blinded samples. Report balance, readability, interest, and overall value
separately. Do not ship a more confusing family just because it has less blank space.

## First production trial

Do not replace the current constructor because a few prototype diagrams look good. A narrow first
production trial needs all of these results:

1. The selected preset and all five inheritance modes create accepted cases within the current retry
   limit.
2. Permanent tests prove the different-sibship rule without an only-child assumption.
3. Generated families stay within every current difficulty bound.
4. The real layout, not only the plan, places planned people at both final-row ends.
5. Biology and teaching checks stay independent of planned-person labels.
6. A matched experiment shows less of the relevant lower-row problem or less repair use without a
   meaningful readability loss.
7. Cache behavior is explicit.
8. The full repository test suite passes.
9. The changelog and focused pedigree documents describe measured behavior and limits accurately.

## Open decisions

These decisions need measurements before they are fixed:

1. Which workload should be first: easy, bonus, rigorous, or experiment-only?
2. What range of `N` works for medium and rigorous?
3. Should easy choose two and three equally, or weight one after testing?
4. Should bonus use a fixed minimum above eight, a range, or a value based on final-row capacity?
5. How should the planner spread selected last-generation sibships across descendant branches?
6. Should this feature affect candidate ranking after visual evidence, or only family construction?
7. When can downward repair become a fallback instead of a normal step for one workload?
8. Should older cached cases remain eligible if this feature becomes required?
9. Do any question formats become harder to read when the final row is broad?

## Current behavior

This document describes a proposed change. The current pedigree generator and its tests remain the
source of truth for current behavior.

After implementation and measurement, move settled behavior into the focused pedigree documentation,
record the decision, and archive this working record under `docs/archive/`.
