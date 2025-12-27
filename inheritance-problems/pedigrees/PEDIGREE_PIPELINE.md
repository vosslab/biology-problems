# PEDIGREE PIPELINE

Pedigree generation is a multi-stage pipeline with a single canonical internal
representation for family structure. This keeps inheritance logic independent
from rendering and makes both HTML and PNG outputs consistent.

## Canonical internal representation (PedigreeGraph)
PedigreeGraph is the source of truth for family structure and genetics.

Individuals
- id
- sex (male, female)
- generation_index (1-based)
- phenotype_state (unaffected, affected, carrier, unknown)
- optional genotype (per locus or per mode)

Relationships
- Couple: partner_a, partner_b, consanguinity_degree (optional)
- Child: child_id with mother_id and father_id
- Derived: sibships, founders, connected components

PedigreeGraph should never encode layout or rendering details.

## Pipeline stages
1) **Skeleton engine**
	- Input: generations, starting couples, sibling range, marriage rate,
	  consanguinity policy.
	- Output: PedigreeGraph with all parents and mates set, no disease labels yet.
	- Goal: generate a graph that is legally structured and visually teachable.
	- Invariants:
	  - No ancestry cycles.
	  - Each child has exactly two parents.
	  - Spouses share the same generation.
	  - Connected components policy is explicit (keep 1-3 founder couples
	    separate, or force a merge via a later marriage).
	  - At least one multi-child sibship and at least one marrying-in spouse.
	  - Consanguinity placement is deliberate, not accidental.

2) **Inheritance engine**
	- Input: PedigreeGraph, inheritance mode, carrier visibility policy,
	  optional target counts.
	- Output: PedigreeGraph with genotype assigned and phenotype derived.
	- Approach: simulate inheritance; if constraints fail, resample founder
	  genotypes or transmissions until constraints pass.

3) **Layout engine**
	- Input: PedigreeGraph.
	- Output: LayoutGraph with x,y positions and connector routing.
	- LayoutGraph is a grid-based geometry layer (node placements plus routed
	  connector segments) with no genetics or pedigree semantics.
	- Layout is deterministic and cacheable for a given graph.

4) **CodeString encoding**
	- Input: LayoutGraph and a CodeSpec (pedigree_code alphabet).
	- Output: CodeString grid with % row separators.

5) **Renderers**
	- Input: CodeString.
	- Output: HTML or PNG.
	- Renderers are pure transforms and never change genetics or structure.

## Validation split
Validation is intentionally layered.

- **Syntax validation** (CodeString)
	- Allowed symbols only.
	- Row structure is well-formed.
	- Optional strict mode: consistent row lengths.

- **Genetics validation** (PedigreeGraph)
	- Autosomal dominant: affected must have an affected parent unless de novo.
	- Autosomal recessive: affected implies both parents are carriers or affected.
	- X-linked recessive: no father-to-son; affected females require affected father.
	- Y-linked: affected only in males; affected fathers imply affected sons.
	- If carriers are hidden, autosomal-recessive validation may need to degrade
	  to weaker checks (for example, an affected child must have two parents who
	  could be carriers, not necessarily flagged as carriers).

Mode validation should prefer PedigreeGraph. Parsing from CodeString is a **fallback**
only for legacy or template-only inputs.

## CodeString as layout serialization
The CodeString format is a compact grid encoding of the LayoutGraph. It is not a
family graph. It should not be treated as the primary source of truth for
inheritance logic.

## CodeSpec
CodeSpec defines the CodeString alphabet and rules for parsing/encoding.

- Alphabet and symbol meanings (including carrier on/off policy).
- Row separator conventions (%), row-length expectations, and grid width.
- Version identifier to keep legacy strings decodable.
- Allowed transforms at this layer (mirror only, unless explicitly expanded).

## Quality knobs and scoring
Randomness is easy; diagnostic clarity is hard. Use scoring and rejection.

Examples of useful scores:
- Mode-consistency score (must be perfect).
- Diagnostic features score (presence of telltale edges).
- Visual clutter score (node count, crossings, density).
- Diversity score across a batch (avoid near-duplicates).

Generate -> label -> validate -> score -> accept if above threshold.

## Compatibility
- CodeString rendering and HTML/PNG outputs remain stable across generator changes.
- PedigreeGraph and inheritance assignment can evolve independently of renderers.
