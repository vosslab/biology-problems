# Changelog

## 2026-06-24

### Additions and New Features
- Added [active_plans/reports/ultra_classic_showcase_question_catalog.md](active_plans/reports/ultra_classic_showcase_question_catalog.md):
  a catalog of every question generator evaluated for the Blackboard Classic vs Ultra
  HTML-sanitization showcase, the seven sanitization-failure classes, the selected twelve,
  and the reason each considered-but-unused generator was left out (mostly redundant failure
  class or too long for an IT-facing demo). Documents both the MC/MA/NUM/FIB candidates and
  the matching-set candidates evaluated for the double-duty matching slot.

### Behavior or Interface Changes
- Re-curate [devel/ultra_classic_showcase.py](../devel/ultra_classic_showcase.py) into a
  pure-short, failure-mode-ordered set of twelve generators across four question types (MC, MA,
  MATCH, FIB; was eight to twelve, several long). The audience is IT staff reviewing failure
  modes, not students, so each item is a SHORT question that isolates one HTML-sanitization
  failure, and generators are ordered worst-first to match the companion request-to-retain-Learn
  email: content destroyed (color/script/layout carries the data), then color-as-convenience,
  then a clean control, then the structural type-drop. Added generators:
  [hla_genotype.py](../problems/dna_profiling-problems/hla_genotype.py) `--num-markers 3`
  (inline marker color marks which parental chromosome each marker came from; required, short
  pure-text MC), [pipet_size_mc.py](../problems/laboratory-problems/pipet_size_mc.py) (small MC
  whose red digits encode decimal place value, stacking several failures in a tiny footprint),
  [metabolic_pathway_inhibitor.py](../problems/biochemistry-problems/enzymes/metabolic_pathway_inhibitor.py)
  (color = identity, figure to text),
  [which_amino_acid.py](../problems/biochemistry-problems/PUBCHEM/AMINO_ACIDS/which_amino_acid.py)
  (smaller RDKit.js `<canvas>` script-render probe),
  [linear_digest.py](../problems/molecular_biology-problems/linear_digest.py) `--length 8
  --num-sites 2` (table-spacing digest ruler),
  [monohybrid_genotype_statements.py](../problems/inheritance-problems/monohybrid_genotype_statements.py)
  (color disambiguates similar AA/Aa/aa tokens),
  [photosynthetic_light_pigments.py](../problems/biochemistry-problems/photosynthetic_light_pigments.py)
  (colored wavelength terms), and
  [michaelis_menten_table-Km.py](../problems/biochemistry-problems/enzymes/michaelis_menten_table-Km.py)
  (zebra-stripe row background for readability). The matching slot now uses
  [column_chromatography.yml](../problems/matching_sets/laboratory/column_chromatography.yml)
  (was degrees_of_dominance): it does double duty, proving the QTI Matching type-drop while
  reinforcing color=identity (colored IEX/AC/HIC/SEC type names recur across the descriptions).
  Dropped as long or redundant: kaleidoscope_ladder
  (colored gel ladder is big and hard for a non-expert to parse; color=data covered by the
  deletion map and HLA, removing the only NUM item), protein_gel_migration (duplicate gel),
  which_macromolecule (replaced by the smaller amino-acid RDKit item), three-point and two-point
  test crosses (long; type coverage is not a goal), dihybrid epistasis (long 4x4), and
  monohybrid_degrees_of_dominance (replaced by the shorter genotype-statements item). The
  combined showcase now emits 24 questions (12 generators x 2), with the leading items being
  the critical color/script/layout failures.

### Fixes and Maintenance
- Correct the question-type label for
  [classify_Haworth.py](../problems/biochemistry-problems/carbs/classify_Haworth.py) in the
  showcase docstring from MC to MA: the "select exactly five categorizations" item is
  Multiple-Answer, confirmed by the MA leading token in the generated BBQ.

### Decisions and Failures
- Curation rule for the showcase: one strong exemplar per failure class, shortest available, over
  breadth of biology topics or question types. Many strong rejected items (Robertsonian
  translocation, exon splicing, branched feedback pathways, phylogenetic trees) were left out only
  because their failure class is already covered by a shorter exemplar.
- HLA genotype was promoted from a color-identity alternate to the color=data slot (item 2): its
  marker color is required (it marks which parental chromosome each marker came from), and it is a
  short pure-text MC, the cleanest inline-text-color=data proof. pipet_size_mc was kept alongside
  it (item 3) as a small MC that stacks several failures (red place-value digits plus a mini dial
  layout) in a tiny footprint.
- The matching item is chosen for double duty: it must prove the QTI type-drop AND reinforce a
  color failure already shown elsewhere. column_chromatography reinforces color=identity; the
  genetics monohybrid_cross set (convenience) and the 2-pair energy_terms set (too minimal) were
  the runner-up matching candidates.
- Two failure classes remain unconfirmed pending a live Ultra import: the RDKit.js `<canvas>`
  script-render (item 5, near-certain to blank) and `font-family:monospace` alignment (probed by
  the control FIB item 11). Both probes already ship in the current packages, so no extra
  generator is needed to test them.

## 2026-06-23

### Additions and New Features
- Added [devel/ultra_classic_showcase.py](../devel/ultra_classic_showcase.py): a local
  orchestrator that demonstrates the difference between Blackboard Classic and Blackboard
  Ultra HTML sanitization. It runs five question generators that each rely on inline HTML
  that Classic keeps but Ultra strips (inline `color:` text in
  [monohybrid_degrees_of_dominance.py](../problems/inheritance-problems/monohybrid_degrees_of_dominance.py);
  table-cell `border-*` ring drawing in
  [classify_Haworth.py](../problems/biochemistry-problems/carbs/classify_Haworth.py);
  Punnett `background-color` answer key in
  [dihybrid_cross_epistatic_gene_metabolics.py](../problems/inheritance-problems/epistasis/dihybrid_cross_epistatic_gene_metabolics.py);
  positional deletion-map bars in
  [deletion_mutant_random.py](../problems/inheritance-problems/deletion_mutants/deletion_mutant_random.py);
  and a simple genetics matching set via
  [yaml_match_to_bbq.py](../problems/matching_sets/yaml_match_to_bbq.py) on
  [inheritance/degrees_of_dominance.yml](../problems/matching_sets/inheritance/degrees_of_dominance.yml)).
  It generates two questions from each generator, concatenates the ten into one BBQ upload
  file under `output_showcase/`, and converts that file to QTI v2.1 via
  qti-package-maker's `tools/bbq_converter.py` (using `--allow-mixed` because the set mixes
  MC and MA item types). Anti-cheat features are disabled for every generator
  (`--no-hidden-terms --allow-click`) so the hidden decoy terms and no-click div
  wrapper do not pollute the HTML being compared between Classic and Ultra.

