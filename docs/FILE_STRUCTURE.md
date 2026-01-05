# File structure

## Overview
- This repo is a collection of standalone Python generators for biology problem sets.
- Domain-specific generators live in `problems/*-problems/` folders.
- Shared helpers live at the repo root.
- Input data and content banks live in `data/`, `matching_sets/`, and
  `problems/multiple_choice_statements/`.
- Generated outputs are ignored by git; see `.gitignore` for `bbq-*.txt`, `qti*.zip`, and
  `selftest-*.html`.
- Follow [docs/REPO_STYLE.md](docs/REPO_STYLE.md) for naming and placement rules.

## Top-level directories
- `problems/biochemistry-problems/`: biochemistry question generators.
- `problems/biostatistics-problems/`: statistics and analysis generators.
- `problems/cell_biology-problems/`: cell biology generators.
- `problems/dna_profiling-problems/`: DNA profiling generators.
- `problems/inheritance-problems/`: genetics and inheritance generators.
- `problems/laboratory-problems/`: lab-focused question generators.
- `problems/molecular_biology-problems/`: molecular biology generators.

## Shared code and templates
- `bptools.py`: shared formatting and utility helpers used by many generators.
- `TEMPLATE.py`: starting point for new generators (argparse + output pattern).
- `find_all_imports.py`: helper for scanning Python imports when updating deps.

## Library modules (`*lib.py`)
- `problems/biochemistry-problems/aminoacidlib.py`: amino acid structure helpers for building
  HTML formulas and structural parts used in amino acid questions.
- `problems/biochemistry-problems/buffers/bufferslib.py`: buffer system data and utilities
  (pKa ranges, states, and color sets) used by buffer-range and buffer-state items.
- `problems/biochemistry-problems/carbohydrates_classification/sugarlib.py`: carbohydrate
  nomenclature and HTML table helpers for sugar structures and classification.
- `problems/biochemistry-problems/enzymelib.py`: generates enzyme pH/temperature tables and
  randomized enzyme sets for activity and optimization questions.
- `problems/biochemistry-problems/metaboliclib.py`: colored letter utilities for labeling
  metabolic pathway steps and mapping questions.
- `problems/biochemistry-problems/proteinlib.py`: parses protein pI/MW data and provides
  helpers for isoelectric point and protein comparison questions.
- `problems/biochemistry-problems/PUBCHEM/aminoacidlib.py`: amino acid formula parsing and
  similarity helpers used with PubChem-derived data and CRC utilities.
- `problems/biochemistry-problems/PUBCHEM/moleculelib.py`: SMILES/CRC helpers and inline
  HTML scaffolding for molecule rendering (RDKit JS).
- `problems/biochemistry-problems/PUBCHEM/pubchemlib.py`: PubChem REST client with YAML
  caching for molecule lookups and metadata retrieval.
- `problems/dna_profiling-problems/gellib.py`: gel electrophoresis band generation and
  image helpers built on PIL for profiling questions.
- `problems/inheritance-problems/chisquare/chisquarelib.py`: chi-square helpers (p-values
  and critical values) used by statistics and genetics tests.
- `problems/inheritance-problems/deletionlib.py`: deletion mapping and ordering helpers
  used in mutant analysis problems.
- `problems/inheritance-problems/disorderlib.py`: genetic disorder scenario generator that
  loads `data/genetic_disorders.yml` and builds multi-disorder cases.
- `problems/inheritance-problems/genemapping/genemaplib.py`: gene mapping helpers, colored
  phenotype tables, and recombination utilities.
- `problems/inheritance-problems/genemapping/tetradlib.py`: tetrad analysis table helpers
  layered on `genemaplib` for meiosis mapping questions.
- `problems/inheritance-problems/genetrees/Deprecated/classic_phylolib/phylolib.py`:
  deprecated phylogeny helper (classic phylolib wrappers).
