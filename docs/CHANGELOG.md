# Changelog

## 2026-04-27

### Behavior or Interface Changes
- Tightened HTML-tag rejection in
  [webwork_lib.py](../webwork_lib.py) `extract_strict_color_span` and
  `extract_strict_color_spans` so only `<sub>` and `<sup>` are tolerated
  inside a strict color span; `<i>` and `<em>` now correctly cause `None`
  to be returned, matching the intent stated in commit `4e15773`.

### Fixes and Maintenance
- Updated stale `import_from_repo_path` paths in three library tests after
  the folder reorganization that moved sources into `enzymes/`, `carbs/`,
  and `buffers/` subfolders:
  [tests/libs/test_biochemistry_enzymelib.py](../tests/libs/test_biochemistry_enzymelib.py)
  -> `enzymes/enzymelib.py`,
  [tests/libs/test_biochemistry_sugarlib.py](../tests/libs/test_biochemistry_sugarlib.py)
  -> `carbs/sugarlib.py`,
  [tests/libs/test_henderson_hasselbalch.py](../tests/libs/test_henderson_hasselbalch.py)
  -> `buffers/Henderson-Hasselbalch.py`.
- Simplified `test_enzymelib_tree_and_html_table` by dropping the
  `len(enzyme_tree) == 4` and exact key-set assertions, per
  [docs/PYTHON_STYLE.md](PYTHON_STYLE.md) "avoid tests that assert on
  collection sizes [or] required key lists".
- Updated
  [tests/yaml/test_mc_statements_to_pgml.py](../tests/yaml/test_mc_statements_to_pgml.py)
  to assert `## TITLE(` and `## DESCRIPTION` membership rather than
  `startswith("## DESCRIPTION")`, since the generator now emits `## TITLE`
  first per commit `c6d43ba`. The remaining OPL header markers
  (`## KEYWORDS(`, `## DBsubject(`, `DOCUMENT();`, `PGcourse.pl`) are kept
  because they are external WeBWorK/OPL spec markers (boundary
  enforcement, not tunable internals).
- Added `description`, `keywords`, `title`, and `TITLE` to `ALLOWED_KEYS`
  in
  [problems/multiple_choice_statements/check_mc_statements_yaml.py](../problems/multiple_choice_statements/check_mc_statements_yaml.py)
  so the validator accepts the same keys the generator already reads in
  [yaml_mc_statements_to_pgml.py](../problems/multiple_choice_statements/yaml_mc_statements_to_pgml.py).
  Five biochemistry MC statements YAMLs (enzyme_cofactors,
  enzyme_equilibrium, enzyme_inhibitors, gibbs_free_energy_equation,
  m-m_kinetics) now validate cleanly.
- Resolved pyflakes warnings by removing unused `import os` from
  [problems/biostatistics-problems/z_score_google_sheet.py](../problems/biostatistics-problems/z_score_google_sheet.py)
  and
  [problems/inheritance-problems/cytogenetic_notation/cytogenetic_notation-disorders.py](../problems/inheritance-problems/cytogenetic_notation/cytogenetic_notation-disorders.py),
  dropping the leading `f` from f-strings without placeholders in
  [problems/biochemistry-problems/enzymes/mm_lib.py](../problems/biochemistry-problems/enzymes/mm_lib.py)
  (3 lines),
  [problems/biochemistry-problems/membranes/_qc_membrane_pgmls.py](../problems/biochemistry-problems/membranes/_qc_membrane_pgmls.py)
  (1 line), and
  [problems/biochemistry-problems/membranes/_visual_qc_v4.py](../problems/biochemistry-problems/membranes/_visual_qc_v4.py)
  (1 line), and removing an unused `lower = html.lower()` in
  `_qc_membrane_pgmls.py`.
- Fixed mixed-indentation in
  [problems/biochemistry-problems/membranes/_qc_membrane_pgmls.py](../problems/biochemistry-problems/membranes/_qc_membrane_pgmls.py)
  by extracting a multi-line tuple of double-escape regex patterns into
  a tab-indented `double_escape_patterns` constant before the `for` loop,
  replacing the space-aligned continuation that was tripping
  `tests/test_indentation.py`.
- Added `# nosec B310` annotation to the hardcoded-localhost
  `urllib.request.urlopen` call in
  [topic_classifier/classifier_common.py](../topic_classifier/classifier_common.py)
  so Bandit no longer flags the Ollama probe; the URL is constructed from
  a fixed `http://localhost:11434` default and is not user-supplied.