### Behavior or Interface Changes
- [devel/ultra_classic_showcase.py](../devel/ultra_classic_showcase.py) now groups the generated
  questions by question type and converts each type into its own pair of packages, instead of one
  combined conversion. After running every generator it groups all BBQ lines by their leading type
  token (via a `TYPE_NAMES` map: MC, MA, MAT->MATCH, NUM, FIB, FIB_PLUS->MULTI_FIB, ORD->ORDER),
  writes `bbq-<TYPE>-questions.txt`, and runs `bbq_converter.py` with `-2 -B --allow-mixed` to emit
  both a QTI v2.1 package and a Blackboard pool export ZIP via the `blackboard_export_zip` engine
  (`-B` / `bbexport`). This yields one Ultra bank per question type (`MC`, `MA`, `MATCH`), with
  short type-named files, so banks are grouped by type rather than by generator title. All
  questions are also gathered into one combined `bbq-ultra_classic_showcase-questions.txt` for a
  single Blackboard Classic upload. New helpers: `write_named_bbq`, `convert_one`, and
  `clean_prior_outputs` (clears prior `bbq-*`, `qti21-*`, `blackboard_export_zip-*` files each run
  so the output folder stays clean), replacing the prior `convert_packages`. The QTI v2.1 package
  does contain the Matching items, but Blackboard Ultra's QTI-package import drops Matching (the
  earlier 8-of-10 result); the Blackboard pool export carries Matching into Ultra through the
  Import Pool / Import from file door.
- Expand [devel/ultra_classic_showcase.py](../devel/ultra_classic_showcase.py) to eight generators
  spanning all six supported question types (was five, covering MC/MA/MATCH only). Added FIB
  ([overhang_sequence.py](../problems/molecular_biology-problems/overhang_sequence.py) `--fib`,
  matching the real Ch02.4 Overhang sample), MULTI_FIB
  ([three-point_test_cross-distances_plus.py](../problems/inheritance-problems/gene_mapping/three-point_test_cross-distances_plus.py),
  matching the real Ch05.3 Three-Point sample), and NUM
  ([protein_gel_migration.py](../problems/biochemistry-problems/electrophoresis/protein_gel_migration.py)
  `--num`, matching the real Ch05 Gel Migration sample). The showcase now emits one Ultra bank per
  type (MC, MA, MATCH, FIB, MULTI_FIB, NUM) plus a complete combined showcase package
  (`ultra_classic_showcase` QTI v2.1 + Blackboard pool export) holding all six types in one
  package (the original showcase goal). The complete bb-export verified to carry all sixteen items
  (6 MC + 2 MA + 2 MATCH + 2 FIB + 2 MULTI_FIB + 2 NUM) with the corrected MATCH `RIGHT_MATCH_BLOCK`
  placement. NUM, FIB, and MULTI_FIB confirmed rendering correctly on live Blackboard Ultra import.
  ORDER is intentionally excluded from the showcase `TYPE_NAMES` map (out of scope and known to fail
  on Blackboard import), so an ORDER question would raise loudly rather than emit a failing bank.
- Expand the numeric (NUM) corpus in [devel/ultra_classic_showcase.py](../devel/ultra_classic_showcase.py)
  from one to three NUM generators so the NUM bank carries six varied numeric examples for testing the
  Blackboard numeric format: protein molecular weight from gel migration (decimal answers, fixed
  tolerance), unknown-band molecular weight from a Kaleidoscope ladder
  ([kaleidoscope_ladder_unknown_band.py](../problems/biochemistry-problems/electrophoresis/kaleidoscope_ladder/kaleidoscope_ladder_unknown_band.py),
  percent-based tolerance), and genetics map distance from a two-point test cross
  ([two-point_test_cross-distance.py](../problems/inheritance-problems/gene_mapping/two-point_test_cross-distance.py)
  `--num`, integer answers with a tight tolerance). The spread (small/large decimals, percent vs fixed
  tolerance, near-exact integers) stresses different numeric encodings. Evaluated and rejected
  `dna_gel-estimate_size-MC_or_NUM.py` as a fourth NUM source: it intermittently raises
  `ValueError: Distance less than zero.` on some random draws, and the showcase runs all generators
  with `check=True`, so a flaky generator aborts the whole run. Confirmed the remaining set stable
  across five consecutive runs.

### Decisions and Failures
- Dropped `titration_pI.py` from the showcase set: its CSS-drawn titration curve breaks on
  Blackboard Classic too, so it shows no Classic-vs-Ultra difference. Also rejected an
  rdkit.js example because inline `<script>` is stripped by both Classic and Ultra, again
  yielding no contrast. PNG-image fallbacks were rejected as showcase items because the
  user's pipeline does not upload images to Blackboard.
