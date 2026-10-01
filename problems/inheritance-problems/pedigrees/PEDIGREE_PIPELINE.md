# Pedigree homework pipeline

The three homework commands share a family model, a Mendelian engine, visible-evidence
teaching profiles, and one layout for HTML and editable SVG. Their teaching reference is
Lecture 05C, *Pedigrees*, September 29, 2026. See [PEDIGREE_AUTHORING.md](PEDIGREE_AUTHORING.md)
for the YAML format and [authored_cases.yml](authored_cases.yml) for editable examples.

## Generate homework

From the repository root:

```bash
source source_me.sh
python3 problems/inheritance-problems/pedigrees/write_pedigree_to_pattern.py -d 10 --selftest
python3 problems/inheritance-problems/pedigrees/write_pedigree_pattern_matching.py -d 3 -B -I
python3 problems/inheritance-problems/pedigrees/write_pattern_to_pedigree.py -d 3 --selftest
```

- `write_pedigree_to_pattern.py`: one pedigree, select its inheritance pattern.
- `write_pattern_to_pedigree.py`: a named pattern, select the corresponding pedigree.
- `write_pedigree_pattern_matching.py`: match pedigrees to all five inheritance patterns.
- All three use randomly generated families exclusively.
- At the medium level, the two MC formats use four or five generations and 16-22 people per diagram.
  Matching uses exactly three generations and 12-15 people per diagram. Diagram choices
  within a selection question share a generation count.
- All commands accept `-s SEED` for reproducibility. There are exactly three generator scripts.
- `--affected-color darkred` (or `darkblue`, etc.) sets the affected-symbol fill; black is default.
  `--random-color` instead selects one of 14 dark hues per question, shared by every diagram
  in that question and its SVG review exports. It respects `--seed`. The two color options
  are mutually exclusive; outlines remain black and unaffected symbols remain white.
- `-d` counts questions. Prebuilt-bank selection and the `-f`/`-y` source flags are retired.
- `-r output_pedigree/review` saves editable SVGs and instructor-only JSON evidence.
- Shared `--selftest`, `-O`, `-B`, and `-I` flags retain browser and Blackboard workflows.

Normal runs use fresh randomness. Verification uses `-s`; it seeds one explicit procedural
RNG and the existing export infrastructure's RNG. Family construction, mirroring, mode selection,
and matching order are randomized rather than cycled by question number.

BBQ files contain positioned HTML directly. The drawing table has a thin gray frame and works with
the existing HTML-to-image converter for Blackboard and Canvas/QTI packaging. Wide diagrams
fit the available width proportionally without scrolling or cropping. SVG exports contain real
shapes and text at the original geometry size.
The drawing table has a class so Material does not wrap it in an article-table scrolling container.
No remote website publication is part of this workflow.

Each nonempty run initially prepares 20 candidates per required pedigree: 20 times the requested
question count for identification, or 100 times for five-pedigree selection and matching.
The question count is `-d`, capped by `-x`; default runs prepare 40 or 200 candidates respectively.
Generation applies bounded polishing and the difficulty filter, then sorts by descending
interestingness.
The CLI reports elapsed preparation time, including generation, polishing, and assembly.
If the pool lacks enough complete scenarios, generation adds batches of the same size,
up to ten batches total, reporting each additional batch.
Identification consumes the highest-ranked entries. Selection
and matching assemble the highest eligible entries for all five modes, sharing depth and
founding-family count. Incomplete groups are unused. The selected questions and their choices
are shuffled before normal bptools export; collector retries consume unused reserve scenarios.
`-x` caps `-d`. Requests exceeding the available complete scenarios fail explicitly.

The deterministic heuristic is `progression - mean_row_density`. Progression counts +1 for
an expanding generation, 0 for an equal population, and -1 for contraction, starting with
generation II to III. Mean row density is the mean of `people / occupied_width` for
generations II onward; occupied width is the span of symbol centers plus 30 native units.
Row density is below one, so progression is primary and lower row density breaks its ties.
There are no fitted weights, learned parameters, or hard progression eligibility thresholds.