### Removals and Deprecations
- Removed `test_yaml_match_to_pgml_inline_colors` from
  [tests/test_pgml_generators.py](../tests/test_pgml_generators.py). Per
  [docs/PYTHON_STYLE.md](PYTHON_STYLE.md), tests should not assert on
  internal Perl variable names (`%answer_html`, `$answers_sorted_html`),
  exact color hex literals, or tunable Unicode-vs-HTML representations of
  H<sub>2</sub>O - all of which this single test asserted. Its purpose
  (verifying replacement_rules and HTML pass-through) is already covered
  by the inline-color tests for sibling generators and by the
  per-function `webwork_lib` tests.

## 2026-04-26

### Behavior or Interface Changes
- Bumped the `membrane_transporter_svg` block from v4 to v5 in all three
  production PGMLs
  ([identify_transporter_type.pgml](../problems/biochemistry-problems/membranes/identify_transporter_type.pgml),
  [coupled_transport_perturbation.pgml](../problems/biochemistry-problems/membranes/coupled_transport_perturbation.pgml),
  [driving_force_from_gradient.pgml](../problems/biochemistry-problems/membranes/driving_force_from_gradient.pgml)).
  The v4 head-row dot loop in `svg_backdrop` is replaced by a doublet-based
  phospholipid bilayer: each doublet is one head-down phospholipid plus its
  rotate-180 mirror about the membrane midline (y=110). The phospholipid
  shape is copied verbatim from
  [problems/biochemistry-problems/membranes/phospholipid-unit.svg](../problems/biochemistry-problems/membranes/phospholipid-unit.svg)
  and inlined as `$PHOSPHO_UNIT_SVG` in each PGML so files stay
  self-contained for upload. Protein body, arrows, blobs, gradient dots,
  labels, and randomization logic are unchanged.

### Decisions and Failures
- Did not port the broader v5 plan (P5 channel + ion/sugar shape tokens)
  yet; user scoped the change to the bilayer rendering only. The protein
  remains the v4 waisted slab with the dashed gate.

## 2026-04-23

### Additions and New Features
- Added `v5_prototypes` render mode to
  [problems/biochemistry-problems/membranes/_svg_lineup.py](../problems/biochemistry-problems/membranes/_svg_lineup.py)
  and wrote three static antiporter prototypes
  (`_proto_v5_a.html`, `_proto_v5_b.html`, `_proto_v5_c.html`) as
  Phase 3 of the membrane transporter v5 rework. All three use
  protein P4 (rounded channel body with an explicit pore, derived
  from the source file `Scheme_facilitated_diffusion_in_cell_membrane-en.svg`)
  and the same biology (3 Na<sup>+</sup> in / 1 Ca<sup>2+</sup> out).
  A uses M_FLAT_SLAB, B uses M_TWO_LINE, C reuses A and adds a
  side legend showing the ion / sugar / water / nucleotide token
  primitives. Phase 4 (human review gate) is pending; no PGML
  files have been touched yet.
- Added substrate-shape dispatcher (`svg_substrate_token`) and
  primitives (`svg_token_ion`, `svg_token_sugar`, `svg_token_water`,
  `svg_token_nucleotide`) plus a `SUB_META` lookup table to
  [_svg_lineup.py](../problems/biochemistry-problems/membranes/_svg_lineup.py).
  Callers look up a substrate by key (`'Na'`, `'glucose'`, ...) and
  get label, color, and chemical-class kind; kind drives the token
  shape so ions render as circles, sugars as hexagons, water as a
  small circle, and nucleotides as rounded rectangles.