- `problems/inheritance-problems/genotypelib.py`: genotype formatting, letter generation,
  and combinatorics helpers for cross problems.
- `problems/inheritance-problems/hybridcrosslib.py`: dihybrid/epistasis utilities, ratio
  dictionaries, and table construction for interaction problems.
- `problems/inheritance-problems/pedigrees/pedigree_lib/template_generator.py`: higher-level pedigree
  scenario picker that selects mode-specific templates and returns code strings.
- `problems/inheritance-problems/pedigrees/pedigree_lib/code_templates.py`: curated pedigree
  code-string templates grouped by inheritance mode.
- `problems/inheritance-problems/pedigrees/pedigree_lib/validation.py`: pedigree code
  validation helpers for checking allowed symbols and row structure.
- `problems/inheritance-problems/pedigrees/pedigree_lib/code_definitions.py`: pedigree code constants
  and helpers for mirroring and generation counting.
- `problems/inheritance-problems/pedigrees/pedigree_lib/html_output.py`: HTML rendering for
  pedigree code strings.
- `problems/inheritance-problems/pedigrees/pedigree_lib/svg_output.py`: SVG rendering for
  pedigree code strings, plus SVG-to-PNG conversion via `rsvg-convert`.
- `problems/inheritance-problems/pedigrees/pedigree_lib/graph_parse.py`: graph-based pedigree
  types and layout helpers for graph-based pedigrees and code-string rendering.
- `problems/inheritance-problems/pedigrees/pedigree_lib/skeleton.py`: procedural pedigree
  skeleton generation (founders, children, marriages).
- `problems/inheritance-problems/pedigrees/pedigree_lib/inheritance_assign.py`: inheritance-mode
  phenotype assignment for graph-based pedigrees.
- `problems/inheritance-problems/pedigrees/pedigree_lib/graph_spec.py`: parse/serialize helpers
  for the compact pedigree IR string format.
- `problems/inheritance-problems/pedigrees/pedigree_lib/mode_validate.py`: inheritance
  mode validation layered on parsed pedigree graphs.
- `problems/inheritance-problems/pedigrees/pedigree_lib/preview_pedigree.py`: CLI helper for generating
  HTML/PNG preview sets with saved code strings.
- `problems/inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md`: local architecture note
  describing the pedigree graph to layout to rendering pipeline.
- `problems/inheritance-problems/pointtestcrosslib.py`: deprecated point-testcross helper
  (use `genemaplib.py` and `genemapclass.py` instead).
- `problems/molecular_biology-problems/restrictlib.py`: restriction enzyme lookup and
  analysis helpers built on Biopython and web queries.
- `problems/molecular_biology-problems/seqlib.py`: DNA/RNA sequence utilities for
  complements, transcription/translation, and HTML table rendering.

## Data and content banks
- `data/`: YAML/CSV/HTML/text inputs and reference tables used by generators.
- `matching_sets/`: YAML banks and templates for matching questions.
- `problems/multiple_choice_statements/`: YAML banks and helper scripts for statement-based
  multiple choice.
- `images/`: static images referenced by HTML question text.
- `javascript/`: small JS assets for HTML outputs and testing.

## Tools and tests
- `tools/`: small utilities (for example, markdown TOC generation and conversion scripts).
- `tests/`: lightweight checks such as `run_pyflakes.sh`.

## Root-level docs and misc
- [README.md](README.md): broad description and sample output.
- [AGENTS.md](AGENTS.md): agent instructions and repository workflow guardrails.
- [LICENSE](LICENSE): repository licensing terms.
- `.gitignore`: ignored outputs and local artifacts.
- `docs/`: repo documentation (see [docs/REPO_STYLE.md](docs/REPO_STYLE.md)).
- `requirements.txt`: Python dependencies for generators and tooling.
- Word lists and scratch files: `SHORT_WORDS.txt`, `science.txt`, `science-count.txt`,
  `temp.txt`.
