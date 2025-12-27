# PEDIGREE PIPELINE

Pedigree generation is a multi-stage pipeline with a single canonical internal
representation for family structure. This keeps inheritance logic independent
from rendering and makes both HTML and PNG outputs consistent.

## Overview
### Pipeline shorthand
- generator -> pedigree_graph_spec -> pedigree_code_string -> HTML/PNG
- The graph parse/compile step is internal and is not persisted as a pipeline artifact.

### Design goals
- PedigreeGraph is the source of truth for structure and genetics.
- CodeString is a compact layout serialization, not a family graph.
- Renderers are pure transforms from CodeString.

## Recent milestones (2025-12-27)
- Stabilized pedigree graph spec rules: founder definition, sex inference, and
  male-first union normalization.
- Fixed CodeString row-parity handling (empty rows preserved as `.`).
- Improved layout compilation to produce canonical `#To`, `r^d`, and compact
  sibship connectors.
- Hardened validation rules (vertical descent checks and connector endpoints).

## Canonical internal representation
### PedigreeGraph
PedigreeGraph is the source of truth for family structure and genetics.

#### Individuals
- id
- sex (male, female)
- generation_index (1-based)
- phenotype_state (unaffected, affected, carrier, unknown)
- optional genotype (per locus or per mode)

#### Relationships
- Couple: partner_a, partner_b, consanguinity_degree (optional)
- Child: child_id with mother_id and father_id
- Derived: sibships, founders, connected components

#### Non-goals
PedigreeGraph should never encode layout or rendering details.

### Role in the pipeline
- PedigreeGraph is an internal, non-persisted structure used to compile a
  pedigree graph spec into a CodeString layout.
- Generators should emit pedigree graph spec strings. PedigreeGraph is created
  only during the compile step.

## Pipeline stages
### 1) Skeleton engine
- Input: generations, starting couples, sibling range, marriage rate,
  consanguinity policy.
- Output: PedigreeGraph with all parents and mates set, no disease labels yet.
- Goal: generate a graph that is legally structured and visually teachable.

#### Skeleton invariants
- No ancestry cycles.
- Each child has exactly two parents.
- Spouses share the same generation.
- Connected components policy is explicit (keep 1-3 founder couples separate, or
  force a merge via a later marriage).
- At least one multi-child sibship and at least one marrying-in spouse.
- Consanguinity placement is deliberate, not accidental.

### 2) Inheritance engine
- Input: PedigreeGraph, inheritance mode, carrier visibility policy,
  optional target counts.
- Output: PedigreeGraph with genotype assigned and phenotype derived.
- Approach: simulate inheritance. If constraints fail, resample founder
  genotypes or transmissions until constraints pass.

### 3) Layout engine
- Input: PedigreeGraph.
- Output: LayoutGraph with x,y positions and connector routing.

#### LayoutGraph definition
- LayoutGraph is a grid-based geometry layer (node placements plus routed
  connector segments) with no genetics or pedigree semantics.
- Layout is deterministic and cacheable for a given graph.

### 4) CodeString encoding
- Input: LayoutGraph and a CodeSpec (pedigree_code alphabet).
- Output: CodeString grid with `%` row separators.

### 5) Renderers
- Input: CodeString.
- Output: HTML or PNG.
- Renderers are pure transforms and never change genetics or structure.

### Implementation note
- `pedigree_graph_parse_lib.compile_graph_spec_to_code()` performs the internal
  graph-spec parse and layout compile to CodeString.

## Validation
Validation is intentionally layered.

### Syntax validation
#### CodeString
- Allowed symbols only.
- Row structure is well-formed.
- Optional strict mode: consistent row lengths.

### Genetics validation
#### PedigreeGraph
- Autosomal dominant: affected must have an affected parent unless de novo.
- Autosomal recessive: affected implies both parents are carriers or affected.
- X-linked recessive: no father-to-son. Affected females require affected father.
- Y-linked: affected only in males. Affected fathers imply affected sons.
- If carriers are hidden, autosomal-recessive validation may need to degrade to
  weaker checks (for example, an affected child must have two parents who could
  be carriers, not necessarily flagged as carriers).

