# Pedigree review evidence

This is the durable evidence record for visual review and production choices. Ratings use the fixed
[PEDIGREE_RUBRIC.md](PEDIGREE_RUBRIC.md). Biological correctness and teaching acceptance are hard
gates; visual scores do not replace them. The [production pipeline](PEDIGREE_PIPELINE.md),
[polishing](PEDIGREE_POLISHING.md), and [ranking](PEDIGREE_RANKING.md) documents define current
behavior. This page records why those choices were made and what the measurements can support.

## Initial topology score tests

The first development exercise used 24 accepted medium pedigrees and two reviewers. A proposed
`unions - generations - maximum sibship` score failed its fresh comparison: only 9 of 16 pairwise
judgments favored its higher-scoring image, and both reviewers rejected the higher score in
rigorous identification, bonus, and rigorous matching. The revised formula
`4 * branch_balance - maximum_sibship` did not generalize: only 7 of 16 workload-spanning judgments
favored it (one tie),
although a separate eight-judgment comparison that held maximum sibship fixed favored higher
balance in 7 cases. These small exploratory comparisons rejected those formulas; they did not
establish a replacement. See sibling `pedigree-aesthetics/CALIBRATION.md`.

## Top-1,000 rigorous cohort

A frozen score selected 1,000 cases from a 10,000-case rigorous pool. All 1,000 images were
blindly rated once, with a 500/500 development/validation split assigned before review. This
selected cohort is not a random-generation baseline. Its top-100 images averaged 3.940 overall
versus 3.684 among the next 900, but that contrast cannot show improvement over random valid
pedigrees.

## Affected reach and coverage

Earlier proposals to combine geometry or coverage signals also met limits. In the reused 1,000
ratings, affected occupancy in native 2-generation by 4-sibling-pitch regions correlated with
interest at +0.343/+0.347 across development and validation, but after controlling review batch,
mode, people count, affected fraction, and outside affected reach, associations were +0.137/+0.098.
The mean grid-origin half-pitch shift was about 0.06 and some measurements changed under
reflection. Outside affected-reach fraction correlated with interest at -0.300/-0.290 in those
halves, but its relationship to readability was positive; unaffected relatives can remain useful
teaching evidence. These reused splits are descriptive consistency checks, not independent
confirmation.

## Polished-200 corpus

In the separate fresh polished-200 corpus, progression correlated with overall ratings at
+0.236/+0.231 for rigorous/bonus, and mean row density at -0.296/-0.204. Progression's interest
correlations were +0.261/+0.267 while its readability correlations were -0.100/-0.099. These
directions informed feature inspection, but did not establish a clearly superior sort; the frozen
simple alternatives gave no decisive validation win. The 200 images had no unpolished controls,
and 84/100 rigorous and 81/100 bonus cases still had negative progression after polishing. The
historical 215-case review corpus (108 rigorous, 83 bonus, 24 matching) versus the new 200-case
corpus had mean overall scores of 3.863 versus 3.840 for rigorous and 3.873 versus 3.880 for bonus.
This is descriptive, not a paired treatment effect: reviewers, sampling, and review contexts
differed. Polishing edits
qualified in 50/100 rigorous and 58/100 bonus cases. The coarse visual ratings and two-child cap
constrain what this study can conclude. The
signals are described further in sibling `pedigree-aesthetics/POLISHED_CORPUS.md`,
`pedigree-aesthetics/top1000/spatial/REPORT.md`, and
`pedigree-aesthetics/AFFECTED_REACH.md`.

## Search review

The local-search discovery pilot included 20 independent starting pedigrees, two in each of five
modes by two starting-rank bands. It used 251 rating assignments across 21 batches; assignments are
not independent cases. On the fixed four-item rubric, mean overall change from original was +0.25
for the current polisher, +0.20 for scalar search, +0.15 for random search, and +0.20 for Pareto
primary selection. All three search arms had 95% case-cluster intervals including zero. An
earlier report statement that gave scalar +0.20 and Pareto +0.15 was corrected; these figures retain
the accepted report's corrected values. Search versus the current polisher showed no clear
incremental overall benefit in this small pilot. The pilot supported proceeding with the frozen
confirmation design, not changing its objectives.

