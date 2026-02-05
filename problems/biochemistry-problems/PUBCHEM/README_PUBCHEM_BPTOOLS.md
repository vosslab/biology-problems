# PubChem Python/bptools Authoring Guide (Blackboard)

This guide covers the PubChem-related Python generators in this folder that
emit Blackboard-format questions via `bptools`. It complements the PGML docs
in `README_PUBCHEM_PGML.md`.

## Scope

Use this for scripts like:

- `which_macromolecule.py`
- `which_amino_acid.py`
- `match_amino_acid_structures.py`
- `polypeptide_mc_sequence.py`
- `polypeptide_fib_sequence.py`

These are **Blackboard** generators, not WeBWorK PGML.

## Script map (Python generators vs utilities)

Primary bptools generators:

- `alpha_amino_acid_identification.py`: identify the alpha-amino acid structure (RDKit canvas + MC).
- `which_macromolecule.py`: macromolecule ID (RDKit canvas + MC).
- `which_amino_acid.py`: amino acid ID (RDKit canvas + MC or FIB).
- `match_amino_acid_structures.py`: structure-to-name matching (MAT).
- `polypeptide_mc_sequence.py`: peptide sequence MC with RDKit rendering.
- `polypeptide_fib_sequence.py`: peptide sequence FIB with RDKit rendering.

Utility and one-off scripts (not bptools outputs):

- `pubchemlib.py`: PubChem API wrapper + cache.
- `moleculelib.py`: RDKit.js HTML/JS builders for generic molecules.
- `aminoacidlib.py`: amino acid helpers + RDKit.js builders.
- `generate_alpha_amino_acid_identification_pg.py`: builds the WebWork `.pg` file from shared YAML.
- `generate_alpha_amino_acid_review_html.py`: builds a combined HTML review page (RDKit canvas) from shared YAML.
- `molecule_lookup.py`, `molecule_search.py`: ad-hoc data tools (not production generators).
- `get_molecules_from_reactions.py`: YAML extractor for reaction lists.
- `generate_macromolecule_id_pgml.py`: PGML conversion helper.
- `new_poly.py`, `poly-alanine_template.py`, `wordle_peptides.py`: experiments/prototypes.

## Quick start

```bash
source source_me.sh
python3 problems/biochemistry-problems/PUBCHEM/which_macromolecule.py -d 1 -x 1
```

Generated files are `bbq-*.txt` and should not be committed.

## Key modules and data

- `pubchemlib.py`: PubChem lookup and caching logic.
- `moleculelib.py`: RDKit.js HTML/JS rendering helpers.
- `aminoacidlib.py`: amino-acid and peptide rendering helpers.
- `data/pubchem_molecules_data.yml`: primary PubChem cache (repo data file).
- `MACROMOLECULE_CATEGORIZE/macromolecules.yml`: source list for macromolecule types.
- `TOOLS/molecules.yml`, `TOOLS/compounds.yml`: source lists for PubChem lookups.
- `TOOLS/molecules.txt`: ad-hoc source list for molecule lookup tooling.
- `amino_acid_distractors.yml`: shared alpha/distractor sets for the
  alpha-amino-acid identification questions (used by both Python and PG).

## PubChem API and caching

`pubchemlib.PubChemLib` manages caching to avoid repeated API calls:

- Uses `data/pubchem_molecules_data.yml` for the main cache.
- Adds a small random sleep after each API call to avoid rate limits.
- Writes the cache on close only if new API calls were made.

Guidelines:

- Always use `PubChemLib()` instead of ad-hoc requests.
- Keep API-heavy loops bounded or run them offline and commit data only if needed.
- Call `close()` so cache updates are persisted when new data is fetched.

## Blackboard HTML/JS sanitization (critical)

Blackboard aggressively sanitizes JavaScript and can inject whitespace into
function tokens. This breaks RDKit.js initialization unless we keep the legacy
comment-split pattern used in `moleculelib.py` and `aminoacidlib.py`.

**Do not remove or reformat these comment splits.**

Examples used in this repo:

```javascript
function/* */getPeptideBonds(mol){
let/* */smiles="...";
```

Guidelines:

- Keep JavaScript assembled as single-line strings (avoid auto-formatters).
- Preserve comment splits like `function/* */name` and `let/* */var`.
- Avoid "cleanup" passes that normalize whitespace in JS strings.
- If Blackboard mangles a script, revert to the exact pattern above.

## RDKit.js rendering flow

Common flow used by the generators:

- Call `generate_load_script()` to load RDKit.js once per question.
- Build a `<canvas>` per molecule and inject JS from `generate_js_functions(...)`.
- Keep the JS blocks in the exact string form from `moleculelib.py` or
  `aminoacidlib.py` to avoid Blackboard whitespace corruption.

If you add new rendering helpers, copy the JS style from the existing helpers
instead of reformatting.

## bptools flags used here

Many PubChem scripts set these flags:

- `bptools.allow_insert_hidden_terms = False`
- `bptools.allow_no_click_div = False`
- `bptools.use_nocopy_script = False` (in peptide generators)

These are intentional to reduce Blackboard HTML interference with RDKit output.

## Output conventions

- Use `bptools.formatBB_*_Question(...)` for final formatting.
- Use `bptools.collect_and_write_questions(write_question, args, outfile)`.
- Keep output names predictable via `bptools.make_outfile(...)`.

## Shared choice data (alpha amino acid question)

The alpha-amino-acid identification question uses a shared YAML file with
aligned distractor sets:

- `amino_acid_distractors.yml`

Each set defines an `alpha` name and at least three `distractors`. The Python
generator (`alpha_amino_acid_identification.py`) reads it directly and can
optionally target a specific set with `-a/--amino-acid`. The WebWork `.pg` file
is generated from the same YAML via `generate_alpha_amino_acid_identification_pg.py`.

When you update the YAML list, re-run the generator to refresh
`alpha_amino_acid_identification.pg`.

You can also generate an instructor review page:

```bash
python3 problems/biochemistry-problems/PUBCHEM/generate_alpha_amino_acid_review_html.py
```

## Known pitfalls (avoid these)

- Do not call `pubchemlib` methods as module-level functions. Always instantiate
  `PubChemLib()` and use the instance.
- Do not reformat or pretty-print embedded JavaScript strings.
- Do not assume `get_similar_amino_acids(...)` can run without a `PubChemLib`
  instance. Pass the instance explicitly from the generator.

## Testing

Run the script with a small duplicate count and max question limit:

```bash
python3 problems/biochemistry-problems/PUBCHEM/which_macromolecule.py -d 1 -x 1
```

Inspect the generated `bbq-*.txt` for:

- RDKit canvas present
- No JavaScript errors when previewed
- Choices and answer formatting correct