### Mode validation preference
Mode validation should prefer PedigreeGraph. Parsing from CodeString is a fallback
only for legacy or template-only inputs.

## CodeString and CodeSpec
### CodeString as layout serialization
The CodeString format is a compact grid encoding of the LayoutGraph. It is not a
family graph. It should not be treated as the primary source of truth for
inheritance logic.

### CodeSpec
CodeSpec defines the CodeString alphabet and rules for parsing and encoding.
- Alphabet and symbol meanings (including carrier on or off policy).
- Row separator conventions (`%`), row-length expectations, and grid width.
- Version identifier to keep legacy strings decodable.
- Allowed transforms at this layer (mirror only, unless explicitly expanded).

### Simple, valid CodeString examples
These examples are intentionally small and are valid under the row-parity rules
below. Rows are separated by `%`. A trailing `%` is not required.

1) One couple, one child
- Meaning: parents with a single male child in the next generation.
- CodeString (rows shown):
  - `#To`
  - `.|.`
  - `.#.`
- CodeString (single string): `#To%.|%.#.`

2) One couple, two children
- Meaning: parents with two children in the next generation.
- CodeString (rows shown):
  - `#To`
  - `r^d`
  - `#.o`
- CodeString (single string): `#To%r^d%#.o`

3) Two-generation chain (child marries and has a child)
- Meaning: gen1 couple has one child; that child forms a couple in gen2 and has one child in gen3.
- CodeString (rows shown):
  - `#To..`
  - `.|...`
  - `.#To.`
  - `..|..`
  - `..o..`
- CodeString (single string): `#To..%.|...%.#To.%..|..%..o..`

Notes
- Examples include trailing `.` padding for clarity. Renderers may pad rows
  internally, but explicitly padding in examples makes row lengths obvious.
- Children appear on people rows, never on connector rows.

## Pedigree code symbols
### CodeString alphabet
Symbols are single-character cells in the grid. Carrier symbols are only
meaningful when carriers are shown. When carriers are hidden they render as
unaffected shapes.

#### People
- `#` = WHITE SQUARE (unaffected male)
- `x` = BLACK SQUARE (affected male)
- `[` = LEFT-HALF BLACK SQUARE (carrier male)
- `]` = RIGHT-HALF BLACK SQUARE (carrier male)
- `o` = WHITE CIRCLE (unaffected female)
- `*` = BLACK CIRCLE (affected female)
- `(` = LEFT-HALF BLACK CIRCLE (carrier female)
- `)` = RIGHT-HALF BLACK CIRCLE (carrier female)

#### Connectors
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

#### Layout
- `.` = SPACE (empty cell)
- `%` = NEW LINE (row separator, not a cell)

### CodeString semantics
#### Row parity
- Rows alternate meaning: even rows (0, 2, 4, ...) are people rows. Odd rows
  (1, 3, 5, ...) are connector rows.
- Person symbols appear only on people rows.
- Connector symbols appear on connector rows, except for spouse connectors
  (`-`, `T`, `=`) which may appear between two people on a people row.

#### Couple and offspring encoding
- A couple is two adjacent person cells with connector cells between them on the
  same people row (for example, `#To`).
- `T` always marks the couple midpoint (even if there are no children) and is the
  attachment point for descent.
- If a couple has children, `T` must have a down edge into the connector row.
- Offspring are encoded by a vertical line from the couple midpoint down to a
  sibship bar, then vertical drops to each child.
- A vertical descent line may terminate on a single person cell, but never on
  another `T` (no "couple gives birth to couple").

#### Rendering rule
- All rows are padded to equal length with `.` before rendering to HTML or PNG.
- Empty rows are encoded as a single `.` to preserve row parity.

### Simple, valid CodeString examples
These examples are intentionally small and valid under the row-parity rules.
Rows are separated by `%`. A trailing `%` is not required.