The polisher tries at most two terminal-child additions to shrinking rows after generation II.
It retains original people, observations, genotypes, and relationships. Each added child's
genotype must be a possible parental transmission. Every edit must pass the existing biology,
teaching, affected-sex balance, layout, and difficulty checks, preserve the answer, teaching
evidence and compatible modes, reduce mean shrink, and never increase width or lower progression.
If no edit qualifies, the original accepted case is returned. Unchanged cases remain eligible.

These are deliberately small aesthetic heuristics, not calibrated quality probabilities.
No prebuilt experimental pool, review artifact, or LLM is used in production. Geometry is
measured before responsive display scaling. Removing the sort in `scenarios.build` restores
the polished pool's generation order; removing the polishing call in `generate_pool` also
restores unmodified accepted families. Normal random generation provides tie ordering.

A historical compactness-only seeded check producing two questions per command took 50 seconds for identification,
51 seconds for selection, and 43 seconds for matching, including pool preparation and exports.
These concurrent-run timings are examples, not performance guarantees.

With polishing and interestingness enabled, a rigorous seeded check producing two questions
per command took 249 seconds for identification, 250 for selection, and 134 for matching.
Each command prepared its full 5,000-candidate pool. Six exported questions and 22 diagrams
passed one-time count, answer, depth, comparable-set, and rendered-score checks. A small
seeded polished pool reproduced exactly, and all difficulty presets passed acceptance checks.

## Structural workload presets

Choose one of `--easy` (default), `--medium`, or `--rigorous` on any question command.
`write_pedigree_to_pattern.py` also supports `--bonus` for one large pedigree. Bonus is rejected
for selection and matching, where it would multiply the reading burden across five diagrams.

| Preset | MC generations / people | Matching generations / people |
| --- | --- | --- |
| Easy | 3 / 12-15 | 3 / 10-11 |
| Medium | 4-5 / 16-22 | 3 / 12-15 |
| Rigorous | 5 / 23-26 | 3-4 / 16-18 |
| Bonus | 5 / 30-40, identification only | Not supported |

Difficulty presets primarily increase how much family structure students must inspect and trace.
The presets increase structural workload across several dimensions, allow overlap between bands,
and retain the same teaching-quality checks.
Size contributes visual scanning workload; total couples and founding families contribute
branching; generations contribute tracing depth. Tune these together rather than increasing
population alone. Sibship sizes provide variation within those constraints.

These are practical workload bands, not calibrated measurements of student difficulty. Larger
families intentionally require more scanning even when evidence repeats. A clear large family
can nevertheless be easier than a smaller one, so individual questions may overlap in difficulty.
Rigorous means more information to process, not weaker evidence or more ambiguity. Every level
retains the same genetic, visible-evidence, sex-balance, carrier-hiding, and layout checks.
There is no additional evidence-subtlety score or required ordering of individual questions.
Review representative examples when tuning presets; use student response times and error rates
to guide future calibration when available.

Easy and medium matching use three generations; rigorous matching allows three or four while
retaining its smaller 16-18-person band. Rigorous MC requires five generations. Choices within
each selection or matching question share a depth and size band. Larger bonus diagrams are
best reviewed at desktop or print size; responsive scaling preserves geometry, not symbol size.

The editable `DIFFICULTY_SETTINGS` and `MATCHING_SETTINGS` tables in
[difficulty.py](pedigree_lib/difficulty.py) also control construction directly:

| Preset | MC seed / total couples | Matching seed / total couples | Later children per couple |
| --- | --- | --- | --- |
| Easy | 1 / 3-4 | 1 / 2-3 | 1-3 |
| Medium | 1-2 / 4-6 | 1-2 / 3-4 | 1-4 |
| Rigorous | 2-3 / 6-8 | 2-3 / 4-5 | MC 1-4; matching 1-3 |
| Bonus | 2-3 / 8-11 | Not supported | 1-4 |