- Extended [tests/test_webwork_lib.py](../tests/test_webwork_lib.py)
  with eight `smart_title_case` tests covering acronym preservation (tRNA, DNA, pH), leading lowercase
  acronyms, apostrophes (Franklin's), HTML subscripts
  (T<sub>m</sub>), HTML entities (&middot;), leading minor words
  (a, the), and the compound case `structure of tRNA synthetases`.
- Added `smart_title_case(text)` to [webwork_lib.py](../webwork_lib.py)
  so title-casing is available to every generator that writes an OPL
  header (multiple-choice statements today, matching generators next).
  Rule: only lowercase -> uppercase, never the reverse. Words that
  already carry any uppercase letter are left alone (DNA, tRNA, pH,
  Franklin's, T<sub>m</sub>, G&middot;U). Minor connector words
  (a, an, and, of, the, to, in, on, at, by, for, with, ...) stay
  lowercase unless they lead the title. HTML tags and entities are
  skipped over so their internal characters keep their case.
- `problems/multiple_choice_statements/yaml_mc_statements_to_pgml.py` now
  assigns the YAML `topic` to the OPL `TITLE` header line when no explicit
  `title` / `TITLE` key is set, running it through
  `webwork_lib.smart_title_case` first since topics are usually a
  lowercase sentence fragment. Existing YAMLs with a `title` key retain
  their value.

### Behavior or Interface Changes
- Relabeled the non-canonical distractor in
  [problems/biochemistry-problems/PUBCHEM/NUCLEOBASES/match_purine_structures.pgml](../problems/biochemistry-problems/PUBCHEM/NUCLEOBASES/match_purine_structures.pgml)
  and
  [problems/biochemistry-problems/PUBCHEM/NUCLEOBASES/match_pyrimidine_structures.pgml](../problems/biochemistry-problems/PUBCHEM/NUCLEOBASES/match_pyrimidine_structures.pgml)
  so students no longer need to know specific non-canonical nucleobase names
  (e.g. `5-methylcytosine`, `7-methylguanine`). The correct dropdown choice
  for the distractor structure is now the generic label `uncommon purine` /
  `uncommon pyrimidine`. The actual chemical name is revealed in the PGML
  solution block instead.
- Shrank the RDKit canvas size for the two nucleobase matching problems
  from 480x320 to 360x240 pixels for a more compact layout.
- Added a dummy `[Rb]` (Rb = ribose) heavy atom at the glycosidic nitrogen
  (N9 for purines, N1 for pyrimidines) in every SMILES in the two
  nucleobase matching problems, giving students a visual cue for the
  ribose attachment point. `7-methylguanine` is drawn in its N7-methylated
  cation form (as it appears in the mRNA 5' cap), which is the form where
  N9 is free to bear a glycosidic substituent.
- Added a sentence to both nucleobase matching question statements
  explaining that the `Rb` atom marks where the ribose sugar would attach.
- Expanded both nucleobase matching statements with a one-sentence
  background on purine vs pyrimidine ring structure, and bolded the key
  terms (`purine` / `pyrimidine`, `Rb`) for readability.
- Colored the four DNA nucleotide full names in
  [problems/multiple_choice_statements/molecular_biology/melting_Tm_type_1.yml](../problems/multiple_choice_statements/molecular_biology/melting_Tm_type_1.yml),
  [melting_Tm_type_2a.yml](../problems/multiple_choice_statements/molecular_biology/melting_Tm_type_2a.yml),
  and [melting_Tm_type_2b.yml](../problems/multiple_choice_statements/molecular_biology/melting_Tm_type_2b.yml)
  using Sanger/ABI chromatogram conventions sourced from the
  pre-approved palette in
  [problems/multiple_choice_statements/TEMPLATE.yml](../problems/multiple_choice_statements/TEMPLATE.yml):
  cytosine blue (`#003fff`), thymine red (`#d40000`), adenine green
  (`#007a00`), guanine black (`#000000`, bold only). Swapped the
  `decrease` / `DECREASE` / `decreases` highlight from `MediumBlue`
  to PURPLE (`#a719db`) to avoid colliding with cytosine-blue;
  `increase` / `INCREASE` / `increases` moved from `OrangeRed` to
  DARK ORANGE (`#b74300`) to match the pre-approved palette entry.
  All three regenerated PGMLs pass renderer-API lint.

### Fixes and Maintenance
- Fixed `<br/>` tags in multiple-choice statement YAMLs rendering as
  literal `\n` in the browser. Root cause: `strip_html_tags` converts
  `<br/>` into a real newline character, which then becomes the
  literal two-character sequence `\n` when emitted inside a Perl
  single-quoted string (`$x = 'a\nb'` -- `\n` is two chars in single
  quotes). Sheltered `<br>`, `<br/>`, and `<br />` variants in
  [webwork_lib.py](../webwork_lib.py)'s `sanitize_text_for_html` so
  line-break tags survive through the HTML pipeline, normalized to
  the canonical `<br/>` form on restore. Regenerated
  `melting_Tm_type_1.pgml` (which newly uses `<br/>` to split each
  answer stem from its condition clause); rendered HTML now carries
  intact `<br/>` with no literal `\n` text.
- Fixed `franklin_diffraction.pgml` failing to render with
  `Unknown regexp modifier "/h"` / `syntax error`. Root cause: the
  generator emitted Perl single-quoted strings with `\'` to escape
  apostrophes ("Franklin's"), but PG's Safe-compartment parser does
  not honor that escape and ended the string at the apostrophe, so
  the rest of the sentence was consumed as a `s///` regex. Added
  `webwork_lib.perl_string_literal(text)` that returns `'...'` when
  no apostrophe is present and `q{...}` (escaping `\\`, `{`, `}`)
  when one is, and routed `$topic` and `$question_true` /
  `$question_false` emissions in
  [yaml_mc_statements_to_pgml.py](../problems/multiple_choice_statements/yaml_mc_statements_to_pgml.py)
  through it. Regenerated PGML now passes renderer-API lint.
  Documented by the "Apostrophes in Perl ... strings" pitfall in
  `PG_COMMON_PITFALLS.md`.
- Replaced `&cdot;` with `&middot;` throughout
  `problems/multiple_choice_statements/molecular_biology/g-u_wobble.yml`
  and regenerated the PGML. `&cdot;` is an HTML5-only entity (U+22C5)
  that does not render in some WeBWorK display paths; `&middot;`
  (U+00B7) is the HTML4 middle-dot entity, universally rendered, and
  already on the repo's entity-survival list. Verified via renderer
  API lint (clean) and by grepping the rendered HTML for intact
  `&middot;` (no double-escape to `&amp;middot;`).
- Hardened `problems/multiple_choice_statements/yaml_mc_statements_to_pgml.py`
  against null/missing required YAML fields. Added `validate_yaml_data()`
  that runs right after `yaml.safe_load` and raises `ValueError` naming
  the file and offending field (`topic` must be a non-empty string; at
  least one of `true_statements` / `false_statements` must be a
  non-empty mapping). Replaced the silent `.get("topic", "this topic")`
  default with a direct `yaml_data["topic"]` lookup so a null `topic:`
  fails fast with a clear message instead of surfacing four frames deep
  as `TypeError: value is not string: None` inside
  `webwork_lib.apply_replacement_pairs_to_text`. The script now also
  prints `Topic: <value>`, `Folder: <folder>  |  dbsubject: <value>`,
  `Statement counts: True: N statements, False: M statements`, and (when
  set) `Override (TRUE stem): ...` / `Override (FALSE stem): ...` before
  generation so the user can eyeball
  the inputs that drove the output.

### Behavior or Interface Changes
- Updated the four fatty-acid skeletal-structure PGMLs in
  [problems/biochemistry-problems/lipids/](../problems/biochemistry-problems/lipids/)
  (`fatty_acid_match_delta.pgml`, `fatty_acid_match_omega.pgml`,
  `fatty_acid_naming_delta.pgml`, `fatty_acid_naming_omega.pgml`) so that
  each cis `C=C` parallel inner line is drawn on the concave (interior)
  side of the kink instead of always above the main bond line. Top-kink
  cis bonds now render with the inner line below the main line; bottom-kink
  cis bonds keep the inner line above. The side is chosen by comparing the
  flat cis bond y to the nearest non-bond neighbor vertex (preferring the
  vertex before the cis bond; falling back to index `i+2` when the cis
  bond starts at vertex 0).
- Restyled chain bonds in the same four PGMLs for visual emphasis: both
  strokes of every `C=C` are now drawn in dark green (`#1b5e20`) at
  `stroke-width="2.4"`; single bonds are drawn in dark gray (`#222`) at
  width 2. `svg_line` gained optional stroke-color and stroke-width
  parameters (default still `#000` / `2`), and each PGML's embedded block
  headers were bumped: `svg_primitives_lipids (v3) -> (v4)` and
  `fatty_acid_svg_builder (v1) -> (v2)` where that block is present.
- Restyled the Delta/omega notation labels in the same four lipid PGMLs to
  match the `18:3` colon-shorthand styling used in
  `quick_fatty_acid_colon_system.pgml`: monospace font, `1.25em` size,
  bold. Previously rendered in a bold serif at the default size.

### Additions and New Features
- Added two nucleobase structure-matching problems under
  [problems/biochemistry-problems/PUBCHEM/NUCLEOBASES/](../problems/biochemistry-problems/PUBCHEM/NUCLEOBASES/):
  `match_purine_structures.{py,pgml}` and
  `match_pyrimidine_structures.{py,pgml}`. Each question displays the
  canonical bases for its class (adenine/guanine for purines;
  cytosine/thymine/uracil for pyrimidines) plus exactly one
  non-canonical base as a distractor drawn from a same-class pool
  (purines: isoguanine, 7-methylguanine; pyrimidines: 5-methylcytosine,
  5-hydroxymethylcytosine, dihydrouracil). Both BBQ generators use
  `moleculelib.generate_html_for_molecule` for Blackboard-sanitizer-safe
  RDKit loading (matches the working amino-acid matcher). PGML files
  mirror `PUBCHEM/AMINO_ACIDS/match_amino_acid_structures.pgml`: seeded
  `PGrandom`, `parserPopUp.pl` widgets, flexbox two-column layout (no
  `<table>`), and RDKit `HEADER_TEXT` block. Helper
  [nucleobaselib.py](../problems/biochemistry-problems/PUBCHEM/NUCLEOBASES/nucleobaselib.py)
  is co-located in `NUCLEOBASES/` (only used by the two matchers) and
  centralizes canonical/non-canonical name lists, SMILES strings, and a
  deterministic `pick_distractor(class, rng)` helper.
- Added five new bptools Python generators in
  [problems/biochemistry-problems/lipids/](../problems/biochemistry-problems/lipids/)
  that mirror the four PGML lipid items, plus a shared library:
  [fatty_acid_lib.py](../problems/biochemistry-problems/lipids/fatty_acid_lib.py)
  (ASCII-art renderer, pool-elimination position picker, omega/Delta
  notation HTML helpers); and the four scripts
  [fatty_acid_naming_omega.py](../problems/biochemistry-problems/lipids/fatty_acid_naming_omega.py),
  [fatty_acid_naming_delta.py](../problems/biochemistry-problems/lipids/fatty_acid_naming_delta.py),
  [fatty_acid_match_omega.py](../problems/biochemistry-problems/lipids/fatty_acid_match_omega.py),
  [fatty_acid_match_delta.py](../problems/biochemistry-problems/lipids/fatty_acid_match_delta.py).
  ASCII art reuses the courier-span + `&#8215;` (low double bond) and
  `<sup>&#9552;</sup>` (high double bond) glyphs from the original
  `fatty_acid_naming.py`, but with a clean cis-aware walker: at each
  bond, single bonds alternate y; cis double bonds emit a flat glyph at
  the current y and do NOT flip direction, producing the visible kink.
  All five files are ASCII-only (verified with `tests/test_ascii_compliance.py`)
  and pyflakes-clean. Note: `&lt;table&gt;` is allowed in Blackboard but
  was deemed to offer no advantage over ASCII art for these zigzag
  skeletons.
- Added two reverse-direction WeBWorK PGML lipid problems in
  [problems/biochemistry-problems/lipids/](../problems/biochemistry-problems/lipids/):
  [fatty_acid_match_omega.pgml](../problems/biochemistry-problems/lipids/fatty_acid_match_omega.pgml)
  and [fatty_acid_match_delta.pgml](../problems/biochemistry-problems/lipids/fatty_acid_match_delta.pgml).
  Inverse of the existing fatty_acid_naming_*.pgml pair: prompt shows
  the notation (e.g., omega-3,12,17), four choices are SVG skeletal
  structures. Distractor strategy (priority order, dedup keeps first 4):
  correct, wrong-end-misread (the most pedagogical -- catches students who
  confuse omega with Delta), off-by-one shift toward COOH, off-by-one
  shift toward methyl, two random-scatter backups. Backup pool is needed
  because palindromic omega positions like 7,10,13 in a 20-carbon chain
  produce identical "correct" and "misread" SVGs (mirror collision).
  Reuses svg_primitives_lipids (v3), fatty_acid_layout (v3), plus new
  blocks fatty_acid_svg_builder (v1) and pool_eliminate_positions (v1).
- Added four WeBWorK PGML lipid problems paralleling the existing Blackboard generators in
  [problems/biochemistry-problems/lipids/](../problems/biochemistry-problems/lipids/):
  [quick_fatty_acid_colon_system.pgml](../problems/biochemistry-problems/lipids/quick_fatty_acid_colon_system.pgml)
  (text-only MC, interpret the chain:bonds colon shorthand),
  [which_lipid-chemical_formula.pgml](../problems/biochemistry-problems/lipids/which_lipid-chemical_formula.pgml)
  (HTML subscript molecular formulas, lipid vs hydrophilic distractors),
  [fatty_acid_naming_omega.pgml](../problems/biochemistry-problems/lipids/fatty_acid_naming_omega.pgml),
  and [fatty_acid_naming_delta.pgml](../problems/biochemistry-problems/lipids/fatty_acid_naming_delta.pgml)
  (inline-SVG zigzag of an unsaturated fatty acid with chosen double-bond
  positions; ask for omega or Delta notation respectively). The fatty-acid
  pair carries identical `# ==== BEGIN BLOCK: svg_primitives_lipids (v3) ====`
  and `# ==== BEGIN BLOCK: fatty_acid_layout (v3) ====` chunks; bump the
  version when either block changes. The fatty-acid SVG uses standard
  skeletal-formula geometry: bonds at +/- 30 degrees from horizontal
  (internal angle 120 degrees) and cis double bonds drawn as flat
  horizontal segments between two carbons at the same y, after which the
  zigzag direction does not flip -- producing the characteristic cis kink.
  Tightened the question to a Level 3 applied-nomenclature item: chain
  length 16-22, 2-3 cis double bonds placed by pool-elimination across
  the full valid range [3..chain_length-2] with minimum spacing of 3
  enforced by removing +/- 2 around each pick. Bonds can land scattered
  across the whole chain (e.g., omega-3,12,17) instead of always
  clustering together, which forces students to read the diagram instead
  of pattern-matching on memorized PUFA shapes like omega-3,6,9. Spacing
  2 is excluded because it would be a conjugated diene (CLA-style),
  a different topic from standard PUFA nomenclature. terminal H<sub>3</sub>C and COOH
  labels only, no internal carbon labels, plus a one-sentence cue in the
  prompt that vertices and line ends represent carbon atoms. The
  double-bond cluster slides freely along the chain (methyl end, middle,
  or near COOH) by varying the first omega from 3 up to
  (chain_length - 2 - total_span). Earlier drafts allowed spacing 2,
  which would create conjugated dienes (CLA-style chemistry) and is not
  what's being assessed. Distractor set always includes the delta-swap
  as the pedagogically meaningful wrong answer.

### Fixes and Maintenance
- Rotated active changelog: moved 30 day blocks (2026-04-14 through
  2026-01-23, 779 lines) into [docs/CHANGELOG-2026-04a.md](CHANGELOG-2026-04a.md),
  using the documented `docs/CHANGELOG-YYYY-MM[a-z].md` naming. Repaired
  a content-integrity bug: the 2026-01-22 day block was present
  identically in both the active changelog and the legacy archive,
  violating the existing rule that a date heading must not be split
  across files. The active duplicate was removed before rotation; the
  archived copy was kept as canonical.
- Renamed the legacy `docs/CHANGELOG_ARCHIVE_01.md` to
  [docs/CHANGELOG-2026-01a.md](CHANGELOG-2026-01a.md) via `git mv` so
  history is preserved. The archive's date range is 2025-12-27 through
  2026-01-22; the most recent month included is 2026-01. The repo now
  uses a single archive naming style (`CHANGELOG-YYYY-MM[a-z].md`) end
  to end.
- Updated [docs/REPO_STYLE.md](REPO_STYLE.md) (and the central copy in
  `~/nsh/starter-repo-template/docs/REPO_STYLE.md`) with two
  clarifications: (1) when an archived range spans multiple months the
  archive filename uses the **most recent** month included, not the
  earliest -- this case was unspecified in the original style guide and
  surfaced when this rotation moved a January-through-April range into
  one archive; and (2) made the existing "do not split entries from the
  same date heading across files" rule explicit by adding the phrase
  "appears in exactly one file" -- the original wording was
  technically correct but easy to misread, which is how the
  2026-01-22 duplication slipped through. Also rewrote the legacy
  archive clause from "preserve as legacy" to "must be renamed via
  `git mv`" so the repo holds only one naming style at a time.

### Decisions and Failures
- First lipid PGML drafts failed renderer compile with "Problem failed
  during render - no PGcore received." Root causes were Safe-compartment
  restrictions documented in
  [PG_COMMON_PITFALLS.md](../../.claude/skills/webwork-writer/references/docs/webwork/PG_COMMON_PITFALLS.md):
  (1) `sort` and `sort { $a <=> $b }` are trapped, replaced with pre-sorted
  hardcoded key lists in `which_lipid-chemical_formula.pgml` and a
  reverse-iteration ascending-walk in the fatty-acid files; (2) `\@array`
  references are broken in PG, so the helper `build_fatty_acid_svg(\@omegas)`
  and `list2html('&omega;', \@list)` patterns were inlined / refactored to
  pass pre-joined scalars (block versions bumped from v1 to v2 to mark the
  drift). All four files now lint clean via the renderer API at
  http://localhost:3000.
- Added four WeBWorK PGML carbohydrate problems paralleling the existing Blackboard generators:
  [convert_Fischer_to_Haworth.pgml](../problems/biochemistry-problems/carbs/convert_Fischer_to_Haworth.pgml),
  [convert_Haworth_to_Fischer.pgml](../problems/biochemistry-problems/carbs/convert_Haworth_to_Fischer.pgml),
  [D_to_L_Fischer_configuration.pgml](../problems/biochemistry-problems/carbs/D_to_L_Fischer_configuration.pgml),
  [D_to_L_Haworth_configuration.pgml](../problems/biochemistry-problems/carbs/D_to_L_Haworth_configuration.pgml).
  Each file renders a Fischer/Haworth SVG of the prompt sugar plus 5
  RadioButtons-wrapped SVG distractors, generated by porting the minimal
  subset of `sugarlib.py` (flip_position, get_enantiomer_code_from_code,
  Fischer/Haworth renderers) to Perl. Fischer/Haworth conversion problems
  include `BEGIN_PGML_HINT` blocks explaining the Rosanoff OH-side rule
  (Fischer right = Haworth down).
- Added [_spike_svg_choice.pgml](../problems/biochemistry-problems/carbs/_spike_svg_choice.pgml),
  a two-choice spike confirming `parserRadioButtons.pl` accepts full SVG
  diagrams as choice labels (rendered verbatim inside `<label>`, not
  sanitised).

### Decisions and Failures
- Each PGML is self-contained (no shared `.pl` macro), because WeBWorK
  uploads problem files individually. Reusable logic is wrapped in
  labelled `# ==== BEGIN BLOCK: <name> (v<N>) ====` sections so the blocks
  can be copy-pasted verbatim across files; bump the `v<N>` when the
  block changes to surface drift with grep.
- Switched from array refs (`\@chirals`) to flat string args after hitting
  "Not an ARRAY reference" inside PG's Safe compartment. Candidate
  (code, anomeric) pairs are stored as `"code|anomer"` strings for the
  same reason, then split with `split(/[|]/, $key, 2)` -- the escaped
  `\|` form is silently treated as an empty regex by PG's Safe regex
  engine and splits between every character. New pitfall added to
  `webwork-writer/references/docs/webwork/PG_COMMON_PITFALLS.md`.
- HTML entities (`&alpha;`, `&beta;`) in PGML body text double-escape to
  `&amp;alpha;`; entities must live in a Perl variable rendered with
  `[$var]*` passthrough. Applied to every Haworth-prompt PGML body.
- Updated [~/.claude/skills/webwork-writer/SKILL.md](../../.claude/skills/webwork-writer/SKILL.md)
  with a new "Self-contained PGML files" section documenting the
  per-file inlining convention and the `BEGIN BLOCK` versioning scheme.

### Developer Tests and Notes
- Verified all four PGMLs render cleanly at seeds 1, 42, 100, 9999 via
  the local renderer API (`lint_pg_via_renderer_api.py --json`): 5
  `<label>`s, 6 `<svg>`s (1 prompt + 5 choices), zero
  `&amp;alpha;/&amp;beta;` double-escapes, `error_flag = None`.

## 2026-04-19

### Behavior or Interface Changes
- [topic_classifier/classify_scripts.py](../topic_classifier/classify_scripts.py) now runs one classification per `(script, flags, input)` variant defined in `biology-problems-website/bbq_control/task_files/*.csv`, instead of classifying each script path once with the first variant it found. Scripts with multi-variant CSV rows (e.g. `classify_Haworth.py --furan`/`--pyran`, `which_amino_acid.py --mc`/`--fib`, `protein_gel_migration.py --mc`/`--num`) now get a distinct classification and a CSV output row per variant. Output CSV rows populate the `flags` and `input` columns so the generated CSVs round-trip with the control files. Dry-run prints the expanded work list. Scripts not present in any CSV still classify once with no flags.
- Added `csv_handler.get_variants_for_script(assignments, script_path)` in [topic_classifier/csv_handler.py](../topic_classifier/csv_handler.py) that enumerates `{flags, input}` variants for a script, returning a single empty variant when the script has no CSV rows so callers always have at least one work unit.
- [topic_classifier/classify_scripts.py](../topic_classifier/classify_scripts.py) `classify_one_script(...)` now takes explicit `flags=""` and `input_file=""` parameters instead of looking them up from `assignments`, and populates those fields on the returned result dict. Replaced internal `_get_run_args(script, assignments)` with `_build_run_args(flags, input_file, repo_root)`. Existing-assignment match lookup keys directly on `f"{bp_root_path}|{flags}"` for per-variant diff accuracy. Repeat/consistency bookkeeping (`repeat_results`, `no_bbq_scripts`, `llm_error_scripts`) keys by `f"{script}|{flags}"` so variant runs do not collide.

### Fixes and Maintenance
- Fixed `BBQ_CONTROL_DIR` in [topic_classifier/classify_scripts.py](../topic_classifier/classify_scripts.py) to point at `biology-problems-website/bbq_control/task_files/` (where the variant CSVs actually live) instead of `biology-problems-website/bbq_control/`. Previously `read_existing_assignments()` found zero CSVs and loaded 0 assignments, which silently disabled the existing-assignment match check and any variant-aware behavior.
- Made 14 previously silent bptools generators produce questions by default (tracked in [topic_classifier/results-gemma4_q8/no_bbq_file.csv](../topic_classifier/results-gemma4_q8/no_bbq_file.csv)). Running any of these scripts with no arguments now writes a `bbq-*-questions.txt` file.
  - Category A - changed `required=True` to `required=False, default='mc'` on `bptools.add_question_format_args(...)` in 6 gene_mapping generators: [tetrad_ordered-centromere_distance.py](../problems/inheritance-problems/gene_mapping/tetrad_ordered-centromere_distance.py), [tetrad_unordered_three_gene-find_one_distance.py](../problems/inheritance-problems/gene_mapping/tetrad_unordered_three_gene-find_one_distance.py), [tetrad_unordered_two_gene-find_distance.py](../problems/inheritance-problems/gene_mapping/tetrad_unordered_two_gene-find_distance.py), [three-point_test_cross-find_interence.py](../problems/inheritance-problems/gene_mapping/three-point_test_cross-find_interence.py), [three-point_test_cross-one_gene_distance.py](../problems/inheritance-problems/gene_mapping/three-point_test_cross-one_gene_distance.py), [two-point_test_cross-distance.py](../problems/inheritance-problems/gene_mapping/two-point_test_cross-distance.py).
  - Category A (custom groups) - added `parser.set_defaults(...)` and dropped `required=True` on the parental/recombinant and parental/double/genes mutually exclusive groups in [two-point_test_cross-which_genotypes.py](../problems/inheritance-problems/gene_mapping/two-point_test_cross-which_genotypes.py) and [three-point_test_cross-which_genotypes.py](../problems/inheritance-problems/gene_mapping/three-point_test_cross-which_genotypes.py) (default `parental`).
  - Category B - added `parser.set_defaults(mode="same")` to the `--same`/`--different` group in [gene_tree_matches_plus.py](../problems/inheritance-problems/phylogenetic_trees/gene_tree_matches_plus.py).
  - Category C - added sys.path insertion for the sibling `inheritance-problems/` directory so `import genotypelib` resolves in [unique_gametes.py](../problems/inheritance-problems/large_crosses/unique_gametes.py), [unique_cross_genotypes.py](../problems/inheritance-problems/large_crosses/unique_cross_genotypes.py), and [unique_cross_phenotypes.py](../problems/inheritance-problems/large_crosses/unique_cross_phenotypes.py). Matches the pattern already used in [dihybrid_cross_epistatic_gene_interactions.py](../problems/inheritance-problems/epistasis/dihybrid_cross_epistatic_gene_interactions.py).
  - Category D - replaced hard-coded `problems/*/data/<file>` paths with `bptools.get_repo_data_path("<file>")` in [z_score_google_sheet.py](../problems/biostatistics-problems/z_score_google_sheet.py) (`student_names.txt`) and [cytogenetic_notation-disorders.py](../problems/inheritance-problems/cytogenetic_notation/cytogenetic_notation-disorders.py) (`cytogenetic_disorders.yml`). Both files live at the repo-root `data/` directory.
  - Deferred: [wordle_peptides.py](../problems/biochemistry-problems/PUBCHEM/PEPTIDES/wordle_peptides.py) still fails with an lxml XML parse error on cached HTML (separate bug, not a defaults issue).

### Decisions and Failures
- `bptools.add_question_format_args(...)` (bptools.py:364) already supported `required=False, default=...`. No change to `bptools.py` was necessary - the Category A fix is purely site-local updates to the script parse_arguments calls, matching the pattern endorsed in [docs/PYTHON_STYLE.md](PYTHON_STYLE.md) (ARGPARSE section).