- Diagnosed why the first showcase build imported only 8 of 10 items into Blackboard Ultra:
  the two pedigree matching (MAT) items were dropped. Root cause is the import route, not a
  general Ultra limit. Blackboard's two import paths support different type sets: Question
  Bank import supports Matching, but QTI v2.1 **package** import supports only Multiple
  Choice, Fill-in-the-Blank, Essay, and True/False, so Matching is removed on QTI import
  (and Multiple Answer is converted to multi-select Multiple Choice, which is why the two
  Haworth MA items survived as MC). Sources: Blackboard help "Question banks"
  (https://help.anthology.com/blackboard/instructor/en/assessments/questions/reuse-questions/question-banks.html)
  and "QTI packages"
  (https://help.anthology.com/blackboard/instructor/en/assessments/questions/reuse-questions/qti-packages.html).
  Replaced the pedigree matching generator with a minimal genetics matching set
  (`yaml_match_to_bbq.py` on `degrees_of_dominance.yml`) so the QTI matching-drop is
  reproduced with a simple, non-HTML matching item, isolating the type limitation from any
  pedigree-specific HTML.

## 2026-06-10

### Fixes and Maintenance
- Corrected [problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md](../problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md):
  corrected the stale module name `pedigree_graph_parse_lib` to
  `pedigree_lib/graph_parse.py` and its compiler function to `compile_graph_spec_to_code()`;
  clarified that `LayoutGraph` is not a Python class and not a persisted data structure --
  it is only a conceptual label for an intermediate layout step computed inside graph_parse.py;
  completed the library-roles table with five previously omitted modules
  (`genetic_assignment.py`, `genetic_validation.py`, `label_strings.py`,
  `graph_spec.py`, `code_render.py`); deduplicated the CodeString column layout examples;
  removed a stale module-rename suggestion; added the entry-scripts and topology subsections;
  added a robustness-findings subsection; ported the implemented labeling design from
  [archive/pedigree_labeling_plan.txt](archive/pedigree_labeling_plan.txt)
  into the "Optional label strings" section.
- Corrected [problems/inheritance-problems/pedigrees/PEDIGREE_SPEC_v1.md](../problems/inheritance-problems/pedigrees/PEDIGREE_SPEC_v1.md):
  updated marry-in wording and fixed the label-example connector-cell reference.

### Removals and Deprecations
- Archived the raw design sketch `problems/inheritance-problems/pedigrees/labeling_plan.txt`
  to [archive/pedigree_labeling_plan.txt](archive/pedigree_labeling_plan.txt) via
  `git mv`; all useful content had been ported to
  [PEDIGREE_PIPELINE.md](../problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md).

## 2026-05-31

### Additions and New Features
- Added `--backend {apple,ollama,claude}` mutually exclusive argparse group to
  [classify_yaml.py](../topic_classifier/classify_yaml.py) and
  [classify_scripts.py](../topic_classifier/classify_scripts.py),
  with shortcut flags `--apple`, `-O`/`--ollama`, and `--claude`. A `resolve_backend(args)`
  helper translates the selected flag into the `backend` string passed to `create_llm_client()`.
  The `-m`/`--model` flag supplies the model name or alias for the selected backend (Ollama model
  name for `--ollama`; Claude alias such as `"sonnet"` or `"opus"` for `--claude`). Help text
  discloses that `--claude` routes prompts to the Anthropic cloud via the local `claude` CLI
  (OAuth/account login; no API key required; no new pip dependency).
- Added [metadata_loader_lib.py](../topic_classifier/metadata_loader_lib.py),
  which reads the canonical `topics_metadata.yml` from the sibling
  `biology-problems-website` repo (raises `FileNotFoundError` if absent) and returns the
  subject/topic structure the classifier needs. Each topic's identifier (`topic_id`) is the
  author-facing alias (e.g. `chi_square`) when present, else the `topicNN` key. Provides
  `load_all_indexes()`, `format_subject_list()`, and `format_topic_list()` used by classifier
  scripts and prompt builders.
- The `topic_classifier` pipeline can now assign a script or YAML question to two subjects
  (a primary plus an optional, conservatively gated secondary), one topic per subject,
  emitting one CSV row per `(script, subject)` into the existing per-subject CSV files.
  The 6-column CSV schema (`subject,topic,script,flags,input,notes`) is unchanged.
  A secondary is kept only when it is a real subject in `all_indexes`, differs from the primary
  (case-sensitive), and its stage-2 `confidence_score` >= 3.
  See [classify_scripts.py](../topic_classifier/classify_scripts.py) and
  [classify_yaml.py](../topic_classifier/classify_yaml.py).

### Behavior or Interface Changes
- Replaced the `use_ollama: bool` parameter of `create_llm_client()` in
  [classifier_common_lib.py](../topic_classifier/classifier_common_lib.py)
  with `backend: str` (values: `"apple"`, `"ollama"`, `"claude"`; default `"apple"`).
  The `model` argument is reused: Ollama model name for `"ollama"`, Claude alias
  (e.g. `"sonnet"`, `"opus"`; default `"sonnet"`) for `"claude"`, ignored for `"apple"`.
  Unknown backends raise `ValueError`. Uses `local_llm_wrapper.ClaudeCodeTransport` for
  the `"claude"` path; no new pip dependency.
- Reorganized `-O`/`--ollama` and bare `-m`/`--model` flags in
  [classify_yaml.py](../topic_classifier/classify_yaml.py) and
  [classify_scripts.py](../topic_classifier/classify_scripts.py)
  into the new mutually exclusive `--backend` group; legacy `-O` still selects ollama
  and `-m` still sets the model name/alias for the active backend.
- Classifiers now read subject and topic data from `topics_metadata.yml` via
  [metadata_loader_lib.py](../topic_classifier/metadata_loader_lib.py)
  instead of parsing subject-index Markdown files. All import sites in
  [classify_yaml.py](../topic_classifier/classify_yaml.py),
  [classify_scripts.py](../topic_classifier/classify_scripts.py),
  [prompt_builder_lib.py](../topic_classifier/prompt_builder_lib.py), and
  [compare_results.py](../topic_classifier/compare_results.py)
  now alias the module as `metadata_loader`.
- Updated [stage2_topic.yaml](../topic_classifier/prompts/stage2_topic.yaml)
  response-format block: placeholder changed from `topicNN` to `chi_square`; added explicit
  instruction "Return the exact alias shown before the colon in the topic list (e.g. chi_square),
  not a topicNN code." All 14 few-shot examples converted from `-> topicNN` targets to real
  aliases (biomolecules, protein_structure, thermodynamics, water_ph, enzyme_kinetics,
  enzyme_inhibition, allostery, protein_purification, lipids, nucleic_acids, membranes,
  carbohydrates, translation). The mRNA-codon example formerly mapped to topic09 (allostery)
  is now correctly mapped to translation (molecular biology alias).
  stage1_subject.yaml has no topicNN references and required no changes.
- `classify_one_script` and `classify_one_yaml` in
  [classify_scripts.py](../topic_classifier/classify_scripts.py) and
  [classify_yaml.py](../topic_classifier/classify_yaml.py)
  now return a list of result dicts (primary always element 0, optional secondary) instead of
  a single dict; callers iterate the list. First-run dedup keys now include the subject field
  (scripts: `(script, flags, subject)`; yaml: `((yaml_path or input), subject)`) and
  repeat-mode voting keys include subject so primary and secondary tally separately.
  [compare_results.py](../topic_classifier/compare_results.py) now stores a
  set of `(subject, topic)` pairs per script (a dual-subject script no longer overwrites) and
  renders multi-pair values as sorted `subject:topic` tokens joined by `;`.
- Removed the retired internal `chapter` terminology from `topic_classifier/*.py`.
  Script and YAML classifier result dicts now both use the `subject` key; comparison output,
  XLSX sheet names, known-overlap CSV headers, unassigned-report vote plumbing, and
  few-shot prompt examples now use `subject/topic` consistently, matching the
  `topics_metadata.yml` and BBQ task CSV format docs.

### Fixes and Maintenance
- Refreshed the doc set against the current repo. [README.md](../README.md) quick start
  now uses a live script (`alpha_helix_h-bonds.py --mc -d 5`), and the first paragraph was
  rewritten as plain prose under 250 characters (no links or code spans) to satisfy
  [tests/test_readme_first_paragraph.py](../tests/test_readme_first_paragraph.py).
- Fixed all 146 broken local Markdown links in
  [docs/CODE_ARCHITECTURE.md](CODE_ARCHITECTURE.md) and
  [docs/FILE_STRUCTURE.md](FILE_STRUCTURE.md): root-relative targets now use `../` so they
  resolve from `docs/` on GitHub, and sibling `docs/*` links drop the redundant `docs/`
  URL prefix. [tests/test_markdown_links.py](../tests/test_markdown_links.py) now passes.
- Corrected stale paths and inventory in the architecture and file-structure docs:
  added `problems/biophysics-problems/`, moved `sugarlib.py` to `carbs/` and the peptide
  web assets to `PUBCHEM/PEPTIDES/PEPTIDYLE_WEB/`, replaced the removed `run_pyflakes.sh`
  and `run_ascii_compliance.py` references with the current pytest lint gates, added a
  `devel/` tooling section, dropped the deleted root `matching_sets/` and
  `refactor-Jan_2026/` entries, and pointed the license entries at the dual
  `LICENSE.LGPL_v3` and `LICENSE.CC_BY_4_0` files.
- Rewrote [docs/INSTALL.md](INSTALL.md) and [docs/USAGE.md](USAGE.md) from current evidence:
  documented the required sibling `qti-package-maker` checkout, a verifiable install check,
  the shared `bptools` CLI flags, and corrected the dead quick-start command.
- Trimmed [AGENTS.md](../AGENTS.md) from 52 lines to a tight pointer file that links into
  `docs/*.md` instead of restating style/commit rules; dropped stale facts (`logger_config.py`,
  `read_qti/`, root `matching_sets/`, "no repo-wide test runner") and preserved the standing
  user directives verbatim.
- Removed the deleted `logger_config` module from `py-modules` in
  [pyproject.toml](../pyproject.toml) and corrected the project license to `LGPL-3.0-or-later`
  to match the shipped `LICENSE.LGPL_v3` (code) and `LICENSE.CC_BY_4_0` (content) files.

### Removals and Deprecations
- Removed `topic_classifier/index_parser_lib.py` - superseded by
  [metadata_loader_lib.py](../topic_classifier/metadata_loader_lib.py),
  which reads `topics_metadata.yml` directly. All call sites were repointed before removal.
- Removed `subject-indexes/` directory and all 7 markdown index files
  (`biochemistry-index.md`, `biostatistics-index.md`, `biotechnology-index.md`,
  `genetics-index.md`, `laboratory-index.md`, `molecular_biology-index.md`,
  `other-index.md`). Topic data now lives in
  `topics_metadata.yml`
  as a single structured YAML source.

### Fixes and Maintenance
- Added `~/nsh/local-llm-wrapper` to `PYTHONPATH` in [source_me.sh](../source_me.sh)
  so `topic_classifier` scripts can import `local_llm_wrapper` (including
  `ClaudeCodeTransport`) without a pip install. A warning is printed to stderr if the
  sibling repo directory is absent.
- Classifier output CSVs and diff comparison now use topic aliases (matching the
  `bbq_control` task CSV `topic` column) instead of `topicNN` codes; this eliminates
  false DISAGREE results where a predicted `topicNN` never matched a CSV alias.
- Verified the subject/topic terminology cleanup with targeted syntax compilation and
  pyflakes on the touched `topic_classifier` Python files.

### Decisions and Failures
- Dual-subject classification (primary + optional secondary) is scoped exclusively to
  the `topic_classifier` pipeline. Question YAML `topic` fields remain a single scalar
  and downstream `bbq`/`pgml` generators are unchanged; this does NOT introduce
  multi-topic YAML behavior.
- No secondary-confidence field is stored; a low-confidence secondary (stage-2
  `confidence_score` < 3, or subject key absent from `all_indexes`, or identical to
  primary) is silently dropped rather than emitted as a review row. Comparisons in
  [compare_results.py](../topic_classifier/compare_results.py) use
  exact set equality of `(subject, topic)` pairs, so a script assigned to two subjects
  must match both in every compared run to register as AGREE.

### Developer Tests and Notes
- Dual-subject classification feature added across six files in `topic_classifier/`:
  [stage1_subject.yaml](../topic_classifier/prompts/stage1_subject.yaml)
  gained an optional `<secondary_subject>` response tag with anti-drift guidance
  ("leave empty unless the question clearly belongs to two subjects equally") and
  empty-secondary micro-examples.
  [classifier_common_lib.py](../topic_classifier/classifier_common_lib.py)
  gained `normalize_secondary_subject(raw) -> str | None` (maps absent/empty/whitespace
  to None, else stripped string).
  [classify_scripts.py](../topic_classifier/classify_scripts.py) and
  [classify_yaml.py](../topic_classifier/classify_yaml.py): `classify_stage1`
  now parses `secondary_subject`; `classify_one_script`/`classify_one_yaml` return a list
  of result dicts (primary always element 0, optional secondary). Secondary is accepted only
  when it is a real subject key, differs from the primary (case-sensitive), and its stage-2
  `confidence_score` >= 3; otherwise dropped. `assignment_rank` ("primary"/"secondary") is
  added to result dicts for debug logging only and is NEVER written to CSV. Dedup keys and
  repeat-mode voting keys include the subject field so primary/secondary tally separately.
  [compare_results.py](../topic_classifier/compare_results.py):
  `load_results_dir` now stores a set of `(subject, topic)` pairs per script; multi-pair
  values render as sorted `subject:topic` tokens joined by `;`.
  [find_unassigned_scripts.py](../topic_classifier/find_unassigned_scripts.py)
  and [find_unassigned_yaml.py](../topic_classifier/find_unassigned_yaml.py):
  outer vote-loop unpacks a set of pairs per script; vote aggregation keys `(subject, topic)`
  unchanged.
  New test: `tests/test_secondary_subject_parse.py` (pure parser test for the
  None-vs-stripped normalization logic in `normalize_secondary_subject`).
- The 6-column CSV schema (`subject,topic,script,flags,input,notes`) is UNCHANGED;
  a dual-subject script emits one row per `(script, subject)` into the existing
  per-subject CSV files.
- pyflakes clean on all six changed `topic_classifier` files.
  `pytest tests/test_pyflakes_code_lint.py tests/test_ascii_compliance.py
  tests/test_secondary_subject_parse.py` -> 367 passed.
  Full `pytest tests/` -> 1 failed, 2391 passed. The single failure is the pre-existing
  `tests/test_shebangs.py::test_shebang_executable_alignment` (classifier_common_lib.py
  carries a shebang with mode 100644 at HEAD; not introduced by this work).
  Multi-subject CSV-split plumbing verified via a deterministic stubbed run (two rows ->
  two per-subject CSVs, one topic each). Live `--claude` dry run on a single script ran
  without crashing (observed `secondary: absent`, single-subject case).

## 2026-05-07

### Additions and New Features
- Added [tetrapeptide_net_charge.pgml](../problems/biochemistry-problems/PUBCHEM/PEPTIDES/tetrapeptide_net_charge.pgml),
  a PGML/WeBWorK question that asks for the approximate net charge of a
  random tetrapeptide at a random pH (1.0-13.0, by 0.1). Adapts the
  `polypeptide_mc_sequence-easy.pgml` SMILES builder and RDKit canvas
  pattern, but draws the peptide in fully neutral form
  (-COOH / -NH2 / -SH / -OH / neutral imidazole / neutral guanidine) so
  the structure does not give away the answer; students must compute the
  charge from the printed pKa table. The random sequence is constrained
  to contain at least 2 ionizable side chains
  (`K, R, H, D, E, C, Y`) via `pick_tetrapeptide_with_two_ionizable`,
  with a deterministic injection fallback if the random loop expires.
  Five radio choices (A-E, scantron friendly): correct + 4 distractors
  built procedurally from a uniformly chosen target sorted index
  (0..4). Distractors fill in `target_idx` consecutive offsets below
  correct and `4 - target_idx` above, so the correct answer's sorted
  position is uniform across all five buttons; display order is then
  Fisher-Yates shuffled. The pKa list rendered to the student is
  filtered to only the groups present in the drawn peptide
  (alpha-amino and alpha-carboxyl always shown; side chains only when
  their single-letter code appears in the sequence) so the list does
  not cue residues that are not there. Solution prints a per-group
  pKa-vs-pH contribution list.
- Added [tetrapeptide_net_charge.py](../problems/biochemistry-problems/PUBCHEM/PEPTIDES/tetrapeptide_net_charge.py),
  a bptools/Blackboard companion to the PGML version. Same neutral
  SMILES backbone (`N[C@@H]...(C(=O)O)`), same neutral side chains,
  same `>=2 ionizable residues` constraint, same target-sorted-index
  distractor design, the same five-choice scantron format, and the same
  per-peptide-filtered pKa list. Renders through
  `aminoacidlib.generate_html_for_molecule`, which embeds an RDKit
  canvas plus the split-comment JS pattern
  (`function/* */getPeptideBonds`) so Blackboard's HTML/JS sanitizer
  cannot rewrite the rendering script. Disables bptools' anti-cheat
  HTML wrappers (`allow_insert_hidden_terms`, `allow_no_click_div`,
  `use_nocopy_script`) so the canvas survives. Verified against 30
  generated questions: zero charged-atom tokens
  (`[NH3+]`, `[O-]`, ...) in any SMILES, all sequences contain
  >=2 ionizable side chains, and the labeled correct answer matches
  the independently computed net charge for every question.

## 2026-04-30

### Behavior or Interface Changes
- Renamed files in `topic_classifier/` so library modules vs runnable
  scripts are obvious from the filename. Library modules now carry the
  repo's standard `_lib.py` suffix and the script-targeting unassigned
  finder mirrors its YAML sibling:
  [classifier_common_lib.py](../topic_classifier/classifier_common_lib.py) ->
  `classifier_common_lib.py`,
  [csv_handler_lib.py](../topic_classifier/csv_handler_lib.py) ->
  `csv_handler_lib.py`,
  `index_parser_lib.py` ->
  `index_parser_lib.py`,
  [prompt_builder_lib.py](../topic_classifier/prompt_builder_lib.py) ->
  `prompt_builder_lib.py`,
  [script_runner_lib.py](../topic_classifier/script_runner_lib.py) ->
  `script_runner_lib.py`,
  [find_unassigned_scripts.py](../topic_classifier/find_unassigned_scripts.py) ->
  `find_unassigned_scripts.py`. All renames performed via `git mv` to
  preserve history. Importers updated to use `import X_lib as X` so
  call sites keep their short aliases unchanged.

### Additions and New Features
- Added [find_unassigned_yaml.py](../topic_classifier/find_unassigned_yaml.py),
  a YAML companion to
  [find_unassigned_scripts.py](../topic_classifier/find_unassigned_scripts.py).
  It enumerates YAML content banks under
  `problems/multiple_choice_statements/*/*.yml` and
  `problems/matching_sets/*/*.yml`, marks any whose path appears in
  the `input` column of a `bbq_control` task CSV as assigned, and
  reports the unassigned remainder. Subject/topic suggestions are
  aggregated from `results-*/` classifier dirs whose entries point at
  `.yml` paths (i.e., `results-yaml*/` runs from
  [classify_yaml.py](../topic_classifier/classify_yaml.py)).
  Reuses `compute_suggestion`, `sort_rows`, `write_report`, and
  `print_console_table` from `find_unassigned_scripts.py` so the report
  schema and confidence buckets stay identical between the script
  and YAML reports.

### Fixes and Maintenance
- Taught the topic_classifier unassigned-report tools about the new
  `bbq_control/bbq_settings.yml` path aliases. Extended
  `_to_bp_root()` in
  [compare_results.py](../topic_classifier/compare_results.py)
  to expand `{bp_mcs}/...` and `{bp_match}/...` into their canonical
  `{bp_root}/multiple_choice_statements/...` and
  `{bp_root}/matching_sets/...` forms, and added `YMMS` to
  `NON_SCRIPT_MARKERS` in
  [find_unassigned_scripts.py](../topic_classifier/find_unassigned_scripts.py).
  Without this,
  [find_unassigned_yaml.py](../topic_classifier/find_unassigned_yaml.py)
  raised `ValueError` on every new `{bp_mcs}` / `{bp_match}` row in
  the task CSVs, and assigned YAMLs all looked unassigned because
  the universe and the assigned set normalized to different prefixes.
  After the fix the report shows 19 assigned YAMLs (matching the 13
  `{bp_match}` and 6 `{bp_mcs}` rows in
  `bbq_control/task_files/*.csv`).

### Behavior or Interface Changes
- `find_unassigned_*` now emit alias-form paths (`{bp_mcs}/...`,
  `{bp_match}/...`) in both the console table and the report CSV's
  `script` column, so the values can be pasted directly into
  `bbq_control` task CSVs. Added `_to_alias()` in
  [compare_results.py](../topic_classifier/compare_results.py)
  as the inverse of `_to_bp_root()`; `write_report` and
  `short_script` in
  [find_unassigned_scripts.py](../topic_classifier/find_unassigned_scripts.py)
  use it before display/serialization. `{bp_root}/<chapter>-problems/`
  paths are unchanged because there is no shorter alias for them.

## 2026-04-28

### Additions and New Features
- Extracted the membrane transporter protein body into
  [transporter-protein.svg](../problems/biochemistry-problems/membranes/transporter-protein.svg)
  (waisted carrier silhouette plus dashed waist line, normalized to
  origin via `tools/normalize_svg.py`). The SVG is the new source of
  truth for the protein art -- editing it in Inkscape and re-running
  the sync script propagates the change to all three production
  membrane PGMLs in lockstep, matching how
  [phospholipid-unit.svg](../problems/biochemistry-problems/membranes/phospholipid-unit.svg)
  was already used as the source of truth for the phospholipid unit.
- Added [sync_membrane_svgs.py](../tools/sync_membrane_svgs.py),
  a small utility that reads each component SVG, extracts the inner
  content of its `<g id="...">` group, and rewrites the matching
  `# ---- BEGIN SYNC: <basename>.svg ----` block in every membrane
  PGML. Edit the SVGs, run `tools/sync_membrane_svgs.py`, lint --
  no manual paste-and-pray.

### Behavior or Interface Changes
- Restructured the v5 `membrane_transporter_svg` block in all three
  production PGMLs to delegate art to the component SVGs:
  - `$PHOSPHO_UNIT_SVG` and `$PROTEIN_INNER_SVG` are now populated
    inside `# ---- BEGIN/END SYNC: <basename>.svg ----` markers and
    are managed by the sync script (DO NOT EDIT BY HAND inside the
    markers).
  - `svg_backdrop()` no longer builds the protein path inline; it
    wraps the inlined `$PROTEIN_INNER_SVG` content in
    `<g transform="translate(173 53)">...</g>` so the SVG file can
    stay origin-anchored at (0,0) for clean Inkscape editing.
  - The unused `$PROTEIN_FILL` and `$PHOSPHO_HEAD_FILL` Perl
    constants were removed; color now lives in the SVG files
    alongside geometry.
- All three production PGMLs (Level 1
  [identify_transporter_type.pgml](../problems/biochemistry-problems/membranes/identify_transporter_type.pgml),
  Level 2
  [driving_force_from_gradient.pgml](../problems/biochemistry-problems/membranes/driving_force_from_gradient.pgml),
  Level 3
  [coupled_transport_perturbation.pgml](../problems/biochemistry-problems/membranes/coupled_transport_perturbation.pgml))
  pass renderer-API lint at seeds 1, 42, 100, 9999 with no errors
  after the sync refactor.

### Decisions and Failures
- The phospholipid SVG keeps its native (40, 140, 30, 40) viewBox
  because `tools/normalize_svg.py` cannot shift relative path
  commands (`m`, `c`, `z`); the existing matrix-transform placement
  in `svg_phospho_doublet` already handles its origin offset, so no
  rework was needed. The protein silhouette uses absolute path
  commands and was normalized to (0, 0, 74, 134) cleanly.
- The sync script enforces self-closing-only inner XML and rejects
  single-quote characters in the extracted content (would break
  Perl single-quoted string embedding). Both component SVGs comply
  today; revisit if a future SVG edit introduces nested groups or
  apostrophes in attribute values.

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
  [test_biochemistry_enzymelib.py](../tests/libs/test_biochemistry_enzymelib.py)
  -> `enzymes/enzymelib.py`,
  [test_biochemistry_sugarlib.py](../tests/libs/test_biochemistry_sugarlib.py)
  -> `carbs/sugarlib.py`,
  [test_henderson_hasselbalch.py](../tests/libs/test_henderson_hasselbalch.py)
  -> `buffers/Henderson-Hasselbalch.py`.
- Simplified `test_enzymelib_tree_and_html_table` by dropping the
  `len(enzyme_tree) == 4` and exact key-set assertions, per
  [PYTHON_STYLE.md](PYTHON_STYLE.md) "avoid tests that assert on
  collection sizes [or] required key lists".
- Updated
  [test_mc_statements_to_pgml.py](../tests/yaml/test_mc_statements_to_pgml.py)
  to assert `## TITLE(` and `## DESCRIPTION` membership rather than
  `startswith("## DESCRIPTION")`, since the generator now emits `## TITLE`
  first per commit `c6d43ba`. The remaining OPL header markers
  (`## KEYWORDS(`, `## DBsubject(`, `DOCUMENT();`, `PGcourse.pl`) are kept
  because they are external WeBWorK/OPL spec markers (boundary
  enforcement, not tunable internals).
- Added `description`, `keywords`, `title`, and `TITLE` to `ALLOWED_KEYS`
  in
  [check_mc_statements_yaml.py](../problems/multiple_choice_statements/check_mc_statements_yaml.py)
  so the validator accepts the same keys the generator already reads in
  [yaml_mc_statements_to_pgml.py](../problems/multiple_choice_statements/yaml_mc_statements_to_pgml.py).
  Five biochemistry MC statements YAMLs (enzyme_cofactors,
  enzyme_equilibrium, enzyme_inhibitors, gibbs_free_energy_equation,
  m-m_kinetics) now validate cleanly.
- Resolved pyflakes warnings by removing unused `import os` from
  [z_score_google_sheet.py](../problems/biostatistics-problems/z_score_google_sheet.py)
  and
  [cytogenetic_notation-disorders.py](../problems/inheritance-problems/cytogenetic_notation/cytogenetic_notation-disorders.py),
  dropping the leading `f` from f-strings without placeholders in
  [mm_lib.py](../problems/biochemistry-problems/enzymes/mm_lib.py)
  (3 lines),
  `_qc_membrane_pgmls.py`
  (1 line), and
  `_visual_qc_v4.py`
  (1 line), and removing an unused `lower = html.lower()` in
  `_qc_membrane_pgmls.py`.
- Fixed mixed-indentation in
  `_qc_membrane_pgmls.py`
  by extracting a multi-line tuple of double-escape regex patterns into
  a tab-indented `double_escape_patterns` constant before the `for` loop,
  replacing the space-aligned continuation that was tripping
  `tests/test_indentation.py`.
- Added `# nosec B310` annotation to the hardcoded-localhost
  `urllib.request.urlopen` call in
  `classifier_common.py`
  so Bandit no longer flags the Ollama probe; the URL is constructed from
  a fixed `http://localhost:11434` default and is not user-supplied.

### Removals and Deprecations
- Removed `test_yaml_match_to_pgml_inline_colors` from
  [test_pgml_generators.py](../tests/test_pgml_generators.py). Per
  [PYTHON_STYLE.md](PYTHON_STYLE.md), tests should not assert on
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
  [phospholipid-unit.svg](../problems/biochemistry-problems/membranes/phospholipid-unit.svg)
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
  `_svg_lineup.py`
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
  `_svg_lineup.py`.
  Callers look up a substrate by key (`'Na'`, `'glucose'`, ...) and
  get label, color, and chemical-class kind; kind drives the token
  shape so ions render as circles, sugars as hexagons, water as a
  small circle, and nucleotides as rounded rectangles.
- Added three WeBWorK PGML membrane-transporter problems under a new
  folder `membranes`:
  [identify_transporter_type.pgml](../problems/biochemistry-problems/membranes/identify_transporter_type.pgml)
  (Level 1: two-part classify + diagnostic feature),
  [driving_force_from_gradient.pgml](../problems/biochemistry-problems/membranes/driving_force_from_gradient.pgml)
  (Level 2: gradient-dot cues, which substrate moves down its gradient /
  provides the driving force), and
  [coupled_transport_perturbation.pgml](../problems/biochemistry-problems/membranes/coupled_transport_perturbation.pgml)
  (Level 3: NCX inhibitor scenarios, stoichiometry and net charge,
  reverse-mode NCX under ischemia, and a model-based symporter &rarr;
  antiporter "what would need to change" item). All three PGMLs share an
  inlined `# ==== BEGIN BLOCK: membrane_transporter_svg (v2) ====` block
  (same pattern as the fatty-acid lipid files). Named transporters appear
  in solutions for transfer: GLUT1, AQP1, SGLT1, LacY, NCX, NHE1, ANT.
  Structured 4-step solution skeleton (Classify / Evidence / Energetic /
  Real example) used uniformly across all three levels.
- Added a scratch SVG-renderer testbed at
  [_test_membrane_svg_block.pgml](../problems/biochemistry-problems/membranes/_test_membrane_svg_block.pgml)
  (underscore-prefix = dev-only) that renders six deterministic SVGs
  (uniporter inward/outward, symporter, 3&times;Na / Ca antiporter,
  antiporter + gradient dots, symporter + gradient dots) so the shared
  block can be visually verified without a full graded problem attached.
- Extended [test_webwork_lib.py](../tests/test_webwork_lib.py)
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

### Decisions and Failures
- Bumped the shared `membrane_transporter_svg` block from v3 to v4 after
  Round-2 A/B/C/D testing recommended Variant D (mechanism-focused) as the
  arrow treatment, Variant A's smaller arrowheads (base 3.5 / tip 6) to
  keep D's multi-element cue from overwhelming, and Variant C's
  pool-rect + graded-dot clustering for gradient cues. V3's single arrow
  through the protein still read as a colored pipe; v4's approach -> bind
  -> release sequence is the first iteration that actually visualizes
  alternating-access. Concrete v4 changes, propagated verbatim into all
  three production PGMLs
  ([identify_transporter_type.pgml](../problems/biochemistry-problems/membranes/identify_transporter_type.pgml),
  [driving_force_from_gradient.pgml](../problems/biochemistry-problems/membranes/driving_force_from_gradient.pgml),
  [coupled_transport_perturbation.pgml](../problems/biochemistry-problems/membranes/coupled_transport_perturbation.pgml)):
  (1) replaced the two-segment through-pipe arrow with an external
  approach arrow (`svg_approach_arrow_{in,out}`, y=50..55 for in and
  y=190..185 for out) + a central white-filled binding circle stroked in
  the substrate color at the waist (`svg_binding_dot`, cy=120, r=6) + a
  small release blob on the far compartment
  (`svg_release_blob_{in,out}`, r=7 at cy=195 or cy=45); (2) smaller
  arrowheads (base 3.5 / tip 6 vs v3's base 5 / tip 8) via Variant A;
  (3) clustered gradient dots with graded radii (3 -> 4) and opacity
  (0.75 -> 0.95), and a rounded-rect pool background
  (`fill-opacity="0.10"`) for clusters of >= 3 dots, tightened
  territories (left x=18..92, right x=310..384) via Variant C; (4) an
  optional 6th arg `$stagger` on `svg_solute_label` so callers can add a
  y-offset (left -2, right +3) when both substrates sit in the top
  compartment (both-inward symporter), breaking the horizontal lineup of
  two top labels. Retained V3b's waisted carrier silhouette, dashed
  waist line, lane constants (LEFT=185, RIGHT=235, CENTER=210),
  compartment labels, and lane-anchored solute labels (cx-16 for left,
  cx+16 for right/center). Dropped Variant B's compact-badge
  stoichiometry placement - the centered v3 placement (anchor=middle,
  y=24/y=222) tested cleaner than B's anchor=end. Block markers bumped
  to `# ==== BEGIN BLOCK: membrane_transporter_svg (v4)`. Added
  side-by-side v3-vs-v4 testbed at
  [_test_membrane_svg_v4.pgml](../problems/biochemistry-problems/membranes/_test_membrane_svg_v4.pgml)
  (Level 0, dev-only) that renders uniporter / 3 Na+ + 1 Ca2+
  antiporter / Na+ + glucose symporter-with-gradients cases in both
  versions for visual comparison. QC results: renderer-API lint clean
  at seeds 1, 42, 100, 9999 on all four files; full
  `_qc_membrane_pgmls.py` sweep (30 seeds per file) reports files with
  issues = 0; a new regex-based visual QC at
  `_visual_qc_v4.py`
  confirms zero internal-body arrow segments across all 9 seed/file
  combinations, binding-circle count == n_substrates, release blobs
  matching approach directions, stoich text at y=24 (no collision with
  "extracellular" at y=22), two anchor styles present for multi-solute
  cases, stagger firing iff both substrates are inward, and pool-rect
  background firing on count >= 3 gradient clusters.
- Bumped the shared `membrane_transporter_svg` block from v2 to v3 after
  reviewer feedback that the carrier silhouette read as a generic box and
  that multi-solute labels crowded each other at the lane. Built an A/B/C
  testbed at
  [_test_membrane_svg_v3_variants.pgml](../problems/biochemistry-problems/membranes/_test_membrane_svg_v3_variants.pgml)
  comparing three variants (V3a "minimal tweak", V3b "carrier shape",
  V3c "asymmetric cavity"); V3b won. V3c was rejected because its
  bottom-face cavity collided with the arrow base. Concrete v3 changes
  propagated verbatim into all three production PGMLs (Level 1/2/3):
  (1) waisted `<path>` carrier body pinched to x=183/237 at y=120
  (~9 px inward from the v2 rect edges) replaces the rounded `<rect>`,
  so the carrier vs. channel distinction survives at thumbnail size;
  (2) lane-anchored solute labels (left lane -> text-anchor=end at
  x=cx-16; right / center lane -> text-anchor=start at x=cx+16) eliminate
  overlap in symporter and antiporter scenes; (3) stoichiometry label
  centered above (y=24) or below (y=222) the blob with
  text-anchor=middle, instead of tucked to the left of the lane;
  (4) gradient dots parameterized by `(compartment, lane_side)` with
  lane-proximal ordering so density asymmetry tracks the substrate lane
  automatically (authors no longer need to hand-swap territories);
  (5) lane separation widened to 50 px (LEFT=185, RIGHT=235; was 36 px);
  (6) head-group visual weight reduced (r=2.6, opacity=0.75) so the
  bilayer texture no longer competes with the carrier body. Block
  markers bumped to `# ==== BEGIN BLOCK: membrane_transporter_svg (v3)`
  so a `grep` surfaces any future drift. QC sweep across 30 seeds on
  all three files reports zero errors / svg_mismatch / double_escape /
  waist_missing / pore_slot_present / correct_not_in_choices.
- The `membrane_transporter_svg` block went through two revisions. v1
  drew a continuous pale pore slot down the protein body; a reviewer
  flagged that this read as a channel, not a carrier, and undercut the
  whole classify-by-transport-logic pedagogy. v2 replaces the pore slot
  with a dashed horizontal waist line at y=120 (a conformational-gate
  cue), shortens each arrow into two segments interrupted by the waist,
  pulls substrate blobs closer to the membrane (y=40 / y=200), and
  renders all `<text>` elements as the last layer so labels sit on top
  of arrows, blobs, and gradient dots. A dev-only scratch PGML
  (`_test_membrane_svg_block.pgml`) with six hardcoded configurations
  was built first and lint-verified via the renderer API; the approved
  block was then pasted verbatim into all three production PGMLs with
  matching `BEGIN BLOCK / END BLOCK` markers so drift is greppable.
- Level 2 (`driving_force_from_gradient.pgml`) initially failed to
  compile with `syntax error near "draw on "` -- a misleading error
  message pointing at an innocuous comment. Bisecting suggested the
  combination of a mid-file `sub plain_label` defined after other setup
  code plus multi-delimiter packed scenario strings (`@@`, `##`, `~~`,
  `::` all in one literal) triggered some PG Safe-compartment parser
  edge case. Resolution: rewrote the scenario selection as a plain
  if/elsif chain populating bare package variables directly, with no
  packed strings and no mid-file subs. The specific root cause was not
  pinned down; if a similar error surfaces again, start by flattening
  any packed-string scenario encodings before deep-diving the syntax.

### Behavior or Interface Changes
- Relabeled the non-canonical distractor in
  [match_purine_structures.pgml](../problems/biochemistry-problems/PUBCHEM/NUCLEOBASES/match_purine_structures.pgml)
  and
  [match_pyrimidine_structures.pgml](../problems/biochemistry-problems/PUBCHEM/NUCLEOBASES/match_pyrimidine_structures.pgml)
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
  [melting_Tm_type_1.yml](../problems/multiple_choice_statements/biochemistry/melting_Tm_type_1.yml),
  [melting_Tm_type_2a.yml](../problems/multiple_choice_statements/biochemistry/melting_Tm_type_2a.yml),
  and [melting_Tm_type_2b.yml](../problems/multiple_choice_statements/biochemistry/melting_Tm_type_2b.yml)
  using Sanger/ABI chromatogram conventions sourced from the
  pre-approved palette in
  [TEMPLATE.yml](../problems/multiple_choice_statements/TEMPLATE.yml):
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
  `lipids`
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
  `NUCLEOBASES`:
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
  `lipids`
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
  `lipids`:
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
  `lipids`:
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
  2026-01-23, 779 lines) into [CHANGELOG-2026-04a.md](CHANGELOG-2026-04a.md),
  using the documented `docs/CHANGELOG-YYYY-MM[a-z].md` naming. Repaired
  a content-integrity bug: the 2026-01-22 day block was present
  identically in both the active changelog and the legacy archive,
  violating the existing rule that a date heading must not be split
  across files. The active duplicate was removed before rotation; the
  archived copy was kept as canonical.
- Renamed the legacy `docs/CHANGELOG_ARCHIVE_01.md` to
  [CHANGELOG-2026-01a.md](CHANGELOG-2026-01a.md) via `git mv` so
  history is preserved. The archive's date range is 2025-12-27 through
  2026-01-22; the most recent month included is 2026-01. The repo now
  uses a single archive naming style (`CHANGELOG-YYYY-MM[a-z].md`) end
  to end.
- Updated [REPO_STYLE.md](REPO_STYLE.md) (and the central copy in
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
  `PG_COMMON_PITFALLS.md`:
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
- Added `_spike_svg_choice.pgml`,
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
- Updated `SKILL.md`
  with a new "Self-contained PGML files" section documenting the
  per-file inlining convention and the `BEGIN BLOCK` versioning scheme.

### Developer Tests and Notes
- Verified all four PGMLs render cleanly at seeds 1, 42, 100, 9999 via
  the local renderer API (`lint_pg_via_renderer_api.py --json`): 5
  `<label>`s, 6 `<svg>`s (1 prompt + 5 choices), zero
  `&amp;alpha;/&amp;beta;` double-escapes, `error_flag = None`.

## 2026-04-19

### Behavior or Interface Changes
- [classify_scripts.py](../topic_classifier/classify_scripts.py) now runs one classification per `(script, flags, input)` variant defined in `biology-problems-website/bbq_control/task_files/*.csv`, instead of classifying each script path once with the first variant it found. Scripts with multi-variant CSV rows (e.g. `classify_Haworth.py --furan`/`--pyran`, `which_amino_acid.py --mc`/`--fib`, `protein_gel_migration.py --mc`/`--num`) now get a distinct classification and a CSV output row per variant. Output CSV rows populate the `flags` and `input` columns so the generated CSVs round-trip with the control files. Dry-run prints the expanded work list. Scripts not present in any CSV still classify once with no flags.
- Added `csv_handler.get_variants_for_script(assignments, script_path)` in `csv_handler.py` that enumerates `{flags, input}` variants for a script, returning a single empty variant when the script has no CSV rows so callers always have at least one work unit.
- [classify_scripts.py](../topic_classifier/classify_scripts.py) `classify_one_script(...)` now takes explicit `flags=""` and `input_file=""` parameters instead of looking them up from `assignments`, and populates those fields on the returned result dict. Replaced internal `_get_run_args(script, assignments)` with `_build_run_args(flags, input_file, repo_root)`. Existing-assignment match lookup keys directly on `f"{bp_root_path}|{flags}"` for per-variant diff accuracy. Repeat/consistency bookkeeping (`repeat_results`, `no_bbq_scripts`, `llm_error_scripts`) keys by `f"{script}|{flags}"` so variant runs do not collide.

### Fixes and Maintenance
- Fixed `BBQ_CONTROL_DIR` in [classify_scripts.py](../topic_classifier/classify_scripts.py) to point at `biology-problems-website/bbq_control/task_files/` (where the variant CSVs actually live) instead of `biology-problems-website/bbq_control/`. Previously `read_existing_assignments()` found zero CSVs and loaded 0 assignments, which silently disabled the existing-assignment match check and any variant-aware behavior.
- Made 14 previously silent bptools generators produce questions by default (tracked in `no_bbq_file.csv`). Running any of these scripts with no arguments now writes a `bbq-*-questions.txt` file.
  - Category A - changed `required=True` to `required=False, default='mc'` on `bptools.add_question_format_args(...)` in 6 gene_mapping generators: [tetrad_ordered-centromere_distance.py](../problems/inheritance-problems/gene_mapping/tetrad_ordered-centromere_distance.py), [tetrad_unordered_three_gene-find_one_distance.py](../problems/inheritance-problems/gene_mapping/tetrad_unordered_three_gene-find_one_distance.py), [tetrad_unordered_two_gene-find_distance.py](../problems/inheritance-problems/gene_mapping/tetrad_unordered_two_gene-find_distance.py), [three-point_test_cross-find_interence.py](../problems/inheritance-problems/gene_mapping/three-point_test_cross-find_interence.py), [three-point_test_cross-one_gene_distance.py](../problems/inheritance-problems/gene_mapping/three-point_test_cross-one_gene_distance.py), [two-point_test_cross-distance.py](../problems/inheritance-problems/gene_mapping/two-point_test_cross-distance.py).
  - Category A (custom groups) - added `parser.set_defaults(...)` and dropped `required=True` on the parental/recombinant and parental/double/genes mutually exclusive groups in [two-point_test_cross-which_genotypes.py](../problems/inheritance-problems/gene_mapping/two-point_test_cross-which_genotypes.py) and [three-point_test_cross-which_genotypes.py](../problems/inheritance-problems/gene_mapping/three-point_test_cross-which_genotypes.py) (default `parental`).
  - Category B - added `parser.set_defaults(mode="same")` to the `--same`/`--different` group in [gene_tree_matches_plus.py](../problems/inheritance-problems/phylogenetic_trees/gene_tree_matches_plus.py).
  - Category C - added sys.path insertion for the sibling `inheritance-problems/` directory so `import genotypelib` resolves in [unique_gametes.py](../problems/inheritance-problems/large_crosses/unique_gametes.py), [unique_cross_genotypes.py](../problems/inheritance-problems/large_crosses/unique_cross_genotypes.py), and [unique_cross_phenotypes.py](../problems/inheritance-problems/large_crosses/unique_cross_phenotypes.py). Matches the pattern already used in [dihybrid_cross_epistatic_gene_interactions.py](../problems/inheritance-problems/epistasis/dihybrid_cross_epistatic_gene_interactions.py).
  - Category D - replaced hard-coded `problems/*/data/<file>` paths with `bptools.get_repo_data_path("<file>")` in [z_score_google_sheet.py](../problems/biostatistics-problems/z_score_google_sheet.py) (`student_names.txt`) and [cytogenetic_notation-disorders.py](../problems/inheritance-problems/cytogenetic_notation/cytogenetic_notation-disorders.py) (`cytogenetic_disorders.yml`). Both files live at the repo-root `data/` directory.
  - Deferred: [wordle_peptides.py](../problems/biochemistry-problems/PUBCHEM/PEPTIDES/wordle_peptides.py) still fails with an lxml XML parse error on cached HTML (separate bug, not a defaults issue).

### Decisions and Failures
- `bptools.add_question_format_args(...)` (bptools.py:364) already supported `required=False, default=...`. No change to `bptools.py` was necessary - the Category A fix is purely site-local updates to the script parse_arguments calls, matching the pattern endorsed in [PYTHON_STYLE.md](PYTHON_STYLE.md) (ARGPARSE section).