Each table row has `generations`, `people`, `seed_couples`, `couples`, `children`, and
`root_children`. All pairs are inclusive bounds; `generations` lists depth choices. Seed
sibships use 2-4 children, except easy matching and medium MC (2-5), and medium matching (2-6). Total couples
includes the seed couples, marriages joining their children, and marrying-in unions. Counts
are sampled within feasible bounds; not every combination inside the ranges is possible.
Selection and matching questions share a seed-couple count across their assembled diagrams.
Pool generation resamples construction choices after rejection within the same preset.

Two or more seed couples start in generation one. Marriages between their generation-two
children connect adjacent founding families, using a different child for each marriage.
Additional descendant unions marry in unrelated people. This produces one connected family
without consanguinity. Sex is assigned consistently with planned parental roles before
genotypes are simulated; affected status is never assigned to manufacture a pattern.

For direct library construction, the same knobs are keyword arguments on `procedural_family`,
`simulate_case`, and `generate_case`. For example:

```python
case = questions.generate_case('autosomal recessive', rng,
    min_people=23, max_people=26, generations=5,
    seed_couples=2, couples=(6, 8), children=(1, 4), root_children=(2, 4))
```

Exact counts use equal bounds, such as `couples=(6, 6)`. Impossible settings raise an explicit
error rather than silently falling back to a different family. The executable scripts remain
thin orchestrators; edit these Python tables to tune the existing difficulty flags.

```bash
source source_me.sh
python3 problems/inheritance-problems/pedigrees/write_pedigree_to_pattern.py --easy -d 10
python3 problems/inheritance-problems/pedigrees/write_pattern_to_pedigree.py --rigorous -d 3
python3 problems/inheritance-problems/pedigrees/write_pedigree_pattern_matching.py --medium -d 3
python3 problems/inheritance-problems/pedigrees/write_pedigree_to_pattern.py --bonus -d 1 --selftest -r output_bonus
```

For a previously accepted pool, use the same public library filter, then sort for review:

```python
selected = [item for item in accepted_pool
    if difficulty.fits_difficulty(item.case.family, 'rigorous', matching=False)]
selected.sort(key=lambda item: similarity.complexity(item.case.family).sort_key())
```

The filter checks seed couples, total couples, and both sibship bounds as well as size and depth.
The pool may contain 5,000 or more accepted cases; this filtering does not compute all pairwise
similarities. Generate across the desired presets to populate their different size/depth bands.
Do not interpret an unmatched family as biologically invalid. No global saved-bank format is
introduced. Instructor review JSON continues to include all structural measures. Authored YAML
examples remain library fixtures and demonstrations, outside the homework generation path.

A temporary run before the multi-founder constructor generated 5,000 accepted families in 31.27 seconds locally,
filtered all four bands in 0.25 seconds, and sorted the pool by the graph complexity key in
3.51 seconds. The largest individual search used 56 candidates. These timings exclude browser
rendering and question exports; they are an example measurement, not a performance guarantee.

Construction plans unions and reserved child slots first, keeping room within the population
and sibship budgets. A small backtracking search handles constrained branch choices before any
people are instantiated. Remaining child slots are allocated within the requested population
band. This supports joined founding families without enumerating all child-count combinations.
The changed sampling distribution changes seeded examples; fixed seeds remain reproducible
within this implementation. Earlier acceptance/timing studies describe the earlier samplers.

## Responsibilities and interfaces

The evaluator also filters affected-sex balance after identifying one supported teaching pattern.
With M affected males and F affected females, the only sex-balance score is
`S = (M-F)^2/(M+F)`:

- Autosomal dominant and recessive require `S < 0.25`.
- X-linked dominant requires `S > 0.99` and more affected females than males.
- X-linked recessive requires `S > 0.99` and more affected males than females.
- Y-linked requires affected males only, plus the existing paternal transmission evidence.

Every mode requires at least two affected individuals before computing the score. Y-linked
counts meeting that minimum automatically exceed 0.99. The existing male-only XR teaching
profile also remains in force; passing the score alone never establishes an answer.
These are classroom clarity filters, not biological laws or sex-specific incidence estimates.
They never resolve a tie between relationship-based profiles. A 3:2 count scores 0.20 and
passes the autosomal filter; 2:1 scores 0.33 and fails both filters. A 3:1 count scores 1.00
and passes the sex-linked filter only in the appropriate direction. Scores exactly 0.25 or
0.99 fail their respective strict cutoffs. Earlier simple-ratio thresholds are no longer used.

