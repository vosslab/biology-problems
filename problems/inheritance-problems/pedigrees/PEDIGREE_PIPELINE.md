# Pedigree homework pipeline

The three homework commands share family construction, biological evaluation, teaching filters,
layout, a local accepted-case bank, and export. The teaching reference is Lecture 05C,
*Pedigrees*, September 29, 2026. See [PEDIGREE_AUTHORING.md](PEDIGREE_AUTHORING.md) for YAML.
The focused authorities below own the detailed rules:

- [PEDIGREE_DIFFICULTY.md](PEDIGREE_DIFFICULTY.md): workload presets and construction.
- [PEDIGREE_BIOLOGY.md](PEDIGREE_BIOLOGY.md): inheritance and teaching acceptance.
- [PEDIGREE_LAYOUT.md](PEDIGREE_LAYOUT.md): layout geometry and rendering.
- [PEDIGREE_POLISHING.md](PEDIGREE_POLISHING.md): bounded repair and polishing.
- [PEDIGREE_RANKING.md](PEDIGREE_RANKING.md): candidate ordering and evidence.
- [PEDIGREE_PROBABILITY.md](PEDIGREE_PROBABILITY.md): diagnostic-only probability analysis.
- [PEDIGREE_GRAPH_ANALYSIS.md](PEDIGREE_GRAPH_ANALYSIS.md): similarity and complexity.
- [PEDIGREE_RUBRIC.md](PEDIGREE_RUBRIC.md): fixed visual-review instructions and score limits.
- [PEDIGREE_EVIDENCE.md](PEDIGREE_EVIDENCE.md): accumulated ratings, production decisions, and caveats.

## Generate homework

From the repository root:

```bash
source source_me.sh
python3 problems/inheritance-problems/pedigrees/write_pedigree_to_pattern.py -d 10 --selftest
python3 problems/inheritance-problems/pedigrees/write_pedigree_pattern_matching.py -d 3 -B -I
python3 problems/inheritance-problems/pedigrees/write_pattern_to_pedigree.py -d 3 --selftest
```

- `write_pedigree_to_pattern.py`: one pedigree, select its inheritance pattern.
- `write_pattern_to_pedigree.py`: a named pattern, select the corresponding pedigree.
- `write_pedigree_pattern_matching.py`: match pedigrees to all five inheritance patterns.
- All commands use randomly generated families, freshly constructed or reused from the local bank.
- `-A` / `--autosomal` provides a warm-up using only autosomal dominant and autosomal recessive.
  Identification offers two pattern choices; selection and matching use two pedigrees. Exports add
  an `autosomal` filename suffix. Difficulty and all acceptance checks still apply.
- `-s SEED` makes procedural choices reproducible. Family construction, mirroring, mode selection,
  and matching order use random selection, not question-number cycling. The CLI seeds both its
  procedural generator and the legacy RNG used by bptools/QTI. Reproduction with cache also depends
  on current bank contents; use `--fresh -s SEED` to replay fresh candidate generation.
- `--affected-color darkred` (or another supported dark hue) sets affected-symbol fill;
  `-C` / `--random-color` selects one of 14 dark hues per question. These options are exclusive.
- `-d` counts questions. `-r output_pedigree/review` saves editable SVGs and instructor-only JSON.
- Shared `--selftest`, `-O`, `-B`, and `-I` flags retain browser and Blackboard workflows.

The old authored-bank source flags are retired. Authored YAML remains for library examples and
regression fixtures; homework commands do not select authored cases.

## Local pedigree bank

Commands share per-difficulty JSONL files under the ignored repository-root
`output_pedigree_cache/` directory:

- `pedigree_cache_easy.jsonl`
- `pedigree_cache_medium.jsonl`
- `pedigree_cache_rigorous.jsonl`
- `pedigree_cache_bonus.jsonl`

Generation is single-threaded. Each bank expires 24 hours after its last actual append; read-only
runs and duplicate-only appends do not renew expiry. Expiry uses file modification time, and a
separate `.jsonl.lock` coordinates deletion and writes. A stale bank is replaced on its next use,
including `--fresh`. Files expire independently.

Default/`--use-cache` runs randomly choose eligible entries, then generate a shortage. `--fresh`
bypasses the bank for selection, creates a full fresh pool, then appends accepted new entries.
Fresh accepted and polished families are saved even if not exported. Exact duplicate records are
omitted; graph-isomorphic but differently encoded cases may remain. Eligibility rechecks current
biology, teaching, geometry, difficulty, and format-specific limits. Compact records reconstruct a
compatible genotype witness and recompute layout; they do not preserve original genotypes.

Identification prepares 20 candidates per requested question; selection and matching prepare 100
per question, or 40 with `--autosomal`. Cached entries are filtered to the offered inheritance modes
before ranking, and fresh generation samples only those modes. The bank remains shared.
`-x` caps exports and does not reduce this pool target. If the initial sample does not
contain complete comparable sets, the pipeline asks the bank for additional random batches before
fresh generation. It adds batches up to ten times. Selection and matching assemble complete groups
across all offered modes with shared depth and founding-family count; incomplete groups are unused.
The highest-ranked eligible entries are used. Choices and selected questions are shuffled before
normal bptools export. Collector retries use unused reserve scenarios. Requests larger than the
available complete scenarios fail explicitly.

Each line stores mode, sex sequence, affected and carrier indexes, and ordered parent-child unions.
For example, this below-minimum-size family illustrates the compact record shape:

