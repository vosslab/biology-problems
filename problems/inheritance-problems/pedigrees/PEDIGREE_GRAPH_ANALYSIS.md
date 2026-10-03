# Pedigree graph analysis

Graph comparison and structural complexity are instructor diagnostics. They do not affect biology,
acceptance, or the production candidate sorter; see [PEDIGREE_RANKING.md](PEDIGREE_RANKING.md).

## Graph representation

[graphs.to_networkx](pedigree_lib/graphs.py) represents every person and union as separate nodes in
an undirected incidence graph. Edge attributes distinguish parent from child. This supports
multiple founders, marrying-in partners, and cousin unions without treating the drawing as the
relationship authority. Each call returns an independent NetworkX snapshot; changing the graph
cannot modify the family. Optional observation labels add sex and visible status, not hidden
observations or answer metadata.

Pairwise comparison prepares structural and visible graphs once per family per call, then reuses
them across pairs. The operation-local data is released after comparison; later calls take new
snapshots so edited observations cannot leave stale visible labels. Enumerating every pair still
requires quadratic work and output space.

## Similarity and duplicates

`similarity.compare(left_case, right_case)` returns structure-only and visible scores from 0 to 1.
The structural score ignores sex and phenotype. The visible score includes relationships, sex,
affected/unknown status, and disclosed carrier marks. Both ignore IDs, text labels, sibling/union
order, reflection, coordinates, hidden genotypes, and answer metadata.

Each score is multiset Jaccard overlap of Weisfeiler-Lehman neighborhood labels at radii zero through
three person-union edges, with equal weight per radius. These are not calibrated student-confusion
probabilities or graph-edit distances; distinct graphs can share signatures. Separate exact
attribute-aware graph isomorphism flags (`same_structure`, `same_visible`) establish duplicates.
No similarity cutoff rejects questions.

`similarity.pairwise(cases)` returns each unordered pair once with one-based indexes. Matching and
diagram-selection commands save these as `question_NNN_similarity.json` with instructor review
exports when `-r` is supplied. Student content omits them.

## Complexity

`similarity.complexity(family)` reports people, unions, generations, founder couples, joining unions,
maximum sibship, connected components, cycle rank, and incidence-graph diameter. A joining union
has two partners with recorded parents. An unrelated two-founder family can have a joining union and
zero cycles. Shared ancestry can create an undirected cycle without a biologically impossible
ancestry cycle. Diameter counts person-union edges, not generations or drawing distance; isolated
people have diameter zero. Complexity ignores sex, phenotype, IDs, and layout.

`complexity.sort_key()` orders generations, unions, joining unions, cycle rank, and people. This is a
transparent review convenience, not a validated difficulty score. All measures appear in instructor
review JSON; student question order remains randomized.

## Aesthetic exploration

`features.measure(family)` in [features.py](pedigree_lib/features.py) is topology-only and adds
degree counts, continuing children, branch points, local branch balance, and sibship variance to
the structural counts. Branch balance averages the smaller-to-larger distinct-descendant ratio at
branch points; shared descendants count once within each child's set. Sibship variance is population
variance. An October 2026 development experiment found degree counts often repeated size or union
counts; founder/joining counts were redundant and components/cycle rank were constant. Sibship
variance varied across workloads. Maximum sibship and local branch balance had some signal, but
simple scores did not generalize consistently to fresh, size/depth-matched examples.

Two independent geometry reviews used fresh pools. Width and parent gaps showed more consistent
associations with ratings for deep identification examples than for matching examples, but
low/middle/high comparisons did not establish a repeatable sweet spot. At fixed person count and
height, width, area density, and horizontal density are redundant. Later width-per-person
enrichment varied between pools and workloads. These measures were not retained as extra production
signals. `pedigree-aesthetics/SWEET_SPOT.md`, `pedigree-aesthetics/POLISHED_CORPUS.md`, and
`pedigree-aesthetics/CALIBRATION.md` preserve protocols, raw reviews, held-out checks, and the
decision to keep these outside production ranking; the evidence does not establish a universal
interestingness metric.
