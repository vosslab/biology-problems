# Plan: Explore Pedigree Quality Through Bounded Multiobjective Local Search

## Context

The current generator produces biologically and pedagogically valid pedigrees, but valid examples vary considerably in visual interest. Previous experiments found useful signals, especially affected placement and outside affected reach, without establishing a reliable general "interestingness" formula.

The existing polisher improves a narrow class of structural defects by adding terminal children. Its offspring-probability results support further investigation: among 1,000 paired rigorous pedigrees, p < 0.05 occurred in 31 originals and 33 polished results. Those observations do not establish that more aggressive optimization will remain statistically credible.

The next experiment should investigate how much quality can be extracted from a valid starting pedigree through local editing. It should preserve several promising alternatives rather than allow one imperfect score to determine the entire trajectory.

The historical top 100 from 10,000, with mean Luna overall rating 3.94, provide a useful reference population. They are not a calibrated quality threshold. Contemporary blind review must establish whether new results approach that population.

## Objectives

- Determine whether local editing improves independently reviewed pedigree quality.
- Compare scalar optimization, Pareto survivor selection, and selection without aesthetic preference under comparable search budgets.
- Identify which mutation families produce useful changes, including interactions between mutations.
- Detect cases where numerical improvement fails to produce visual improvement.
- Measure biological validity, outcome-selection effects, computational cost, and available optimization headroom.
- Produce a reproducible experimental foundation from which a small production polisher can later be selected.

## Design Philosophy

Apply **Use the scientific method**, **Dream big**, and **Keep It Simple** together: explore powerful edits, preserve the evidence, and let results decide what deserves production complexity.

### What the books contribute

**Represent quality as a vector.** Chapter 2 of *Linear Algebra for Data Science with Python* describes vectors as representations of data points and features. This supports retaining separate measurements instead of immediately collapsing them into one weighted score. Its discussion of correlation and projection supports examining overlap among those measurements. It does not establish that any particular feature predicts pedigree quality. Sources: `/Users/vosslab/nsh/MARKDOWN_BOOKS/linear_algebra/Linear_Algebra_for_Data_Science_with_Python-2026.md`, sections on vectors/features (line 445) and correlation/projection (line 1247).

**Treat edits as graph transformations.** *Modern Graph Theory Algorithms with Python* motivates using graph representations to study relationships and biological systems. Our application is to make pedigree transformations explicit: what relationships changed, what biological states changed, and which descendants must be reconsidered. The book motivates the representation; it does not validate our mutation operators. Source: `/Users/vosslab/nsh/MARKDOWN_BOOKS/graph_theory/Modern_Graph_Theory_Algorithms_with_Python-2024.md`, network-science discussion (line 118).

**Acknowledge imprecise quality judgments.** Section 1.1 of *Fuzzy Graph Theory: Applications to Global Problems* introduces partial membership for concepts with ambiguity or vagueness. This supports treating "interesting," "balanced," and "good use of space" as uncertain judgments rather than exact biological properties. It does not justify implementing fuzzy membership curves before we have evidence for them. Source: `/Users/vosslab/nsh/MARKDOWN_BOOKS/graph_theory/Fuzzy_Graph_Theory_Applications_to_Global_Problems-2023.md` (line 177).