Easy matching allows up to five children in its seed sibship, within the existing 10-11-person
limit, so three-generation XD examples can meet the squared-bias requirement.
Default medium matching construction allows two to six children per seed sibship, for every mode;
later sibships have one to four. The default matching size stays 12-15. This leaves room for
clear female-biased XD families without selecting offspring sex or changing allele transmission.
An earlier construction investigation using the squared score `(M-F)^2/(M+F) > 0.99` with
female excess doubled raw XD acceptance from 20/2,000 to 40/2,000. In 200 seeded XD requests,
exhaustions fell from six to zero and mean attempts among completed requests fell from 122.5
to 57.2. These measurements describe the earlier sampler, not current acceptance rates.
The retry limit is now 5,000 candidates per requested pedigree, stopping at the first success.
Three local timing runs of 500 three-generation XD candidates under the squared score
took 0.21-0.22 seconds each, including simulation, evaluation, and qualifying layouts, but excluding
interpreter startup, browser rendering, and export. At that measured rate, a full 5,000-candidate
search would take approximately 2.2 seconds; other modes and machines may differ.

| Module | Responsibility and entry points |
| --- | --- |
| [family.py](pedigree_lib/family.py) | `Person`, `Union`, `Family`, `Observation`; structural validation and derived ancestry/generations |
| [graphs.py](pedigree_lib/graphs.py) | `to_networkx`, `components`; independent graph snapshots and shared connectivity analysis |
| [difficulty.py](pedigree_lib/difficulty.py) | Editable constructor presets, `difficulty_settings`, `difficulty_limits`, `fits_difficulty` |
| [inheritance.py](pedigree_lib/inheritance.py) | `MODES`, `simulate`, `observe`, `analyze`; shared transmission and phenotype rules |
| [policy.py](pedigree_lib/policy.py) | `teaching_evidence`, `assess`; observations only, no intended answer or simulated state |
| [sources.py](pedigree_lib/sources.py) | `Case`, `load_cases`, `procedural_family`, `simulate_case` |
| [questions.py](pedigree_lib/questions.py) | `evaluate`, `generate_case`, `authored_cases`, `present`, `matching_set` |
| [layout.py](pedigree_lib/layout.py) | `lay_out`, `layout_errors`; symbol positions, labeled bounds, connector segments |
| [html_output.py](pedigree_lib/html_output.py) | `render_html(diagram, observations)` |
| [svg_output.py](pedigree_lib/svg_output.py) | `render_svg(diagram, observations)` |
| [cli.py](pedigree_lib/cli.py) | Common argument parsing, question formatting, and instructor exports |
| [similarity.py](pedigree_lib/similarity.py) | Graph similarity, exact duplicate checks, and structural complexity measures |
| [features.py](pedigree_lib/features.py) | Independent topology measurements for aesthetic experiments |
| [geometry_features.py](pedigree_lib/geometry_features.py) | Native horizontal density measurement |
| [generation_features.py](pedigree_lib/generation_features.py) | Generation counts, progression, and shrink |
| [polishing.py](pedigree_lib/polishing.py) | Bounded terminal-child edits with full acceptance checks |
| [ranking.py](pedigree_lib/ranking.py) | Progression-first interestingness with row-density tie breaking |
| [scenarios.py](pedigree_lib/scenarios.py) | Accepted pools, removable score sort, comparable scenario assembly |

Import these submodules from a script in this directory. The command files are thin callers.
The old character-grid format, grid labels, graph-string format, and internal APIs are removed.

## Graph comparison and complexity

NetworkX (declared dependency, version 3.4 or newer within major version 3) compares the
relationship model, not rendered pixels. Each person and union is a separate node in an
undirected incidence graph. Edge attributes distinguish parent from child, preserving ancestry
direction without assuming a single founding couple or an unbranched tree. Cousin unions,
separate components, and two founding couples whose descendants marry are supported.

