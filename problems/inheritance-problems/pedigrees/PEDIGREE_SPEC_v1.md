# PEDIGREE_SPEC_v1

This document defines the two external, stable formats used by the pedigree system:

1. `pedigree_graph_spec` (a compact text format for family structure and optional phenotype flags)
2. `pedigree_code_string` (a compact grid layout format used by renderers)

Internal graph objects (for example, `PedigreeGraph`) are an implementation detail and are not part of this spec.

## 1) Pedigree graph spec (v1)

### Purpose
`pedigree_graph_spec` describes founders, unions, and children. The format is intentionally small and easy to generate.

### Syntax
A spec string is a sequence of **segments** separated by semicolons (`;`).

- Segment 1: founders, starts with `F:`
- Segment 2 and later: unions, formatted as `ParentA-ParentB:Children`

General form:

```
F:<FounderTokens>;<Union1>;<Union2>;...
```

### Person tokens
A person token is a short, self-contained label.

Format:

```
<Id><Sex><Status?>
```

- `<Id>` is a single uppercase letter `A` to `Z`
- `<Sex>` is `m` or `f`
- `<Status?>` is optional and may be:
  - `i` infected (affected)
  - `c` carrier

Examples:

- `Am` male A
- `Bfi` female B, infected
- `Cmc` male C, carrier

### Founder segment
The founder segment lists the generation 1 founders:

```
F:AmBf
```

Rules:

- The `F:` segment must include at least two founder tokens.
- Founder tokens must include sex.
- The first two founder tokens define the generation 1 main couple

### Union segments
Each union segment encodes one couple and at least one child:

```
A-B:CmDfEf
```

Rules:

- Partners are written as `ParentA-ParentB`.
- Union partners are bare IDs only (no sex or status tokens allowed).
- The parser accepts either partner order, then normalizes to male then female based on stored sex.
- At least one partner in every union must already be defined as a founder or as a child in an earlier union (so their sex/status are known).
- Founder-descendant unions are allowed (incest pedigrees).
- Founder-undefined unions are invalid.
- A union may not introduce two new partners. If both partners have no parents listed in the spec, they must appear in `F:` and be treated as founders.
- A union partner may not redefine a person; conflicting person definitions are invalid.
- Children are written as a concatenation of full person tokens, with no separators inside the child list.
- A union must include at least one child. An empty child list after `:` is invalid.
- A child may appear in only one union.

### Founder definition and marry-ins
The `F:` segment lists only true generation 1 founders.

A person that first appears as a union partner, has no parents listed, and is not listed in `F:` is treated as a marry-in spouse. The generation for a marry-in spouse is inherited from the partner. Marry-ins are always assumed unaffected/non-carrier, and their sex is inferred from the known partner.

Founder-descendant unions are allowed (incest pedigrees). A founder-undefined union is invalid. If both partners in a union are undefined, they must be listed in `F:` and treated as founders.

#### Marry-in union: a union where:
- Exactly one partner has no parents specified in the graph spec (the "undefined partner") and is not listed in `F:`, and
- The other partner is a descendant of an `F:` founder and is defined by a previous union.

### Examples

```
F:AmBf;A-B:CmDfEf;C-G:HmIf
F:AfBm;B-A:CmDfEfFm;C-G:JmKm;H-E:LmMmNfOf
```

### Version notes
`pedigree_graph_spec` v1 assumes single-letter IDs. If the system later needs multi-character IDs, that change requires a new version.

## 2) Pedigree code string (v1)

### Purpose
`pedigree_code_string` (CodeString) is a compact grid encoding of a pedigree layout. CodeString is not a family graph.

Renderers (HTML, SVG, PNG) consume CodeString directly.

### Grid structure
- CodeString is a sequence of rows separated by `%`.
- `.` means an empty cell.
- All rows are padded to the same length with `.` before rendering.
- An empty row is encoded as a single `.` to preserve row parity.

Example with three rows:

```
#To%.|%.#.
```

### Row parity
Rows alternate meaning:

- Even rows (0, 2, 4, ...) are **people rows**
- Odd rows (1, 3, 5, ...) are **connector rows**

Rules:

- Person symbols appear only on people rows.
- Connector symbols appear on connector rows, except spouse connectors (`-`, `T`, `=`) which may appear between two people on a people row.

### Alphabet

#### People
- `#` unaffected male (white square)
- `x` affected male (black square)
- `[` carrier male (left-half black square)
- `]` carrier male (right-half black square)
- `o` unaffected female (white circle)
- `*` affected female (black circle)
- `(` carrier female (left-half black circle)
- `)` carrier female (right-half black circle)

#### Connectors
- `-` horizontal line
- `|` vertical line
- `+` plus
- `T` couple midpoint and descent attachment
- `=` incest T
- `^` perpendicular tent
- `L` up-right elbow
- `u` up-left elbow
- `r` down-right elbow
- `d` down-left elbow

#### Layout
- `.` empty cell
- `%` row separator (not a cell)

### Couple and offspring encoding
- A couple is two adjacent person cells with connector cells between them on the same people row, for example `#To`.
- `T` marks the couple midpoint (even if there are no children).
- If a couple has children, `T` must have a down edge into the connector row.
- Offspring are encoded by a vertical line from the couple midpoint down to a sibship bar, then vertical drops to each child.
- A vertical descent line may terminate on a single person cell, but never on another `T` (no couple gives birth to couple).

### Simple, valid CodeString examples

1) One couple, one child

Rows:
- `#To`
- `.|.`
- `.#.`

CodeString:
- `#To%.|%.#.`

2) One couple, two children

Rows:
- `#To`
- `r^d`
- `#.o`

CodeString:
- `#To%r^d%#.o`

3) Two-generation chain (child marries and has a child)

Rows:
- `#To..`
- `.|...`
- `.#To.`
- `..|..`
- `..o..`

CodeString:
- `#To..%.|...%.#To.%..|..%..o..`

## 3) Optional label strings (v1)

A label string is a parallel grid with the same row and column structure as CodeString.

Rules:

- `.` means no label in that cell.
- Labels use `A-Z` (and optionally `a-z`) for person labels.
- Labels must align with person cells only.

### Simple, valid LabelString examples

One couple, two children

Rows:
- `ATB`
- `r^d`
- `C.D`

LabelString:
- `ATB%r^d%C.D`

## 4) Reference implementation hooks

The reference compiler is:

- `compile_graph_spec_to_code(spec_string: str, show_carriers: bool = True) -> str`

This compiler parses `pedigree_graph_spec` and emits `pedigree_code_string`. The internal graph created during compilation is not a stable interface.