1) One couple, one child
- Meaning: parents with a single male child in the next generation.
- Rows:
  - `#To`
  - `.|.`
  - `.#.`
- CodeString: `#To%.|%.#.`

2) One couple, two children
- Meaning: parents with two children in the next generation.
- Rows:
  - `#To`
  - `r^d.`
  - `#.o`
- CodeString: `#To%r^d.%#.o`

3) Two-generation chain (child marries and has a child)
- Meaning: gen1 couple has one child; that child forms a couple in gen2 and has one child in gen3.
- Rows:
  - `#To..`
  - `.|...`
  - `.#To.`
  - `..|..`
  - `..o..`
- CodeString: `#To..%.|...%.#To.%..|..%..o..`
## Pedigree graph spec
### Pedigree graph spec string format
This is a compact, self-delimiting, union-based pedigree graph spec string.

#### Syntax
- Segments are separated by `;`.
- Segment 1 defines generation-1 founders: `F:` followed by 2+ person tokens.
- The first two founder tokens define the main couple (used for centering).
- Segment 2+ define unions: `ParentA-ParentB:Children`.
- Union partner order is normalized to male then female. The parser accepts
  either order.

#### Person tokens
- Format: `X` + `m|f` + optional `i|c`
  - `m` or `f` = sex.
  - `i` = infected, `c` = carrier.

#### Rules
- Founders in `F:` must include sex. Children must include sex. Status is optional.
- Union partners may omit sex. If a partner omits sex, sex is inferred from the
  other partner in the union.
- A union is invalid if both partner sexes are omitted.
- Children are listed as a concatenation of person tokens (no separators within
  the child list).
- Unions must list at least one child. An empty `:` is invalid.
- People IDs are single uppercase letters.

#### Founder definition
- The `F:` segment lists only true generation-1 founders.
- Outside spouses are not founders. If a person first appears as a union partner
  and has no parents listed, the person is treated as a marry-in spouse whose
  generation is inherited from the partner.

#### Examples
- `F:AmBf;A-B:CmDfEf;C-G:HmIf`
- `F:AfBm;B-A:CmDfEfFm;C-G:JmKm;H-E:LmMmNfOf`

### Naming bundle
- Concept name (docs): pedigree graph spec
- String form: `pedigree_graph_spec_str` or `pedigree_graph_spec_string`
- Parsed object: `PedigreeGraphSpec` (class) or `pedigree_graph_spec` (dict)
- Codec module: `pedigree_graph_spec_lib.py`

#### Functions
- `parse_pedigree_graph_spec(s) -> PedigreeGraph`
- `format_pedigree_graph_spec(graph) -> str`
- `hash_pedigree_graph_spec(s) -> str`

### Terminology consistency
- Use `pedigree_code_string` for the grid and layout encoding.
- Use `pedigree_graph_spec` for the union-based formalism.

## Quality knobs and scoring
Randomness is easy. Diagnostic clarity is hard. Use scoring and rejection.

### Example scores
- Mode-consistency score (must be perfect).
- Diagnostic features score (presence of telltale edges).
- Visual clutter score (node count, crossings, density).
- Diversity score across a batch (avoid near-duplicates).

### Acceptance loop
Generate -> label -> validate -> score -> accept if above threshold.

## Compatibility
- CodeString rendering and HTML/PNG outputs remain stable across generator changes.
- PedigreeGraph and inheritance assignment can evolve independently of renderers.

## Library roles (current files)
Each library is intentionally narrow and maps to a pipeline layer or cross-cutting
validation. These names are stable in code. Rename suggestions are listed after.

### Libraries
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

### CLI
- `preview_pedigree.py`: CLI for batch preview (HTML/PNG/code strings).

## Possible naming improvements
These are suggestions only. They are not required by the pipeline.

- `pedigree_graph_parse_lib.py` -> `pedigree_skeleton_lib.py` (if it stays focused
  on structure generation).
- `preview_pedigree.py` -> `cli_preview_pedigree.py` (distinguish CLI entry points).