`graphs.to_networkx(family, observations=None)` is the shared adapter used by comparison and
complexity analysis. Without observations its labels encode topology only; supplying observations
adds sex and visible status to person labels. Each call returns an independent native NetworkX
graph. Editing it cannot change the family or another snapshot. The graph is a derived analysis
view, not another editable relationship authority.

Pairwise comparison prepares each family's structural graph, visible graph, and neighborhood
counts once per call, then reuses them across pairs. This operation-local cache is released after
the comparisons. Subsequent calls take new snapshots, so observation edits cannot leave stale
visible labels. No persistent or global cache is maintained. This reduces graph construction
and hashing from four times the pair count to twice the case count; enumerating every pair
still requires quadratic work and output space.

`similarity.compare(left_case, right_case)` returns two scores in [0, 1]:

- `structure`: relationship topology only, ignoring sex and phenotype.
- `visible`: relationships plus sex, affected/unknown status, and disclosed carrier markings.

Both ignore IDs, text labels, sibling/union order, reflection, coordinates, hidden genotypes,
and answer metadata. Each score is multiset Jaccard overlap of Weisfeiler-Lehman neighborhood
labels at radii zero through three person-union edges. Every radius contributes equally.
These are similarity scores, not calibrated student-confusion probabilities or graph edit
distances. Distinct graphs can have identical neighborhood signatures. The separate
`same_structure` and `same_visible` flags require exact attribute-aware graph isomorphism;
only those flags establish duplicates. No similarity cutoff currently rejects questions.

`similarity.pairwise(cases)` returns each unordered pair once, using one-based case indices.
With `-r`, matching and diagram-selection commands save these comparisons in
`question_NNN_similarity.json`, alongside the existing instructor review JSON and SVGs.
Student question content contains none of these diagnostics.

`similarity.complexity(family)` reports:

| Measure | Interpretation |
| --- | --- |
| `people`, `unions`, `generations` | Size, number of couples, and depth |
| `founder_couples` | Unions where neither parent has recorded parents |
| `joining_unions` | Unions where both partners have recorded parents; branches join |
| `max_sibship` | Largest child count of any union |
| `components` | Number of disconnected relationship groups |
| `cycle_rank` | Independent undirected loops: edges - nodes + components |
| `diameter` | Largest component's longest shortest path, in person-union edges |

An unrelated two-founder family can have a joining union and zero cycles; shared ancestry
can create an undirected loop without a biologically impossible ancestry cycle. Diameter
counts incidence edges, not generations or drawing distance. Isolated people have diameter
zero. Complexity is independent of sex, phenotype, IDs, and layout.

For a transparent structural ordering, use
`sorted(cases, key=lambda case: similarity.complexity(case.family).sort_key())`.
The key orders generations, unions, joining unions, cycle rank, then people lexicographically.
This is a review convenience, not a validated difficulty score. The complete measures and key
are included in instructor review JSON; student question order remains randomized.

Algorithm references: NetworkX [neighborhood hashing](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.graph_hashing.weisfeiler_lehman_subgraph_hashes.html),
[isomorphism](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.isomorphism.is_isomorphic.html),
[cycle bases](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.cycles.cycle_basis.html),
and [diameter](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.distance_measures.diameter.html).
The local *Modern Graph Theory Algorithms with Python* (2024), Chapters 1 and 6, provided
the graph-representation and diameter background.

## Aesthetic measurements

[features.py](pedigree_lib/features.py) exposes `measure(family)` without reading observations,
genotypes, difficulty, or drawing coordinates. It includes the existing structural counts plus:

- `degree_counts`: degree histogram over the person-union incidence graph, including isolated nodes.
- `continuing_children`: children with offspring, counted across the authoritative union child lists.
- `branch_points`: unions with at least two continuing children.
- `branch_balance`: mean smallest/largest distinct-descendant count at those branch points;
  zero when there are none. Shared descendants count once within each child's descendant set.