The bounded Pareto archive is a separate algorithmic choice. Dominance-based local search maintains alternative nondominated solutions while exploring their neighborhoods. We will test whether that choice helps this application. [Pareto local-search research](https://doi.org/10.1007/s10732-011-9181-3).

## Scope

- Build an experimental local-search runner using the existing pedigree representation, transmission model, acceptance checks, renderer, and measurements.
- Implement independently testable presentation, genotype, resampling, and structural mutations.
- Compare search strategies on shared starting pedigrees.
- Preserve originals, proposals, survivors, biological outcomes, rendered images, and blind reviews.
- Produce a reviewed-quality comparison and a concrete recommendation for subsequent production work.

## Non-Goals

- Change production ranking or polishing during this investigation.
- Introduce fuzzy logic, learned weights, a new graph framework, or a general-purpose optimization dependency.
- Generate another 10,000-case corpus before using the existing preserved data.
- Treat p-values as proof of unbiased sampling or as aesthetic rewards.
- Broaden the initial experiment to matching, easy, or bonus pedigrees.
- Require every measured feature or proposed mutation to survive into the final design.

## Current State Summary

The initial workload remains rigorous identification pedigrees:

- Exactly five generations.
- Between 23 and 26 people.
- Existing founding-couple, total-couple, and sibship-size bounds.
- Existing teaching answer and inheritance mode.
- Existing biological and layout requirements, including affected presence in the last two generations.

The current scalar score is:

```text
S(P) = progression(P)
       - mean_row_density(P)
       - 0.1 * outside_affected_reach(P)
```

The renderer already responds to sibling ordering and uses constrained alignment. Presentation experiments should exercise that machinery before proposing another layout system.

The offspring diagnostic uses actual parental genotypes and sex-by-phenotype categories. It compares observed sibships with independent fixed-cross simulations. It is not a full ancestry-resimulation test and cannot detect every change within an unaffected genotype category.

## Architecture Boundaries and Ownership

Keep the experiment in a new subdirectory of the existing sibling `pedigree-aesthetics` workspace. This is not a new repository.

Use ordinary functions and the existing `Family`, `Case`, and `AcceptedCase` objects. Avoid a plugin system or a general-purpose optimization framework.

Separate four responsibilities:

1. Proposal generation: describe and apply one mutation to a copy of a candidate.
2. Evaluation: validate biology, teaching, difficulty, and layout; calculate measurements.
3. Survivor selection: implement scalar, Pareto, or random selection.
4. Recording and review: preserve states, render images, prepare blind assignments, and join ratings afterward.

Each candidate record needs enough information to reproduce and interpret it:

- Starting-case and parent-candidate identifiers.
- Operation and its affected people or unions.
- Proposal seed.
- Complete relationships, sexes, genotypes, and relevant ordering.
- Acceptance result and rejection reasons.
- Raw measurements and search-selection outcome.
- Proposal/evaluation counts and timing.

Use original genotype records, not compact-cache witnesses. A compatible reconstructed genotype can imply different expected offspring probabilities.

### Mutation contracts

| Family | Initial operations | Biological consequences |
| --- | --- | --- |
| Presentation | Reverse or exchange sibling-order segments; reorder founder-family blocks | None: retain people, relationships, sexes, and genotypes |
| Sibship reassignment | Exchange genotype states between same-sex siblings | Preserve the source cross and its genotype counts |
| Descendant propagation | Propagate a sibling reassignment through descendant branches | Resample affected descendants from updated parents |
| Descendant resampling | Regenerate one descendant branch from unchanged upstream parents | Preserve relationships and sexes; sample a different genetic realization |
| Growth | Add terminal offspring; add a mate and offspring to an eligible individual | Add biological states using existing sampling authorities |
| Pruning and replacement | Remove terminal people or a pendant terminal family; combine removal and growth | Change workload allocation while retaining preset bounds |

"Branch balancing," "couple promotion," and "generation redistribution" are strategies for choosing locations for these operations. They should not become separate implementations of the same mutation.

A subtree moved on the page is a presentation edit. A subtree assigned different parents is a different biological operation. Reparenting existing subtrees and exchanging established mates remain follow-up possibilities rather than ambiguously entering the first implementation.

### Presentation edits

- Change ordering inputs that the renderer actually honors.
- Keep every parent-child and mating relationship unchanged.
- Re-layout and run the existing collision and connector checks.
- Record no-op proposals where an ordering change produces the same displayed arrangement.
- Preserve the existing symbol sizing and line-width behavior.

Do not introduce arbitrary coordinate displacement that bypasses family alignment.

### Genotype reassignment and propagation

The principal genotype treatment includes downstream consequences.

1. Select same-sex siblings with different genotypes.
2. Exchange their complete allele tuples.
3. Derive their visible observations from those genotypes.
4. Find the union of their descendant sets.
5. Process descendants in generation order.
6. Sample each affected descendant once using its updated parental genotypes and existing sex.
7. Preserve independently marrying-in founders.
8. Re-evaluate the complete pedigree.

When branches converge, process the shared descendant once using both current parents. Do not resample the same person independently from two traversal paths.

Terminal-only permutations provide a useful control. They must not replace the branch-propagating treatment.

### Structural edits

Growth follows the existing biological authorities:

- New offspring sex is sampled with equal male/female probability.
- Genotypes come from weighted Mendelian transmissions.
- New spouses follow the generator's existing spouse-genotype policy.

Pruning begins from structural eligibility, not a rule that unaffected people are useless.

Support two narrowly defined removal operations:

- Remove a terminal child when the retained sibship and complete pedigree remain valid.
- Remove a pendant family consisting of a marrying-in spouse and terminal offspring, retaining the original individual and their ancestry.

Allow atomic removal-plus-growth proposals so pedigrees already at 26 people can redistribute their population. Evaluate the completed proposal against the workload bounds; an intermediate construction step is not itself an emitted pedigree.

## Quality Representation and Search Mechanics

### Raw quality record

Preserve the existing measurements, including:

- Progression, shrink, adjacent-generation imbalance, and generation sizes.
- Row densities, width, parent gaps, and existing connector measurements.
- Coupled fraction, branching, and existing structural counts.
- Outside affected reach, affected fraction, and affected-region coverage.
- Current scalar interestingness.
- Probability diagnostics.

Do not assume every measurement has a useful monotonic direction.

### Initial Pareto objectives

Use three existing signals:

```text
q(P) = (progression(P), -outside_reach(P), affected_region_fill(P))
```

The displayed directions are local working hypotheses for the initial Pareto search. Individual measures are useful, but they can stop helping or become harmful at extremes; do not interpret these directions as globally monotonic truths. Keep the raw values in every candidate record.

Use the existing affected-region definition: two generations by four sibling pitches, counting occupied person-containing regions. Preserve its current anchoring and record the known boundary sensitivity.

Density, width, shrink, and other features remain diagnostic initially. Late affected presence remains a validity requirement rather than another redundant objective.

This vector is a testable starting hypothesis. It is not a declaration that these three dimensions fully describe quality, nor that further progression, affected-region fill, or reductions in outside reach always improve a diagram.

### Metric response and overshoot

Treat each established metric as meaningful evidence whose relationship to perceived quality may flatten or reverse at extremes reached during polishing. Randomly generated corpora may not reach those extremes, so corpus-only correlations do not establish a safe optimization direction.

- Preserve per-round trajectories for all raw measurements and blind ratings.
- During the discovery pilot, deliberately review endpoint candidates and intermediate checkpoints that span the observed metric extremes, including apparent overshoots.
- Compare metric values with blind ratings using coarse bins and smoothed plots as exploratory diagnostics; show sample counts and uncertainty.
- Use pilot evidence to identify likely plateaus or reversals before freezing confirmation. Do not guess preferred ranges in advance, add hand-set fuzzy membership functions, or fit new weights against confirmation results.
- Keep the existing combined scalar score as a comparator. Its weighting formula remains unproven even when its component metrics carry useful information.

If the pilot indicates that a proposed Pareto direction rewards harmful overshoot, document and freeze a justified revision before confirmation. Otherwise keep the initial direction for the confirmatory comparison and report the discrepancy.

### Pareto archive

Candidate A dominates B when A is no worse on all three objectives and strictly better on at least one.

- Start with the original pedigree.
- Retain nondominated candidates from parents and offspring.
- Limit the active archive to six candidates.
- When necessary, truncate using objective-space crowding distance.
- Normalize neighbor gaps by the observed range of each objective solely for crowding calculations; ignore constant dimensions.
- Resolve equal crowding distances with seeded randomness.

Crowding is used to preserve a spread of alternatives, not to invent another quality score. This follows the standard role of crowding in bounded multiobjective survival selection. [Official algorithm documentation](https://pymoo.org/algorithms/moo/nsga2.html).

Do not merge biologically distinct states merely because their quality vectors are equal. Prefer coverage of distinct vectors when space is limited, then use remaining capacity for alternative states.

### Search arms

| Arm | Survivor rule | Purpose |
| --- | --- | --- |
| Original | No editing | Paired baseline |
| Current polisher | Existing production behavior | Practical baseline |
| Scalar search | One champion under the unchanged production score | Test aggressive optimization of the current proxy |
| Pareto search | Up to six nondominated alternatives | Test retaining multiple quality tradeoffs |
| Random-survivor search | Up to six valid alternatives selected without quality preference | Separate mutation/search breadth from aesthetic selection |

The random arm is a control, not an assumption that all reachable pedigrees are sampled uniformly.

The scalar and Pareto arms use different objective representations. A difference between them establishes a difference between strategies, not proof that archive size alone caused it.

### Search budget and proposal policy

Use eight rounds and up to 100 proposals per round across the entire active population. The budget is 800 proposals per starting pedigree and search arm.

- Generate each round's proposals from that round's starting survivors.
- Select parent states uniformly.
- Select uniformly among mutation families with available proposals, then select an eligible local edit.
- Use the same proposal policy and mutation menu across experimental search arms.
- Count failed and rejected proposals against the budget.
- Record actual work when a neighborhood is exhausted.

For scalar search, select the best candidate from the incumbent and that round's proposals. Keep the incumbent on a score tie.

For Pareto and random search, select survivors after the round from the union of parents and valid offspring.

Evaluate each distinct stochastic edit once per exact parent state. Do not reroll an already attempted edit because its biological outcome was unattractive. A genuinely changed parent state may create a new proposal.

Preserve checkpoints after every round. Budget exhaustion and sampled-neighborhood exhaustion are different outcomes; neither proves a global optimum.

## Milestone Plan

| Milestone | Title | Summary | Goal |
| --- | --- | --- | --- |
| M1 | Freeze evidence and inputs | Capture source state, corpus, definitions, and assignments | Reproducible starting point |
| M2 | Implement and verify mutations | Build proposal functions and shared evaluation | Correct candidate transformations |
| M3 | Run the discovery pilot | Exercise operators and search strategies on 20 cases | Discover defects and misleading directions |
| M4 | Run frozen confirmation | Apply the frozen experiment to 80 held-out cases | Independent comparison |
| M5 | Analyze and recommend | Join blind ratings, diagnostics, and trajectories | Evidence-based production recommendation |

### M1: Freeze evidence and inputs

**Depends on:** none.

Use the recent 1,000-case dataset containing original unpolished genotypes.

Select 100 starting pedigrees:

- 50 from the lower score quartile.
- 50 from the middle half.
- Equal representation of the five inheritance modes.
- Rank within mode and use seeded random tie handling.

Assign two cases per mode and sampling band to the pilot: 20 total. Reserve the remaining 80 for confirmation.

Verify that reconstructed inputs still pass current requirements. Report any drift; do not silently replace failed inputs after examining search results.

Record code versions, feature definitions, random seeds, rubric, and historical reference identities.

**Done when:** the corpus can be reconstructed with original genotypes and assignments are frozen.

**Parallel-plan ready:** no. Later work depends on this shared authority.

### M2: Implement and verify mutations

**Depends on:** M1.

Build independent presentation, genetic, and structural proposal modules with one shared evaluator and recorder.

The evaluator must explicitly verify hidden-genotype transmissions. Visible compatibility alone is insufficient: it could be satisfied by a different genotype witness.

Preserve the intended answer and existing supported teaching profiles and compatible-mode set. Compare semantic profile presence, not diagnostic count strings.

**Done when:** representative proposals demonstrate their intended change, preserve their declared invariants, and produce clear rejection reasons when invalid.

**Parallel-plan ready:** yes, up to four lanes: presentation, genetics, structure, and shared evaluation/search infrastructure. Each lane owns its files; the integration owner controls shared interfaces.

### M3: Run the discovery pilot

**Depends on:** M2.

On the 20 pilot cases:

- Exercise every mutation family independently before combining them.
- Record feasibility, rejection reasons, score/vector changes, runtime, and biological effects.
- Run the scalar, Pareto, and random search arms.
- Obtain blind reviews of pilot outputs.
- Inspect numerical extremes and examples where measurements and reviewers disagree.

Do not eliminate an operation solely because the current scalar score fails to reward it.

If an operation is defective, fix it and rerun the affected pilot comparisons. If the objectives appear misleading, document that result and freeze a revised hypothesis before confirmation. Do not repeatedly tune against the confirmation cases.

**Done when:** the implementation is correct, practical runtime is measured, and the confirmation procedure is recorded.

**Parallel-plan ready:** limited. Generation must precede rendering; independent image review can then run in parallel.

### M4: Run frozen confirmation

**Depends on:** M3.

Apply the frozen strategies to all 80 reserved cases. Retain unchanged and unsuccessful cases in every denominator.

Preserve the full candidate history, round checkpoints, and final survivors. Do not replace unfavorable results or grant one method extra search because its outputs look weak.

**Done when:** all declared cases and arms have completed or have an explicit recorded failure, and blind review is complete.

**Parallel-plan ready:** yes. Case searches are independent; blinded review batches are independent. Keep manifest assembly and identity mapping under one owner.

### M5: Analyze and recommend

**Depends on:** M4.

Separate pilot discovery from confirmation results. Report results by starting-score band and inheritance mode, with population size and search cost available for interpretation.

**Done when:** the report answers which strategies improve reviewed quality, what biological selection effects appear, and what remains uncertain.

**Parallel-plan ready:** yes for statistical analysis and independent evidence audit; final interpretation belongs to the experiment owner.

## Blind-Review Protocol

Use Luna-6 subagents and the unchanged fixed rubric. Reviewers receive only anonymous final PNGs and rubric instructions.

They must not receive operation labels, scores, metrics, probabilities, pedigree rank, or before/after identities.

For each starting pedigree, review:

- The original.
- The current-polisher result.
- The scalar endpoint.
- One randomly selected random-search survivor.
- One randomly selected Pareto survivor as the primary Pareto output.
- Up to two additional randomly selected Pareto survivors for archive-quality analysis.

Choose review samples and construct the anonymous assignment manifest before opening any ratings. Freeze the manifest before ratings begin. Randomize assignments into balanced batches that mix treatment arms, inheritance modes, and historical references; do not assign reviewers to treatment arms. Place related variants from the same starting pedigree in separate batches so a reviewer does not see them together. Randomize image order within each batch.

Mix in 60 historical references: 20 from ranks 1-100, 20 from 101-500, and 20 from 501-1,000. These are reference bands; do not mislabel each band as the entire corresponding percentile population.

Re-review 20 reference images independently to expose reviewer variability. Treat repeated ratings as repeated measurements of the same image, not additional independent pedigrees.

Use the same rendering settings for candidates and references. Verify that PNGs correspond to their recorded biological states and contain the complete pedigree. Reuse a review when outputs are demonstrably identical; preserve all treatment mappings.

At the planned maximum of 100 cases, the main assignments comprise seven images per case (original, current-polisher, scalar, random-survivor, primary Pareto, and two additional Pareto survivors), or 700 assignments. Add 60 historical-reference assignments and 20 independent repeat assignments for a maximum of 780 main assignments, before extra pilot checkpoints or operator-specific images. The actual load will be lower when fewer Pareto survivors are available or displayed outputs are demonstrably identical and can share a review, while preserving all treatment mappings.

## Biological Credibility and Statistical Interpretation

### Mandatory biological checks

Impossible genotypes or transmissions are correctness failures. They do not become acceptable because a p-value or aesthetic score is favorable.

Preserve:

- Valid genotype domains for inheritance mode and sex.
- Valid parental transmissions.
- Full penetrance and existing mutation assumptions.
- Teaching answer and evidence requirements.
- Existing later-spouse restrictions.
- Difficulty and layout requirements.

### Probability diagnostics

Calculate the existing diagnostic for original states, accepted search checkpoints, and final outputs.

Report:

- Pedigree-wide and worst-sibship p-values.
- Fractions below 0.05 and 0.01 as descriptive comparisons, not acceptance rules.
- Sex and phenotype/genotype outcomes against cross-specific expectations.
- Proposed versus retained outcomes.
- Effects by mutation family and inheritance mode.

Add a temporary conditional genotype log-likelihood calculation for fixed-structure comparisons. The sex-by-phenotype diagnostic cannot see all carrier-versus-noncarrier changes.

Condition that likelihood on the stated founder genotypes and existing sexes. Do not compare raw likelihoods across different pedigree sizes as if their scales were equivalent.

Keep these distinctions explicit:

- A valid Mendelian proposal need not be retained without bias.
- Source-sibship probability preservation does not establish whole-pedigree probability preservation.
- The fixed-cross diagnostic does not resimulate consistent ancestry.
- Selecting candidates by p-value would itself change the output distribution.

Use the full preserved 1,000-case dataset as the baseline/current-polisher reference. Experimental probability comparisons use the actual search cohort and survivors. Do not disguise the cost of extending every search arm to another 1,000 cases as a cheap diagnostic calculation.

## Analysis and Success Criteria

### Primary quality outcome

Compare paired overall-usefulness ratings between originals and each method's preselected primary output.

Report paired changes and 95% bootstrap intervals, resampling starting pedigrees within inheritance-mode and sampling-band strata. Keep all variants from a starting pedigree together.

Report interest, balance, and readability alongside overall usefulness. A rise in overall rating should not conceal a readability decline.

### Frontier quality versus reviewer-assisted selection

Report separately:

1. Quality of the randomly selected primary Pareto survivor.
2. Mean and spread of reviewed Pareto survivors.
3. Best reviewed survivor from each archive.

The third measures available opportunity with reviewer assistance. It is not the quality an automatic production selector would necessarily achieve.

Do not compare "best of three Pareto reviews" with one scalar endpoint and describe that as a fair automatic-output comparison.

### Historical target

Compare new outputs with contemporaneously reviewed historical references. Report differences and uncertainty rather than declaring equivalence because an interval includes zero.

For descriptive attainment rates, predefine "reference-like" as meeting the contemporaneous reference median for both overall usefulness and interest. Report this label as a benchmark convention, not proof of membership in a true quality percentile.

For pooled top-5% and top-10% reference summaries, weight the sampled rank bands by their historical population sizes. Do not average the three equally sampled bands as though they were equally large.

Report historical score-threshold crossings separately.

### Mechanisms and metric exploitation

Examine:

- Which edits enter successful trajectories.
- Which edits create opportunities for later operations.
- How frequently each constraint blocks proposals.
- Whether gains require increasing population within the allowed band.
- Whether region-fill gains arise mostly from bin-boundary changes.
- Whether affected fraction rises without improved spatial organization.
- Whether Pareto survivors trade readability for affected coverage.
- Whether scores improve while reviews stagnate.

Use correlations and raw plots to examine redundancy and disagreement. Do not fit a new weighted score during confirmation.

Estimate candidate-pool savings from reviewed-quality yield and total computation cost. A search examining hundreds of variants has a real cost even if it begins with one pedigree.

## Test and Verification Strategy

Follow `docs/PYTEST_STYLE.md`: permanent tests must protect important, stable, regression-prone behavior.

During the experiment, use temporary checks for:

- Mutation preservation contracts and input immutability.
- Correct propagation through converging descendant branches.
- Complete hidden-genotype validation.
- Presentation edits leaving biology unchanged.
- Same-sex source-sibship permutations retaining genotype counts.
- Correct Pareto dominance, constant-objective handling, and archive bounds.
- Search-budget accounting and reproducibility.
- PNG-to-state correspondence and review-data joins.

Run small hand-checkable examples before corpus runs. Reuse existing biological authorities instead of writing a parallel inheritance implementation.

Do not permanently pin experimental budgets, archive size, exact score improvements, corpus proportions, or review outcomes. Promote tests only when a behavior is adopted into production and earns durable protection.

Run the repository suite if shared repository code changes. Record one-time experiment verification separately from permanent-suite results.

## Work Packages

| Package | Owner | Depends on | Deliverable |
| --- | --- | --- | --- |
| WP1: Freeze inputs and protocol | Experiment lead | None | Corpus, split, references, definitions, seeds |
| WP2: Implement presentation edits | Layout implementer | WP1 | Ordering mutations and preservation checks |
| WP3: Implement genetic edits | Genetics implementer | WP1 | Sibship reassignment and correct propagation |
| WP4: Implement structural edits | Structural implementer | WP1 | Growth, pruning, and capacity exchange |
| WP5: Build evaluator and searches | Integration owner | WP1; integrates WP2-WP4 | Shared evaluation, three search strategies, records |
| WP6: Prepare and review images | Rendering owner plus independent Luna reviewers | WP5 | Verified PNGs, blind assignments, ratings |
| WP7: Analyze and audit evidence | Analyst plus independent reviewer | WP6 | Results, limitations, reproducibility audit |
| WP8: Close documentation | Experiment lead | WP7 | Report, changelog, next-step recommendation |

## Risk Register

| Risk | Evidence to watch | Response |
| --- | --- | --- |
| Goodharting several metrics | Numerical gains with flat or worse reviews | Preserve examples; reconsider objectives after confirmation |
| Biased outcome selection | Proposed/retained biological distributions diverge | Identify responsible operations; do not hide the shift with a p-value cutoff |
| Region-boundary exploitation | Coverage improves mainly after small ordering changes | Inspect geometry and report sensitivity |
| Redundant Pareto objectives | Objectives move together and archive diversity is superficial | Document redundancy; simplify in a later frozen experiment |
| Reviewer drift | Historical references or repeated anchors shift | Use contemporary comparisons and report uncertainty |
| More survivors create an unfair advantage | Only best-of-archive results look strong | Keep primary-output and reviewer-assisted results separate |
| Computational growth | Proposal cost rises sharply for structural combinations | Measure during pilot; revise the budget for all arms before confirmation |
| Too little structural freedom | Most cases blocked by population or couple limits | Report the constraint as an experimental finding |

## Documentation Close-Out Requirements

Preserve:

- The frozen protocol and book citations.
- Source-state information and reproducible commands.
- Original and candidate genotype records.
- Proposal, rejection, and survivor histories.
- Search trajectories and before/after galleries.
- Anonymous review manifests, raw ratings, and identity mappings.
- Analysis tables, uncertainty estimates, and concrete disagreements.
- Runtime and storage measurements.
- A concise recommendation for production or the next experiment.

Update the repository changelog with the investigation and its result. Keep bulky artifacts in the sibling experimental directory `../pedigree-aesthetics/local_search/`.

Completion does not require proving that Pareto search works. It requires a credible answer about whether it improves reviewed quality, which mutations contribute, what biological selection effects remain, and what the evidence supports doing next.
