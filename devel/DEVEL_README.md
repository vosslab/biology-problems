# devel scripts

> This file is vendored. Local changes can and will be overwritten by propagation.

`devel/` holds engineering commands for highly technical maintainers working on
the repository itself. These commands may require source-tree knowledge, Git,
development dependencies, or internal fixtures. The canonical placement policy
is [docs/REPO_STYLE.md](../docs/REPO_STYLE.md#scripts-and-executables).

Use this folder for repository lifecycle and engineering work:

- Git, version, release, and changelog maintenance.
- Dependency refresh, environment setup, builds, packaging, and source generation.
- Lint, benchmark, probe, diagnostic, screenshot, and engineering-evidence commands.
- Documentation repair, repository hygiene, and local or vendored engineering helpers.

## Placement classifier

- Use `devel/` for maintainer and repository-engineering commands.
- Use [tools/TOOLS_README.md](../tools/TOOLS_README.md) for optional standalone user utilities
  whose domain input produces a useful domain result.
- Use the application CLI or package for primary workflows and reusable application behavior.
- Use an optional local `launchers/` directory for thin compatibility or convenience delegates
  into the application.

## Import boundary

Use `tools/`, `devel/`, `tests/`, and `launchers/` as support locations rather than
repository-level import packages. Maintainer commands in `devel/` may keep the established flat
sibling-helper pattern used by helpers such as `changelog_lib`, `version_lib`, and `version_files`.
The support-directory gate preserves this boundary and the homes of locally owned or vendored
engineering helpers.

## Propagated devel scripts

Some developer tools arrive by propagation and appear in `devel/` when this repo's
`REPO_TYPE` calls for them. Keep these vendored helpers in `devel/` alongside locally authored
engineering commands.

`devel/make_release.py` ships to the `scripted`, `compiled`, and `other` families, including
their descendants (`python`, `pypi`, `rust`, and `swift`). It prepares a GitHub source release:
CalVer freshness check, free-tag check, committed `LICENSE.<SPDX>` verification,
zip and tgz archive build with byte-level checks of every license, LLM-prompt generation for
the release description, optional `docs/RELEASE_HISTORY.md` and `docs/NEWS.md` updates,
and printed `git tag` + `gh release create` commands. Use `--dry-run` to preview or
`--write` to update doc files. See [docs/REPO_STYLE.md](../docs/REPO_STYLE.md) versioning
section for the full flow.

Other propagated devel tools are type-specific, so a repo receives only the ones
matching its `REPO_TYPE`. Examples include Python release publishing helpers and
TypeScript setup/rendering helpers.

## Repository mapping with Graphify

[graphify_map_repo.py](graphify_map_repo.py) builds a queryable map of this
repository and writes agent orientation to `graphify-out/MANAGER_CONTEXT.md`.
Read that file before exploring an unfamiliar repository: it names the major
areas, the architectural hubs, the cross-area connectors, and the map size.

Build or refresh the map, then read the orientation:

```bash
source source_me.sh && python3 devel/graphify_map_repo.py
source source_me.sh && python3 devel/graphify_map_repo.py --context
```

Force a full refresh only when needed. Use local Ollama when the Claude allowance is exhausted:

```bash
source source_me.sh && python3 devel/graphify_map_repo.py --fresh
source source_me.sh && python3 devel/graphify_map_repo.py --fresh --ollama
```

Prefer targeted Graphify traversal over a broad repository sweep:

```bash
graphify query "<question>" --budget 1500
graphify explain "<symbol_or_path>"
graphify affected "<symbol_or_path>" --depth 2
```

### Published map page

`--svg` writes both `docs/GRAPHIFY.md` and its compact `docs/GRAPHIFY_map.svg` from an
existing map:

```bash
source source_me.sh && python3 devel/graphify_map_repo.py --svg
```

Add the flag to a build when the map and published documentation should advance together:

```bash
source source_me.sh && python3 devel/graphify_map_repo.py --update --svg
source source_me.sh && python3 devel/graphify_map_repo.py --fresh --svg
```

The figure is generated directly from `graph.json`. It shows the largest twelve communities,
scales circles by membership, and weights lines by intercommunity relationships. It carries no
per-symbol labels or legend; names, repository groups, representative symbols, and observations
remain readable and searchable in the Markdown page.

`graphify-out/` is generated output and stays out of Git. The page and SVG describe the repository
where they were generated, so neither is shared between repositories. Scope comes from
`.graphifyignore`.

### Rust test symbols

Graphify's Rust extractor indexes `#[cfg(test)] mod tests` contents as
production symbols. Because those modules live inside `src/*.rs`, no ignore rule
can exclude them without dropping the production code beside them.

In a repository with a `Cargo.toml`, a fresh build therefore extracts without
clustering, removes those symbols from `graph.json`, and clusters what remains,
so community detection and hub ranking never see the test suite. The run reports
how many nodes and links it removed.

Incremental updates do not prune, because re-clustering renumbers communities
and would strand the stored labels. Orientation still filters test symbols out
of what it prints, which covers updates and other languages' inline test
conventions.

## Running scripts

For Python scripts, use the repo bootstrap environment:

```bash
source source_me.sh && python3 devel/<script>.py
```

Run individual scripts with `--help` for current options. Keep command details
in script help output instead of duplicating them here.