- `sibship_variance`: population variance of union child counts, zero with no unions.

The October 2026 development experiment used independent image reviews over three rounds.
Degree counts often duplicated size or union counts; founder and joining counts were redundant;
components and cycle rank were constant. Sibship variance behaved differently across workloads.
Maximum sibship and local branch balance showed some useful information, but neither tested
simple score generalized consistently to fresh, size/depth-matched examples. More unions could
reward crowding, while local balance missed global imbalance and rendered density.

A follow-up measured native rendered dimensions, density, spacing, distribution, and connector
lengths across two fresh pools. Width and parent gaps showed more consistent associations for
deep identification examples than for matching examples. Low/middle/high comparisons did not
establish a repeatable general sweet spot. At fixed person count and height, width, area density,
and horizontal density are redundant. See `SWEET_SPOT.md` in
the same sibling directory for the protocol, corrected blind reviews, and limitations.

The subsequent pool-enrichment experiment compared raw width and width per person with
ordinary valid selection. Results varied between pools and workloads; they do not establish
a general interestingness score. The simple width-per-person preference was initially used
with the 5,000-case scenario pipeline. Later, the fresh 200-case polished corpus found repeatable
weak associations for progression and mean row density. At the user's explicit decision,
production now uses those signals as the small deterministic heuristic above, together with
the bounded polisher. `POLISHED_CORPUS.md` in the sibling experiment directory preserves the
raw reviews, held-out checks, mixed results, and rationale. This is a pragmatic choice for
later revisiting, not a claim that calibration established a superior universal score.
Experimental scripts, raw measurements, rendered galleries, reviewer comparisons, and runtime
results live in the sibling `pedigree-aesthetics` directory, with the record in `CALIBRATION.md`.
No production module reads that directory or calls an LLM.

## Family and biology contracts

`Union.children` is the only parentage authority. People have stable string identifiers, sex,
and optional labels; neither generation numbers nor coordinates are authored. Structure validation
rejects missing references, duplicate IDs or parentage, ancestry cycles, incompatible generations,
and multiple unions per person. Founding families, marrying-in spouses, and cousin unions are
ordinary relationships. The introductory model uses one male father and one female mother per union.

Genotypes are separate from observations. Alleles are represented internally as `0` (ordinary)
and `1` (trait). Autosomal and female X-linked genotypes have two alleles; male X/Y genotypes
have one; females have no Y genotype. Carrier markings mean a known unaffected heterozygote.
An unmarked unaffected person can still be a carrier. Hiding carriers never modifies genotypes.

Simulation samples actual gametes, retaining their Mendelian multiplicities. Compatibility analysis
uses the same transmissions with genotype-domain propagation and backtracking across **every**
union and founding family. It assumes complete penetrance and no new mutations. It does not
assume that every marrying-in unaffected spouse lacks recessive alleles.

An affected father and son do not by themselves exclude X-linked inheritance: the son can receive
the allele from his mother. Two affected recessive parents cannot have unaffected children.
Affected-by-carrier crosses are simulated rather than replaced with phenotype heuristics.

## Teaching acceptance

These profiles encode the lecture's multi-clue reasoning. They are deliberately selective teaching
criteria, not inheritance laws or statistical likelihoods. Percentages and sex balance alone do
not establish an answer. A case must have exactly one supported profile among biologically
compatible modes. Other modes can remain biologically possible; the prompt says **most likely**.

| Mode | Required visible evidence |
| --- | --- |
| Autosomal dominant | Affected lineage spans three generations, both sexes affected, affected father has an unaffected daughter, no affected child of two unaffected parents |
| Autosomal recessive | Unaffected parents have affected offspring, plus both sexes affected or related parents of an affected child |
| X-linked dominant | Affected father with affected daughters and unaffected sons from an unaffected mother, plus an affected mother with affected sons and unaffected offspring |
| X-linked recessive | Affected grandfather, unaffected connecting daughter, affected grandson; affected son of unaffected parents; only males observed affected |
| Y-linked | Affected father-son lineage spans three generations, multiple affected sons in a sibship with daughters, all observed females unaffected; compatibility checks every father-son relationship |