The held-out confirmation then reviewed 80 independent starting pedigrees, eight per mode-by-band
cell, with 536 blinded assignments including historical references and repeat-reference
occurrences. Pareto primary selection improved overall usefulness by +0.325 points (case-cluster
95% CI +0.200 to +0.450) versus original; versus the current polisher it was +0.275 (+0.163 to
+0.388). Readability changed by -0.100 (-0.200 to 0.000) versus original. The current polisher's
overall change was +0.050 (-0.038 to +0.138); scalar was +0.025 (-0.125 to +0.163), with readability
at -0.250 (-0.388 to -0.113). Thus Pareto improved selected visual ratings in this frozen cohort,
with a readability tradeoff, but the result does not validate a general quality scale or
prospective production yield.

Search also shifted diagnostic probability outcomes. Fixed-cross Monte Carlo p-values below 0.05
occurred in 18/80 Pareto outputs versus 2/80 originals and 1/80 current-polisher outputs; all
primary outputs passed mandatory genotype and transmission checks. This is evidence that selecting
valid candidates can condition the observed outcome distribution. It is not evidence of impossible
biology, and probability scores remain diagnostic, not aesthetics rewards or acceptance gates.
The separate paired 1,000-case rigorous check of ordinary polishing found p<0.05 in 31/1,000
originals and 33/1,000 polished outputs, and p<0.01 in 9/1,000 both before and after, with no
impossible transmissions. That near-equality is a
different comparison and cohort from the search result; together they show that the measured
selection shift was specific to the Pareto-selected cohort, not evidence that every polishing or
selection stage has the same effect. The paired polishing results are in sibling
`pedigree-aesthetics/offspring_probability/REPORT.md`.
The same confirmation report estimates 32.1% fewer starts for a descriptive reference-like target
only under linear-yield and equal-baseline-cost assumptions; actual production savings and
end-to-end break-even remain unknown. The one-time reports are sibling
`pedigree-aesthetics/local_search/PILOT_REPORT.md` and
`pedigree-aesthetics/local_search/REPORT.md`.

For interpretation, the 251 pilot assignments and 536 confirmation assignments must not be
reported as independent sample sizes. Starting pedigrees are the units used for case-cluster
uncertainty. Luna-6 reviewers rated final images only, with neutral IDs and the fixed rubric; they
saw no metrics, formulas, or before/after identities. These reviews are not student or instructor
ratings. Repeated references show between-reviewer differences, not an estimated reviewer-variance
model. The former scalar score's Spearman association of 0.14 with overall ratings came from 496
candidate states in this local-search analysis, not from the 1,000-case cohort. Heuristic
improvements could diverge from readability and overall usefulness. The local-search experiment
remained experimental and was not adopted as production search.

## Bottom-empty repair

In the historical 1,000 reviewed rigorous pedigrees, normalized largest bottom-anchored empty
rectangle fraction had a modest inverse association with balance in development and validation
(Spearman rho -0.320/-0.286). Associations were weaker for overall usefulness (-0.152/-0.141),
interest (-0.067/-0.094), and near zero for readability (-0.077/-0.045). This motivated treating
lower empty space as a geometry feature, not as a complete visual-quality score.

A subsequent blind feasibility study used 100 fresh accepted rigorous pedigrees, 20 per inheritance
mode. The exploratory trigger was 0.2257808, the historical development Q3; 40 cases exceeded it
and 13 changed. Twelve reviewers rated the 113 unique images under the fixed rubric; unchanged
cases retained their baseline rating, so paired n remained 100. Across all cases, mean overall
change was +0.09 (95% case-bootstrap interval +0.02 to +0.18), including 87 zero-change cases.
Among the 13 changed cases it was +0.69 (+0.23 to +1.15). Mean balance change was +0.08 overall
and +0.62 among changed cases. These are a modest, small-sample pilot signal, not proof of student
benefit or a general response to the geometric measure.

