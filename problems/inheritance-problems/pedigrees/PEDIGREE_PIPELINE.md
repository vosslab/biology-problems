# Pedigree homework pipeline

The three homework commands share a family model, a Mendelian engine, visible-evidence
teaching profiles, and one layout for HTML and editable SVG. Their teaching reference is
Lecture 05C, *Pedigrees*, September 29, 2026. See [PEDIGREE_AUTHORING.md](PEDIGREE_AUTHORING.md)
for the YAML format and [authored_cases.yml](authored_cases.yml) for editable examples.

## Generate homework

From the repository root:

```bash
source source_me.sh
python3 problems/inheritance-problems/pedigrees/write_pedigree_choice.py -d 10 --selftest
python3 problems/inheritance-problems/pedigrees/write_pedigree_match.py -d 3 -B -I
python3 problems/inheritance-problems/pedigrees/write_pedigree_match_random.py -d 3 --selftest
```

- `write_pedigree_choice.py`: MC, authored families by default.
- `write_pedigree_match.py`: matching, authored families by default.
- `write_pedigree_match_random.py`: matching, procedural families by default.
- All commands accept `-f authored` or `-f procedural` and `-s SEED`.
- `-y BANK.yml` selects a custom bank when the source is authored.
- `-d` counts questions, including for authored commands. It no longer enumerates a bank product.
- `-r output_pedigree/review` saves editable SVGs and instructor-only JSON evidence.
- Shared `--selftest`, `-O`, `-B`, and `-I` flags retain browser and Blackboard workflows.

Normal runs use fresh randomness. Verification uses `-s`; it seeds one explicit procedural
RNG and the existing export infrastructure's RNG. Authored selection, sibling permutations,
mirroring, mode selection, and matching order are randomized rather than cycled by question number.
Explicit sibling-order hints prevent sibling shuffling; whole-diagram mirroring can reverse
the displayed left-to-right order.

BBQ files contain positioned HTML directly. The one borderless drawing table also works with
the existing HTML-to-image converter for Blackboard and Canvas/QTI packaging. Wide diagrams
fit the available width proportionally without scrolling or cropping. SVG exports contain real
shapes and text at the original geometry size.
The drawing table has a class so Material does not wrap it in an article-table scrolling container.
No remote website publication is part of this workflow.

## Responsibilities and interfaces

| Module | Responsibility and entry points |
| --- | --- |
| [family.py](pedigree_lib/family.py) | `Person`, `Union`, `Family`, `Observation`; structural validation and derived ancestry/generations |
| [inheritance.py](pedigree_lib/inheritance.py) | `MODES`, `simulate`, `observe`, `analyze`; shared transmission and phenotype rules |
| [policy.py](pedigree_lib/policy.py) | `teaching_evidence`, `assess`; observations only, no intended answer or simulated state |
| [sources.py](pedigree_lib/sources.py) | `Case`, `load_cases`, `procedural_family`, `simulate_case` |
| [questions.py](pedigree_lib/questions.py) | `evaluate`, `generate_case`, `authored_cases`, `present`, `matching_set` |
| [layout.py](pedigree_lib/layout.py) | `lay_out`, `layout_errors`; symbol positions, labeled bounds, connector segments |
| [html_output.py](pedigree_lib/html_output.py) | `render_html(diagram, observations)` |
| [svg_output.py](pedigree_lib/svg_output.py) | `render_svg(diagram, observations)` |
| [cli.py](pedigree_lib/cli.py) | Common argument parsing, question formatting, and instructor exports |

Import these submodules from a script in this directory. The command files are thin callers.
The old character-grid format, grid labels, graph-string format, and internal APIs are removed.

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
families have three or four generations and one to three descendant unions. Each new union
can extend an existing branch or start another sibling's branch, with a marrying-in spouse
and one to four children. Sibship sizes are chosen together within the requested people bounds
before construction. Founder crosses can seed the trait in the top couple or a marrying-in
relative with grandchildren; all descendants are simulated. No teaching cores or complete-tree
templates are required, and the visible-evidence evaluator is unchanged.
Arbitrary clinical family generation, half-sibships, and multiple partners are outside scope.
Authored families can include more generations, separate founding families, and consanguinity.

Candidates pass biological, teaching, then layout acceptance. A different teaching answer, weak or
tied evidence, or an ambiguous drawing causes rejection. A bounded search raises `GenerationFailure`
with rejection counts on exhaustion. Invalid inputs and programming errors propagate immediately.
Correct the input or inspect the reasons; never silently emit a weak question or truncate a family.

Matching sets contain each mode once. Every case qualifies independently before assembling the set.
They share a 12-15-person size band and allow three or four generations, without requiring identical
depth or branching. Authored matching fails explicitly
if a bank lacks a qualifying comparable example for any mode.

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