Homework profiles require known affected/unaffected observations for everyone. The lower-level
engine and renderers also support unknown phenotype (`null`, rendered as `?`). Instructor review
JSON records the winning rationale and all compatible modes. Hidden genotypes and authored
`expected_mode` metadata never enter the teaching decision; an expectation is checked afterward.

## Generation and layout gates

The procedural source samples a feasible family size **before** construction. Current homework
families have three to five generations and one to four descendant unions. Each new union
can extend an existing branch or start another sibling's branch, with a marrying-in spouse
and one to four children. Sibship sizes are chosen together within the requested people bounds
before construction. Founder crosses can seed the trait in the top couple or a marrying-in
relative with grandchildren; all descendants are simulated. No teaching cores or complete-tree
templates are required, and the visible-evidence evaluator is unchanged.
Arbitrary clinical family generation, half-sibships, and multiple partners are outside scope.
Authored families can include more generations, separate founding families, and consanguinity.
Student commands select only single connected families and always hide carrier status before
evaluating the teaching answer. Cases that become unclear without carrier disclosure are excluded.
Carrier symbols and disconnected families remain available through the library for demonstrations.

Candidates pass biological, teaching, then layout acceptance. A different teaching answer, weak or
tied evidence, or an ambiguous drawing causes rejection. A bounded search raises `GenerationFailure`
with rejection counts on exhaustion. Invalid inputs and programming errors propagate immediately.
Correct the input or inspect the reasons; never silently emit a weak question or truncate a family.

Matching sets contain each mode once. Every case qualifies independently before assembling the set.
At medium difficulty they share a 12-15-person size band and exactly three generations,
with varied branching. Incomplete comparable groups are excluded from the scenario pool.

Layout first derives generations and ordered partner blocks from the fixed relationships.
It then solves horizontal positions jointly across the connected family with SciPy linear
programming: minimize total row spans plus marriage-line spans subject to symbol/label clearances and each couple's
midpoint centered over its outermost children. A sole child sits directly below the marriage
midpoint, with one straight vertical connector. Two children sit equally far on either side
of that midpoint. Segment construction rejects one- or two-child misalignment greater than
0.000001 pixels (solver noise only). Larger sibships can have unequal sibling gaps to accommodate
spouses and descendant branches; the middle child need not sit below the marriage midpoint.
Marrying-in spouses start outside their sibling group. Layout then tries reversing each such
couple, retaining collision-free reversals that reduce the component width, or reduce row and
marriage spans at the same width. It repeats until no reversal improves those dimensions.
Sibling order and related-partner order stay fixed; this does not claim an optimum over every
possible order. Positions are rounded
to eight decimal places to remove solver noise before drawing. An infeasible order raises an
explicit error for author revision. Siblings have smaller minimum gaps than separate sibships;
disconnected components have additional separation. Labels participate in clearance calculations.
Generation spacing keeps full-size symbols with short child drops and room for labels. The shared
QTI self-test gives rich matching prompts the available column width; narrower diagrams scale
all symbols, lines, and labels together instead of creating a scrolling region.
Consanguineous unions get double marriage lines. A shared descendant is drawn only once.
Mirroring transforms geometry, not relationships or labels. Some complex graphs cannot be laid out
without crossings by this compact layered algorithm; those are rejected for author revision.
Ordering hints can make complex authored families readable without storing pixel coordinates.

The geometry gate rejects symbol/label collisions, lines through symbols or labels, and intersections
between unrelated relationship connectors. Both renderers enforce it. Neither renderer calculates layout.

## Verification

```bash
source source_me.sh
python3 -m pytest tests/libs/pedigrees/ -q
pytest tests/
```

Focused regressions protect Mendelian contradictions, disclosure, source parity, weak-case rejection,
matching balance, cousin unions, shared descendants, labels, mirroring, and escaped editable output.
Broader seed sweeps and browser/package inspection are temporary implementation checks. A failed
biological, teaching, or layout gate blocks the question; a failed export blocks that workflow's migration.