The 22.58% historical Q3 cutoff and the production 12% trigger/target are distinct. The user
selected 12% as a practical production constant; it was not fitted to these ratings, and it has no
new blind review of its own. The 100 preserved rigorous sources were each replayed with two fixed
stage seeds (200 paired runs per order, not 200 independent source pedigrees). Repair-then-polish
reached 12% in 40/200 runs versus 34/200 for polish-then-repair. In repair-then-polish order, the
later polishing stage raised the fraction by 0.003233 in two runs, but no run that had reached
12% crossed back above it. This supports repair before ordinary polishing as a bounded operational
choice, not a claim that 12% is an aesthetic threshold. Production applies it only to the rigorous
workload and retains the person/generation caps. Evidence: sibling `pedigree-aesthetics/bottom_empty_space/REPORT.md`,
`pedigree-aesthetics/downward_repair/REPORT.md`, and repository archive
[pedigree_consolidation.md](../../../docs/archive/pedigree_consolidation.md).

The 100-case study proposed 15 children and retained 14 after required acceptance gates. Four of
15 proposals and three of 14 retained children were affected, against summed sex-conditional
expected counts of 4.5 and 4.0. The sole rejected child was an affected female whose addition
failed autosomal-dominant affected-sex balance. These counts illustrate conditioning by mandatory
gates; they do not estimate a general outcome bias. Among all 100 cases, fixed-cross p<0.05 counts
were 3 before and 3 after repair. Never infer unconditional offspring probabilities from accepted
output counts.

## Production sorter

The current sorter averages five favorable percentile ranks within each eligible candidate pool:
outside affected reach, affected-region fill, generation progression, mean row density, and excess
bottom-empty fraction above 12%. A retrospective re-ranking of 1,000 reviewed top-pool pedigrees
found top-quartile overall means of 3.888 versus 3.824 in development and 3.928 versus 3.888 in
validation for equal-five versus the former sorter. Mode-balanced differences were smaller:
3.781 versus 3.728 and 3.851 versus 3.845. Readability was slightly lower for equal-five in both
pooled splits. This is a modest retrospective comparison on an already selected corpus, not a
prospective gain or independent confirmation.

The percentile score is recalculated from current pool membership, used only to order already
eligible candidates, and is not a calibrated quality score. The ranking and geometry definitions
are in [PEDIGREE_RANKING.md](PEDIGREE_RANKING.md) and [PEDIGREE_LAYOUT.md](PEDIGREE_LAYOUT.md).
Evidence and frozen split details are in repository archive
[pedigree_consolidation_progress.md](../../../docs/archive/pedigree_consolidation_progress.md)
and sibling `pedigree-aesthetics/consolidation/`.

## Terminal-frontier comparison

The terminal-frontier constructor tests a design hypothesis: reserving terminal families before
building the middle generations may make the final generation span a more useful horizontal
frontier. The first comparison used 100 accepted targets: five seeds per inheritance mode, for
baseline and frontier construction at easy and bonus identification. It also prepared 10 blinded
pairs for visual review. This is a moderate construction test, not a student-outcome study or a
general quality calibration. Detailed provisional output is in
`output_pedigree_frontier/comparison/report.md` and `results.json`; the blinded judgment is in
`output_pedigree_frontier/comparison/visual_review.md`.

All 100 targets were accepted. The 50 frontier candidates passed their designated-endpoint check,
and no repair or polishing proposal was rolled back for breaking that contract. No downward-repair
additions occurred in these easy and bonus cases. For easy, median pre-polish bottom-empty fraction
`E` was 0.0861 for baseline and 0.0923 for frontier; both methods had zero polishing additions in
all 25 cases. The initial construction measure therefore showed no easy-workload gain. Median
attempts were 6 versus 7, with maxima of 188 versus 187. Median constructor-only times were 0.0032
seconds for baseline and 0.0136 seconds for frontier; median total measured target times, including
instrumented stages, were 0.0063 and 0.0190 seconds. Median people counts were 14 versus 13.

For bonus, median pre-polish `E` was 0.1373 for baseline and 0.0138 for frontier, about 90% lower
in this sample. Median terminal sibship count was 2 versus 10. Polishing added children in 8/25
baseline cases (13 additions) and 7/25 frontier cases (10 additions), a small difference that does
not establish reduced dependence on polishing. Median attempts were 16 versus 4, with maxima of 69
versus 76. Median constructor-only times were 0.089 seconds for baseline and 0.322 seconds for
frontier; median total measured target times, including instrumented stages, were 0.327 and 0.839
seconds. Median people counts were 78 versus 86. Both methods remain inside the same preset limits,
but the different person and terminal-family distributions constrain direct interpretation of `E`
and runtime.

