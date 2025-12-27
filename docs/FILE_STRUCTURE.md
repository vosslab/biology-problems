# File structure

## Overview
- This repo is a collection of standalone Python generators for biology problem sets.
- Domain-specific generators live in `*-problems/` folders.
- Shared helpers live at the repo root.
- Input data and content banks live in `data/`, `matching_sets/`, and
  `multiple_choice_statements/`.
- Generated outputs are ignored by git; see `.gitignore` for `bbq-*.txt`, `qti*.zip`, and
  `selftest-*.html`.
- Follow [docs/REPO_STYLE.md](docs/REPO_STYLE.md) for naming and placement rules.

## Top-level directories
- `biochemistry-problems/`: biochemistry question generators.
- `biostatistics-problems/`: statistics and analysis generators.
- `cell_biology-problems/`: cell biology generators.
- `dna_profiling-problems/`: DNA profiling generators.
- `inheritance-problems/`: genetics and inheritance generators.
- `laboratory-problems/`: lab-focused question generators.
- `molecular_biology-problems/`: molecular biology generators.

## Shared code and templates
- `bptools.py`: shared formatting and utility helpers used by many generators.
- `TEMPLATE.py`: starting point for new generators (argparse + output pattern).
- `find_all_imports.py`: helper for scanning Python imports when updating deps.

## Library modules (`*lib.py`)
- `biochemistry-problems/aminoacidlib.py`: amino acid structure helpers for building
  HTML formulas and structural parts used in amino acid questions.
- `biochemistry-problems/buffers/bufferslib.py`: buffer system data and utilities
  (pKa ranges, states, and color sets) used by buffer-range and buffer-state items.
- `biochemistry-problems/carbohydrates_classification/sugarlib.py`: carbohydrate
  nomenclature and HTML table helpers for sugar structures and classification.
- `biochemistry-problems/enzymelib.py`: generates enzyme pH/temperature tables and
  randomized enzyme sets for activity and optimization questions.
- `biochemistry-problems/metaboliclib.py`: colored letter utilities for labeling
  metabolic pathway steps and mapping questions.
- `biochemistry-problems/proteinlib.py`: parses protein pI/MW data and provides
  helpers for isoelectric point and protein comparison questions.
- `biochemistry-problems/PUBCHEM/aminoacidlib.py`: amino acid formula parsing and
  similarity helpers used with PubChem-derived data and CRC utilities.
- `biochemistry-problems/PUBCHEM/moleculelib.py`: SMILES/CRC helpers and inline
  HTML scaffolding for molecule rendering (RDKit JS).
- `biochemistry-problems/PUBCHEM/pubchemlib.py`: PubChem REST client with YAML
  caching for molecule lookups and metadata retrieval.
- `dna_profiling-problems/gellib.py`: gel electrophoresis band generation and
  image helpers built on PIL for profiling questions.
- `inheritance-problems/chisquare/chisquarelib.py`: chi-square helpers (p-values
  and critical values) used by statistics and genetics tests.
- `inheritance-problems/deletionlib.py`: deletion mapping and ordering helpers
  used in mutant analysis problems.
- `inheritance-problems/disorderlib.py`: genetic disorder scenario generator that
  loads `data/genetic_disorders.yml` and builds multi-disorder cases.
- `inheritance-problems/genemapping/genemaplib.py`: gene mapping helpers, colored
  phenotype tables, and recombination utilities.
- `inheritance-problems/genemapping/tetradlib.py`: tetrad analysis table helpers
  layered on `genemaplib` for meiosis mapping questions.
- `inheritance-problems/genetrees/Deprecated/classic_phylolib/phylolib.py`:
  deprecated phylogeny helper (classic phylolib wrappers).
- `inheritance-problems/genotypelib.py`: genotype formatting, letter generation,
  and combinatorics helpers for cross problems.
- `inheritance-problems/hybridcrosslib.py`: dihybrid/epistasis utilities, ratio
  dictionaries, and table construction for interaction problems.
- `inheritance-problems/pedigrees/pedigree_template_gen_lib.py`: higher-level pedigree
  scenario picker that selects mode-specific templates and returns code strings.
- `inheritance-problems/pedigrees/pedigree_code_templates.py`: curated pedigree
  code-string templates grouped by inheritance mode.
- `inheritance-problems/pedigrees/pedigree_validate_lib.py`: pedigree code
  validation helpers for checking allowed symbols and row structure.
- `inheritance-problems/pedigrees/pedigree_code_lib.py`: pedigree code constants
  and helpers for mirroring and generation counting.
- `inheritance-problems/pedigrees/pedigree_html_lib.py`: HTML rendering for
  pedigree code strings.
- `inheritance-problems/pedigrees/pedigree_png_lib.py`: PNG rendering for
  pedigree code strings.
- `inheritance-problems/pedigrees/pedigree_graph_lib.py`: graph-based pedigree
  types and layout helpers for graph-based pedigrees and code-string rendering.
- `inheritance-problems/pedigrees/pedigree_skeleton_lib.py`: procedural pedigree
  skeleton generation (founders, children, marriages).
- `inheritance-problems/pedigrees/pedigree_inheritance_lib.py`: inheritance-mode
  phenotype assignment for graph-based pedigrees.
- `inheritance-problems/pedigrees/pedigree_mode_validate_lib.py`: inheritance
  mode validation layered on parsed pedigree graphs.
- `inheritance-problems/pedigrees/preview_pedigree.py`: CLI helper for generating
  HTML/PNG preview sets with saved code strings.
- `inheritance-problems/pedigrees/PEDIGREE_PIPELINE.md`: local architecture note
  describing the pedigree graph to layout to rendering pipeline.
- `inheritance-problems/pointtestcrosslib.py`: deprecated point-testcross helper
  (use `genemaplib.py` and `genemapclass.py` instead).
- `molecular_biology-problems/restrictlib.py`: restriction enzyme lookup and
  analysis helpers built on Biopython and web queries.
- `molecular_biology-problems/seqlib.py`: DNA/RNA sequence utilities for
  complements, transcription/translation, and HTML table rendering.

## Data and content banks
- `data/`: YAML/CSV/HTML/text inputs and reference tables used by generators.
- `matching_sets/`: YAML banks and templates for matching questions.
- `multiple_choice_statements/`: YAML banks and helper scripts for statement-based
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
