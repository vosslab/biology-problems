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

Pipeline shorthand
- generator -> pedigree_graph_spec -> pedigree_code_string -> HTML/PNG
- The graph parse/compile step is an internal transformation and is not
  persisted as a pipeline artifact.

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

## Pedigree code symbols (CodeString alphabet)
Symbols are single-character cells in the grid. Carrier symbols are only
meaningful when carriers are shown; when carriers are hidden they render as
unaffected shapes.

People
- `#` = WHITE SQUARE (unaffected male)
- `x` = BLACK SQUARE (affected male)
- `[` = LEFT-HALF BLACK SQUARE (carrier male)
- `]` = RIGHT-HALF BLACK SQUARE (carrier male)
- `o` = WHITE CIRCLE (unaffected female)
- `*` = BLACK CIRCLE (affected female)
- `(` = LEFT-HALF BLACK CIRCLE (carrier female)
- `)` = RIGHT-HALF BLACK CIRCLE (carrier female)

Connectors
- `-` = HORIZONTAL LINE SHAPE
- `|` = VERTICAL LINE SHAPE
- `+` = PLUS SHAPE
- `T` = T SHAPE
- `=` = INCEST T SHAPE
- `^` = PERPENDICULAR TENT SHAPE
- `L` = UP-RIGHT ELBOW SHAPE
- `u` = UP-LEFT ELBOW SHAPE
- `r` = DOWN-RIGHT ELBOW SHAPE
- `d` = DOWN-LEFT ELBOW SHAPE

Layout
- `.` = SPACE (empty cell)
- `%` = NEW LINE (row separator; not a cell)

## CodeString semantics (row parity and offspring encoding)
These rules define which symbols can appear where and how descent is encoded.

Row parity
- Rows alternate meaning: even rows (0, 2, 4, ...) are people rows; odd rows
  (1, 3, 5, ...) are connector rows.
- Person symbols appear only on people rows.
- Connector symbols appear on connector rows, except for spouse connectors
  (`-`, `T`, `=`) which may appear between two people on a people row.

Couple and offspring encoding
- A couple is two adjacent person cells with connector cells between them on the
  same people row (e.g., `#-o` or `#To`).
- `T` marks the couple midpoint and is the attachment point for descent.
- If a couple has children, `T` must have a down edge into the connector row.
- Offspring are encoded by a vertical line from the couple midpoint down to a
  sibship bar, then vertical drops to each child.
- A vertical descent line may terminate on a single person cell, but never on
  another `T` (no “couple gives birth to couple”).

Rendering rule
- All rows are padded to equal length with `.` before rendering to HTML/PNG.

## Pedigree graph spec string format
This is a compact, self-delimiting pedigree graph spec (union-based) string.

Syntax
- Segments are separated by `;`.
- Segment 1 is the sex-anchor list: `F:` followed by person tokens.
- Segment 2+ are unions: `ParentA-ParentB:Children`.

Person tokens
- Format: `X` + `m|f` + optional `i|c`
  - `m`/`f` = sex (required for children and founders).
  - `i` = infected, `c` = carrier (optional).
- Outside spouses may omit sex; the sex is inferred from the known partner.
- Children must always include sex, with optional status.

Examples
- `F:AmBfCmDfEfGfHmIf;A-B:CmDfEf;C-G:HmIf`

Naming bundle
- Concept name (docs): pedigree graph spec
- String form: `pedigree_graph_spec_str` or `pedigree_graph_spec_string`
- Parsed object: `PedigreeGraphSpec` (class) or `pedigree_graph_spec` (dict)
- Codec module: `pedigree_graph_spec_lib.py`
- Functions:
  - `parse_pedigree_graph_spec(s) -> PedigreeGraph`
  - `format_pedigree_graph_spec(graph) -> str`
  - `hash_pedigree_graph_spec(s) -> str`

Terminology consistency
- Use `pedigree_code_string` for the grid/layout encoding.
- Use `pedigree_graph_spec` for the union-based formalism.

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

## Library roles (current files)
Each library is intentionally narrow and maps to a pipeline layer or cross-cutting
validation. These names are stable in code; rename suggestions are listed after.

- `pedigree_graph_parse_lib.py`: internal graph types plus compile step from
  graph spec to code-string layout (intermediate only).
- `pedigree_skeleton_lib.py`: procedural skeleton generation (structure only).
- `pedigree_inheritance_lib.py`: inheritance-mode phenotype assignment.
- `pedigree_code_lib.py`: CodeSpec, code alphabet, mirroring, and encode/decode helpers.
- `pedigree_validate_lib.py`: CodeString syntax validation.
- `pedigree_mode_validate_lib.py`: inheritance-mode validation (PedigreeGraph-first).
- `pedigree_html_lib.py`: HTML renderer (CodeString -> HTML).
- `pedigree_png_lib.py`: PNG renderer (CodeString -> PNG).
- `pedigree_template_gen_lib.py`: template-based pedigree selection (CodeString output).
- `pedigree_code_templates.py`: template library (static CodeStrings).
- `preview_pedigree.py`: CLI for batch preview (HTML/PNG/code strings).

## Possible naming improvements
These are suggestions only; they are not required by the pipeline.

- `pedigree_graph_parse_lib.py` -> `pedigree_skeleton_lib.py` (if it stays focused on
  structure generation).
- `preview_pedigree.py` -> `cli_preview_pedigree.py` (distinguish CLI entry points).