The blinded review of the 10 pairs preferred frontier construction in four of five bonus pairs; the
baseline was preferred for X-linked dominant. Across the five modes, ordinal readability ratings
were 3, 3, 3, 3, 4 for frontier and 2, 3, 4, 3, 3 for baseline. These are one reviewer's judgments
on 900-pixel PNGs, not calibrated scores or student outcomes. The combined evidence supports
enabling frontier construction for bonus identification only, with random terminal counts 9 or 10.
Easy remains on baseline construction because its numerical comparison showed no construction
advantage. Polishing frequency is supporting context; the 8/25 versus 7/25 bonus result is not a
demonstrated meaningful reduction. Keep polishing and all existing acceptance gates. Do not infer
student benefit or universal visual improvement from this sample.

## Terminal-frontier interest review

A second, matched blind review did not find higher structural interest for terminal-frontier
construction. At the accepted pre-repair checkpoint, reviewer A rated baseline/frontier interest
3.12/3.04 on average (frontier minus baseline -0.08; 3 wins, 17 ties, 5 losses across 25 matched
blocks). Reviewer B rated them 4.00/3.96 (-0.04; 6 wins, 13 ties, 6 losses). These small ordinal
differences do not support an interest advantage. The earlier five-pair bonus review above is a
separate, unmatched trial and should not be pooled with these ratings.

| Reviewer | Accepted interest: baseline / frontier | Frontier minus baseline | Wins / ties / losses | Final interest: baseline / frontier | Final difference |
| --- | ---: | ---: | ---: | ---: | ---: |
| A | 3.12 / 3.04 | -0.08 | 3 / 17 / 5 | 3.12 / 3.12 | 0.00 |
| B | 4.00 / 3.96 | -0.04 | 6 / 13 / 6 | 4.00 / 3.96 | -0.04 |

The review covered 25 matched blocks, one per combination of five inheritance modes and five exact
target sizes (70, 76, 82, 88, and 94 people). Each pair also matched generation depth (6 or 7) and
founding-couple count (3 or 4); the remaining bonus bounds were held fixed. Two fresh, independent
GPT-6 Luna instances using the same model rated the 68 unique accepted and final images at 1800
pixels using the unchanged four-dimension rubric. The 25 blocks, not the 50 reviewer-by-block
ratings, are the matched sample units. Accepted checkpoints are the primary comparison; final images are secondary because
polishing can add people. In final interest ratings, A's means were 3.12/3.12 and B's were
4.00/3.96 for baseline/frontier.

Other dimensions show a reviewer difference worth retaining: at acceptance, A's balance,
readability, and usefulness changes were +0.04, +0.04, and +0.04 points, while B's were +0.60,
+0.36, and +0.56. This suggests little overall change to A and clearer, more useful layouts to B;
it does not change the flat interest result. Polishing added people in 11/25 baseline cases
(18 total) and 7/25 frontier cases (7 total). All seven changed frontier cases gained one person;
four changed baseline cases gained one, and seven changed baseline cases gained two. The small,
coarse ordinal sample does not establish that frontier construction can replace polishing.

The corrected logging run used the frozen seeds and configuration, but the first provisional
run's per-attempt records were missing and its data and packets were removed before replay. Exact
record-for-record equivalence cannot be verified; the corrected run is the study dataset, not a
second sample. The 25 fixed-size blocks are a narrow, unranked workload, not the natural production
size distribution. Ratings are judgments by two reviewers, not student or instructor outcomes,
and do not calibrate general visual quality. No p-values or production-policy change are warranted.
The final analysis report and complete paired gallery are in sibling
`pedigree-aesthetics/terminal_frontier_interest/REPORT.md` and
`pedigree-aesthetics/terminal_frontier_interest/gallery.html`. The report and `summary.json` were
reconciled against these reviewer-level results; the report also includes mode and agreement
summaries, final-stage dimensions, and within-arm changes.

## Evidence sources

The numerical summaries above are self-contained for future maintainers. Detailed case-level data,
review packets, and analysis scripts remain in the adjacent `pedigree-aesthetics` research checkout
and are not required for production. Archived implementation plans are linked for decision history;
the durable production contracts remain the current pedigree reference documents.