```json
{"mode":"AR","sex":"mfmf","affected":[2],"carriers":[0,1],"families":[[0,1,[2,3]]]}
```

Person indexes are zero-based positions in `sex`; `m` and `f` mean male and female. The record
omits full genotypes and geometry. File locks protect concurrent readers, expiry, and appenders on
macOS/Linux; separate runs may select the same reusable case.

## Preparation flow

For each fresh candidate, the pipeline simulates a family and applies rare-trait, biological,
teaching, and layout acceptance. Bonus identification pools use the terminal-frontier constructor;
easy, other difficulties, and other formats use procedural construction. The public
`generate_candidate` helper retains baseline construction, while `generate_pool` routes by the
actual question format. Construction first validates the planned layout before biology is
simulated. Frontier IDs stay local to the candidate call. After ordinary acceptance, the pipeline
checks the actual `Diagram` endpoints. Downward repair and ordinary polishing each run as usual; if
either changes the terminal endpoints, the pipeline discards that stage's proposal and retains its
accepted input. This preserves the endpoint contract without changing either stage's internal
acceptance rules. Every fresh candidate enters the downward-repair stage; it changes only a
qualifying rigorous workload and otherwise returns the case unchanged. The ordinary bounded
polisher then runs for every workload, including easy, bonus, selection, and matching. See
[PEDIGREE_POLISHING.md](PEDIGREE_POLISHING.md) for exact scopes and stops. Cached cases are
revalidated and ranked in the current pool without biological repolishing. Accepted candidates are
sorted by [PEDIGREE_RANKING.md](PEDIGREE_RANKING.md), then assembled into question scenarios.
The CLI reports elapsed preparation time, including generation, polishing, and assembly.

Each fresh candidate request for a mode gets at most 5,000 attempts. If no suitable family is found,
the pipeline raises `GenerationFailure` with rejection counts. If valid cached or fresh cases do not
yield enough complete scenarios, it tries up to ten additional pool batches before failing with an
explicit count of distinct candidates and completed scenarios.

The eligible pool score is recalculated on each run; it is not saved in cache records and is not a
calibrated quality estimate. Immutable family objects cache member indexes, parentage, and validated
generation ranks for reuse within the pipeline. Public mapping methods return independent
dictionaries; new or replaced families validate and cache their own structure.

## Modules

| Module | Responsibility |
| --- | --- |
| [family.py](pedigree_lib/family.py) | Person, union, family, observations, structural validation |
| [graphs.py](pedigree_lib/graphs.py) | NetworkX snapshots and family components |
| [difficulty.py](pedigree_lib/difficulty.py) | Workload presets and structural filters |
| [inheritance.py](pedigree_lib/inheritance.py) | Modes, transmissions, simulation, compatibility |
| [policy.py](pedigree_lib/policy.py) | Visible teaching evidence and assessment |
| [sources.py](pedigree_lib/sources.py) | Cases, family construction, simulation sources |
| [questions.py](pedigree_lib/questions.py) | Evaluation, generation, presentation, matching sets |
| [layout.py](pedigree_lib/layout.py) | Symbol positions, labels, connector geometry, layout checks |
| [html_output.py](pedigree_lib/html_output.py) | Positioned HTML renderer |
| [svg_output.py](pedigree_lib/svg_output.py) | Editable SVG renderer |
| [cli.py](pedigree_lib/cli.py) | Arguments, question formatting, instructor exports |
| [scenarios.py](pedigree_lib/scenarios.py) | Pool preparation and comparable scenario assembly |
| [cache.py](pedigree_lib/cache.py) | Compact records, expiry, locking, and validation |
| [downward_repair.py](pedigree_lib/downward_repair.py) | Rigorous bottom-gap repair |
| [polishing.py](pedigree_lib/polishing.py) | Bounded terminal-child additions |
| [ranking.py](pedigree_lib/ranking.py) | Five-signal pool-relative ordering |
| [similarity.py](pedigree_lib/similarity.py) | Graph similarity and complexity |
| [features.py](pedigree_lib/features.py) | Topology-only experimental measurements |
| [geometry_features.py](pedigree_lib/geometry_features.py) | Native-space row density and bottom-gap measures |
| [generation_features.py](pedigree_lib/generation_features.py) | Generation counts, progression, and shrink |
| [affected_features.py](pedigree_lib/affected_features.py) | Visible affected-reach and region-fill measures |
| [offspring_probability.py](pedigree_lib/offspring_probability.py) | Fixed-cross probability diagnostic |

The executable scripts are thin callers of these modules. The old character-grid, graph-string,
and associated internal interfaces are removed.

## Verification

Focused pedigree regressions live under `tests/libs/pedigrees/`; the full repository command is
`source source_me.sh && pytest tests/`. Current static and review contracts are documented in
[PEDIGREE_BIOLOGY.md](PEDIGREE_BIOLOGY.md), [PEDIGREE_LAYOUT.md](PEDIGREE_LAYOUT.md),
[PEDIGREE_POLISHING.md](PEDIGREE_POLISHING.md), [PEDIGREE_RANKING.md](PEDIGREE_RANKING.md),
and [PEDIGREE_PROBABILITY.md](PEDIGREE_PROBABILITY.md). Historical one-time verification results
belong to their dated changelog entries and sibling `pedigree-aesthetics` evidence files; they are
not current performance guarantees.
